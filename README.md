### FastAPI Boilerplate with SQLAlchemy and Alembic for Migration Management.

#### Steps
-   Clone the Repo
-   COPY env.example as .env and add environment variables there.
-   I have added a demo example.Example Model, You can remove it and also remove it's import inside db/base.py
-   Add your model files and Create Your Model inside db/models/ and List their imports inside db/base.py so that Alembic can track them
-   To Create migrations run
    -   ```alembic revision --autogenerate -m "Commit Message"```
-   To Apply Migrations
    -   ```alembic upgrade head```