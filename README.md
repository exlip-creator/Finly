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