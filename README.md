# swiftform-backend

## Installation and Setup

### Setting up the Environtment Variables

Before running the application, you need to set up the necessary environment variables. These may include database URLs, secret keys, API keys, etc.

There's a sample env file called `.env.example`. You can simply rename it to `.env`

### Installing Docker

Ensure Docker is installed on your system. If not, download and install it from the [official Docker website](https://docs.docker.com/engine/install/).

Navigate to the root directory of the swiftform-backend project and use the terminal to run the following command:

```bash
docker compose up --build
```

### Accessing the API

After successfully running the Docker setup, the API should now be accessible via localhost:8000. You can test this by navigating to `http://localhost:8000` in your web browser or using a tool like Postman to send requests to the API.
