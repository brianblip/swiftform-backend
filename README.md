# AI Form Builder Backend

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL Database

### Setting up the Environtment Variables

Before running the application, you need to set up the necessary environment variables.

Locate the `.env.sample` file in the project's root directory and rename it to `.env` ."

```
# .env.sample

# openai
OPENAI_API_KEY= # will only be used if OPEN_AI_ENABLED is true
OPEN_AI_ENABLED=false # disabled by default to prevent accidental charges

FLASK_DEBUG=1 # 0 for production, 1 for development
FLASK_APP=project # name of the folder containing the app

# postgres
DATABASE_URL='postgresql://postgres:password@localhost:5433/form_builder' # change this to your postgres database url

JWT_SECRET_KEY='7b69b40ac69d7c4c44213f20b10115f5346f76d2895c46583a1bbb2fdb0ede59' # you can generate a key by typing python -c 'import secrets; print(secrets.token_hex())' in your terminal
```

### Setting up the Environment

1. Create a virtual environment:

> Make sure you are using the correct python version to create the virtual environment

```bash
python -m venv venv
# or python3.11 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/Scripts/activate
```

3. Install required dependencies:

```
pip install -r requirements.txt
```

### Database Setup

You need to have a postgresql database connected to do the ff. Make sure you have activated your environment before doing so.

Run Alembic migrations to set up the database schema:

```
alembic upgrade head
```

### Start the flask application

Run the Flask application using the following command:

```bash
flask run
```
