# Finly

Web-service for personal finance accounting

## Project structure

- backend/ - server part
- frontend/ - client part

## Backend's stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Psycopg
- pytest and httpx
- Ruff

## Requirements
- Python 3.14.4

## Launch backend
Run the following commands from the project root directory.
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment to isolate project dependencies:
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Install the dependencies listed in `requirements.txt`:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Start the application:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   The `--reload` option automatically restarts the server when the code changes. Use it during development.
Once the server is running, you can access:

- Application: http://127.0.0.1:8000
- Application health check: http://127.0.0.1:8000/health
- API documentation: http://127.0.0.1:8000/docs

Press `Ctrl+C` to stop the server.

For subsequent runs, navigate to the `backend` directory, activate the virtual environment, and start the server. Reinstall dependencies whenever `requirements.txt` changes.

## Launch database

Install Docker with Docker Compose before proceeding.

1. Create a `.env` file in the project root and configure the database credentials:
   ```dotenv
   POSTGRES_DB=finly
   POSTGRES_USER=finly
   POSTGRES_PASSWORD=replace_with_your_password
   ```
   Replace the example password with your own. Add `.env` to `.gitignore` to keep credentials out of version control.
2. Start the database from the project root:
   ```bash
   docker compose up -d db
   ```
3. Check the container status:
   ```bash
   docker compose ps
   ```
The database is available to applications running on your computer at `localhost:54321`. PostgreSQL uses port `5432` inside the container.
To open the PostgreSQL console:
```bash
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```
To stop the database:
```bash
docker compose stop db
```

Database data is stored in the `postgres_data` volume and persists across container recreation. The credentials in `.env` are used during the first initialization; changing them later does not update existing database users or passwords.