# swiftform-backend

## Installation and Setup

### Setting up the Environtment Variables

Before running the application, you need to set up the necessary environment variables. These may include database URLs, secret keys, API keys, etc.

There's a sample env file called `.env.example`. You can simply rename it to `.env`

### Setting up the Environment

1. **Create a virtual environment:**

Use the following command to create a virtual environment named 'venv':

```bash
python -m venv venv
```

2. **Activate the virtual environment:**

Activate the virtual environment with this command:

```bash
source venv/Scripts/activate
```

3. **Verify python version:**

Ensure you are using Python 3.12 for this environment. You can check your Python version with:

```
python --version
```

The output should be Python 3.12.

5. **Install required dependencies:**

Install all necessary dependencies from the `requirements.txt` file:

```
pip install -r requirements.txt
```

### Start the flask application

Run the Flask application using the following command:

```bash
flask run
```

### Installing Docker

Ensure Docker is installed on your system. If not, download and install it from the [official Docker website](https://docs.docker.com/engine/install/).

Navigate to the root directory of the swiftform-backend project and use the terminal to run the following command:

```bash
docker compose up --build
```

### Accessing the API

After successfully running the Docker setup, the API should now be accessible via localhost:8000. You can test this by navigating to `http://localhost:8000` in your web browser or using a tool like Postman to send requests to the API.

### Database Setup

You need to have a postgresql database connected to do the ff. Make sure you have activated your environment before doing so.

Run Alembic migrations to set up the database schema:

```
alembic upgrade head
```

### Database Migrations with Alembic

To manage database migrations with Alembic in your Flask project, follow these commands:

#### 1. Generate Migration

Create a new migration script after making changes to your models:

```bash
alembic revision --autogenerate -m "Description of changes"
```

#### 2. Apply Migrations

Update your database to the latest migration:

```bash
alembic upgrade head
```

This command applies any pending migrations and updates your database schema.

#### 3. Rollback Migrations

If you encounter issues or need to revert the database to a previous state, you can roll back the last applied migration using the following command:

```bash
alembic downgrade -1
```

Running this command will undo the changes introduced by the last migration, effectively rolling back your database schema to the state it was in before the last migration was applied. Be cautious when using downgrade, as it can lead to data loss if not handled carefully.

### Formatting and Linting Files

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting. [pre-commit](https://pre-commit.com/) is used to automate the running of `ruff` checks before each commit.

#### How to Use

Before your first commit, ensure you have `pre-commit` installed and the hooks set up by running:

```bash
pre-commit install
```

After installation, it should automatically address issues before commits are finalized.

#### Manually Running Checks

To manually run all configured pre-commit checks on all files:

```bash
pre-commit run --all-files
```
