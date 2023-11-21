export DATABASE_NAME=<your_db>
export DATABASE_USER=
export DATABASE_PASSWORD=
export DATABASE_HOST=

PROJECT_NAME = ecom
PYTHON = python3
VENV_DIR = env
ALEMBIC_CONFIG = alembic.ini

revision:
	echo "Running revision"
	alembic -c ${ALEMBIC_CONFIG} revision --autogenerate --head head

upgrade:
	echo "Upgrading head..."
	alembic -c ${ALEMBIC_CONFIG} upgrade head

runserver:
	echo "Starting Uvicorn"
	uvicorn main:app --reload

test:
	echo "Running Unit Tests"
	pytest -vs