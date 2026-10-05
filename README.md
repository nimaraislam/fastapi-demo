# LIA Platform – FastAPI Demo

A small demo backend for the LIA (internship) platform. It shows how to use **FastAPI** with **PostgreSQL**, **async SQLAlchemy** and **connection pooling**, with `cities` and `users` as a first example.

## What's inside

| Part | Technology |
|---|---|
| Web framework | FastAPI |
| Server | Uvicorn |
| Database | PostgreSQL 16 (runs in Docker) |
| ORM | SQLAlchemy 2 (async) |
| DB driver | asyncpg |
| Validation | Pydantic |

**Endpoints**

| Method | URL | Description |
|---|---|---|
| GET | `/` | Homepage |
| POST | `/cities` | Create a city |
| GET | `/cities` | List all cities |
| POST | `/users` | Create a user (the city must exist) |
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | Get one user |

---

## 1. Prerequisites

Install these first:

- **Git**: https://git-scm.com/downloads
- **Python 3.11 or newer**: https://www.python.org/downloads/ (on Windows, tick "Add Python to PATH" during install)
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/ (must be **running** before you start the database)

Check that they work:

```powershell
git --version
python --version
docker --version
```

---

## 2. Get the code

```powershell
git clone https://github.com/nimaraislam/fastapi-demo.git
cd fastapi-demo
```

Replace `<your-username>` and `<repo-name>` with the real values from the GitHub page.

---

## 3. Create a virtual environment and install packages

A virtual environment keeps this project's Python packages separate from the rest of your computer.

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell says "running scripts is disabled", run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

When it works, your prompt starts with `(venv)`.

---

## 4. Create the `.env` file

The `.env` file holds settings and is **not** stored in Git. Copy the example file:

**Windows**
```powershell
copy .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

If there is no `.env.example`, create a file named `.env` in the project root with this content:

```
DATABASE_URL=postgresql+asyncpg://fastapi_demo:fastapi_demo@localhost:5432/fastapi_demo
```

---

## 5. Start the database

Make sure Docker Desktop is running, then:

```powershell
docker compose up -d
docker compose ps
```

`docker compose ps` should show the `db` service as `Up`.

> **Port 5432 already in use?** Another PostgreSQL (for example from a different project's Docker container, or one installed on your computer) is using the same port. Stop it first, for example with `docker compose down` in the other project's folder.

---

## 6. Run the application

```powershell
uvicorn app.main:app --reload
```

The tables are created automatically when the app starts.

Open in your browser:

- **http://127.0.0.1:8000/** – homepage
- **http://127.0.0.1:8000/docs** – interactive API page where you can try every endpoint

Stop the server with `Ctrl + C`.

---

## 7. Try it out

On the `/docs` page, click an endpoint, then **Try it out**, edit the body, and click **Execute**. Create a city first, because users need one.

**1. `POST /cities`**
```json
{"name": "Malmö", "region": "Skåne", "latitude": 55.605, "longitude": 13.0038}
```

**2. `POST /users`**
```json
{"name": "Test User", "email": "test@example.com", "phone": "0701234567", "city_id": 1}
```

**3. `GET /users`** to see the result.

Things that should fail on purpose (to see the validation working):

| Test | Expected |
|---|---|
| Create the same city twice | `400 City already exists` |
| Create the same email twice | `400 Email already registered` |
| Use `"city_id": 999` | `400 City does not exist` |
| Use `"email": "abc"` | `422` validation error |

---

## 8. Look inside the database

Open an interactive PostgreSQL session (run this in the project folder):

```powershell
docker compose exec db psql -U fastapi_demo -d fastapi_demo
```

Useful commands inside it:

| Command | What it does |
|---|---|
| `\dt` | List tables |
| `\d users` | Show the columns of `users` |
| `SELECT * FROM cities;` | Show all cities |
| `SELECT * FROM users;` | Show all users |
| `\q` | Quit |

SQL commands must end with `;`.

---

## 9. Stop and reset

```powershell
docker compose down        # stop the database, keep the data
docker compose down -v     # stop the database AND delete all data (fresh start)
```

Use `down -v` if you change a model and want the tables rebuilt from scratch. This demo creates tables with `create_all`, which does not update tables that already exist.

---

## Project structure

```
.
├── app/
│   ├── main.py          # creates the app, plugs in the routers
│   ├── database.py      # async engine + connection pool settings
│   ├── schemas.py       # Pydantic schemas (what the API accepts/returns)
│   ├── models/          # SQLAlchemy models (the database tables)
│   │   ├── base.py
│   │   ├── city.py
│   │   └── user.py
│   └── routers/         # API endpoints, one file per area
│       ├── cities.py
│       └── users.py
├── compose.yaml         # PostgreSQL in Docker
├── requirements.txt     # Python packages
├── .env.example         # example settings (copy to .env)
└── README.md
```

**Models vs schemas:** a *model* describes how data is stored in the database. A *schema* describes what the API accepts and returns. They are kept separate so clients cannot set fields like `id` or `is_active`, and so private fields like `password_hash` are never sent back.

---

## Connection pooling

Opening a new database connection for every request is slow. A **connection pool** keeps a set of open connections and reuses them. The settings are in `app/database.py`:

| Setting | Value | Meaning |
|---|---|---|
| `pool_size` | 5 | Connections kept open |
| `max_overflow` | 10 | Extra connections allowed during bursts |
| `pool_timeout` | 30 | Seconds to wait for a free connection |
| `pool_recycle` | 1800 | Refresh connections after 30 minutes |

Each Uvicorn worker process has its **own** pool. With 4 workers and `pool_size=5`, up to 20 connections can be open (more with overflow), so keep this in mind when scaling. For larger setups, a pooler such as PgBouncer can sit in front of PostgreSQL.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `failed to connect to the docker API` | Docker Desktop is not running. Start it and wait until it is ready. |
| `port is already allocated` (5432) | Another PostgreSQL is using the port. Stop it, or change the port in `compose.yaml` **and** `.env`. |
| `connection timeout` / `Connect call failed` when starting the app | The database is not running. Run `docker compose up -d` and check `docker compose ps`. |
| `ModuleNotFoundError` | The virtual environment is not active, or packages are missing. Activate `venv` and run `pip install -r requirements.txt`. |
| `no configuration file provided` | You are in the wrong folder. `cd` into the project folder (where `compose.yaml` is). |
| Tables are missing or have old columns | Run `docker compose down -v`, then `docker compose up -d`, then start the app again. |

---

## Notes

- This is a **demo**. In the real project, database changes will be managed with Alembic migrations instead of `create_all`.
- Never commit the `.env` file. It is listed in `.gitignore`.
