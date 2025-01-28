---

# ZKP Project

This project implements a Zero-Knowledge Proof (ZKP) system where clients upload CSV files and generate proofs that are verified by the server. The project uses Python for both the client and server, and the system is managed using Docker Compose.

## Prerequisites

Before you begin, ensure that you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```
.
├── ./client
│   ├── ./client/app
│   ├── ./client/data
│   ├── ./client/.env
├── ./requirements.txt
├── ./server
│   ├── ./server/app
│   ├── ./server/.env
│   ├── ./server/test.db
│   └── ./server/uploads
├── docker-compose.yml
```

### Client
The client is responsible for uploading CSV files and generating Zero-Knowledge Proofs. The client runs inside a Docker container and uses Python to handle file processing and communication with the server.

### Server
The server handles file uploads, generates public keys, verifies proofs, and manages an SQLite database to store checksums and public keys.

## Setup

### 1. Clone the Repository

First, clone the repository:

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Build and Start the Containers

Use Docker Compose to build and start the containers. The `-d` flag will run the containers in detached mode.

```bash
docker compose up --build -d
```

This command will:
- Build the Docker images for the client and server.
- Start the containers for both the client and the server in the background.

### 3. Interact with the Client

The client container is set to sleep indefinitely when it starts, so you can manually run the client at your convenience.

To interact with the client, you need to exec into the running container:

```bash
docker exec -it zkp-client-1 bash
```

This will drop you into the client container's shell.

### 4. Run the Client Application

Once you're inside the client container, run the client application with the following command:

```bash
python -m app.main
```

This will execute the `main.py` file inside the `client/app` directory and start the process of uploading a file and generating a proof.

You can also execute client code with the given command:

```bash
docker exec -it zkp-client-1 python -m app.main
```

### 5. Server Operations

The server will automatically start and run in the background when the `docker compose up` command is executed.

You can access logs from the server to monitor the status of the server:

```bash
docker logs -f zkp-server-1
```

### 6. Stopping the Containers

To stop the containers, run:

```bash
docker compose down
```

This will stop and remove the containers. If you want to stop them but keep the containers running (detached mode), you can use:

```bash
docker compose stop
```

### 7. Database Access

If you'd like to interact with the database inside the server container (e.g., check or modify records), you can exec into the container and use SQLite commands:

```bash
docker exec -it zkp-server-1 bash
```

Once inside the server container, you can access the database like so:

```bash
sqlite3 /app/server/test.db
```

### Troubleshooting

- If you encounter any issues with Docker Compose, check the logs for both the client and server containers using the following command:

  ```bash
  docker logs -f zkp-client-1
  docker logs -f zkp-server-1
  ```

- Ensure the environment variables in `.env` files are correctly configured.

---
