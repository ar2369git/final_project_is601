# 📦 Project Setup

This is a FastAPI-based calculator application with JWT authentication, SQLAlchemy for persistence, and full test coverage. These instructions will get you up and running locally (and optionally in Docker) in minutes.

---

## 🔗 1. Clone the Repo

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

---

## 🐍 2. Python Environment

1. **Create & activate** a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

2. **Upgrade pip** and **install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 🗄️ 3. Database Configuration

By default, this app uses SQLite at `./data/app.db`. You can override this:

- **SQLite** custom path:

  ```bash
  export DB_PATH=/absolute/path/to/my.db
  ```

- **PostgreSQL** or other:

  ```bash
  export DATABASE_URL=postgresql://user:password@localhost:5432/dbname
  ```

### Initialize the schema

```bash
python -c "from app.db import init_db; init_db()"
```

---

## 📜 4. Environment Variables

Create a `.env` file in the project root (requires `python-dotenv`, already in `requirements.txt`):

```ini
# .env
JWT_SECRET_KEY=your-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶️ 5. Run the Application

```bash
# with auto-reload for development
uvicorn main:app --reload
```

Open your browser at <http://127.0.0.1:8000> or explore the API docs at <http://127.0.0.1:8000/docs>.

---

## ✅ 6. Run the Test Suite

This project includes **unit**, **integration**, and **end-to-end** tests:

```bash
pytest
```

Make sure everything passes before you push!

---

## 🐳 7. Docker (Optional)

1. **Build** the image:

   ```bash
   docker build -t fastapi-calculator .
   ```

2. **Run** the container (reads your `.env`):

   ```bash
   docker run --env-file .env -p 8000:8000 fastapi-calculator
   ```

---

## 🛠️ 8. GitHub Actions & CI

On every push, GitHub Actions will:

1. Run **pytest** (all tests).
2. Build the Docker image.
3. (If configured) Push the image to Docker Hub.

See `.github/workflows/ci.yml` for the full pipeline.

---

## 🔖 Cheat-Sheet & Useful Commands

| Task                          | Command                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| Create venv                   | `python3 -m venv venv`                                                  |
| Activate venv                 | macOS/Linux: `source venv/bin/activate` / Windows: `venv\Scripts\activate` |
| Install dependencies          | `pip install -r requirements.txt`                                       |
| Initialize DB                 | `python -c "from app.db import init_db; init_db()"`                     |
| Run server (dev)              | `uvicorn main:app --reload`                                             |
| Run tests                     | `pytest`                                                                |
| Build Docker image            | `docker build -t fastapi-calculator .`                                  |
| Run Docker container          | `docker run --env-file .env -p 8000:8000 fastapi-calculator`            |
| Show API docs                 | Visit `/docs` on your running server                                    |

---

## Docker Repository for this project:

https://hub.docker.com/r/ar2369/final_project_is601


## 📚 Quick Links

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)
- [Pytest](https://docs.pytest.org/)
- [GitHub Actions](https://docs.github.com/actions)
