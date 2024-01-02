# AI Form Builder Backend

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL Database

### Setting up the Environtment Variables

Before running the application, you need to set up the necessary environment variables. These may include database URLs, secret keys, API keys, etc. 

Create a file named `.env` in the root directory of your project and add your environment variables like so:

```
FLASK_DEBUG=1  
FLASK_APP=project  

DATABASE_URL=<YOUR_POSTGRESQL_DATABASE_URL>

# no need to activate open ai for now to save money
OPENAI_API_KEY= # not needed for now
OPEN_AI_ENABLED=false #  
```

### Setting up the Environment

1. Create a virtual environment:

> Make sure you are using the correct python version  to create the virtual environment
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
