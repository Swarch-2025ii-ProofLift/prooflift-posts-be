# Posting Service

This service provides functionalities related to posts, comments, and reactions for ProofLift.

## Running the Service

You can run this service either locally or using Docker.

### Option 1: Running Locally

#### 1. Clone the repository
```bash
git clone https://github.com/Swarch-2025ii-ProofLift/prooflift-posts-be
cd prooflift-posts-be
```

#### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables
Create a `.env` file in the root of the project using `.env.example` as a template.

When running locally set:

```
DB_HOST=localhost
MQ_HOST=localhost
```

This ensures the service connects to your locally installed PostgreSQL instance and RabbitMQ server.

#### 5. Run the service locally
```bash
uvicorn app.main:app --reload
```

### Option 2: Running with Docker

#### 1. Clone the repository
```bash
git clone https://github.com/Swarch-2025ii-ProofLift/prooflift-posts-be
cd prooflift-posts-be
```

#### 2. Set up environment variables
Create a `.env` file in the root of the project using `.env.example` as a template.

When running the service with Docker, the database and message queue hosts should point to the services defined in `docker-compose.yml`:

```
DB_HOST=prooflift-posts-db
MQ_HOST=prooflift-notifications-mq
```

This ensures the service connects to the Postgres and RabbitMQ containers inside the Docker network.

#### 3. Build and run with Docker Compose
```bash
docker-compose up --build
```

### Accessing the API

The API will be available at (both locally and with Docker)
- GraphQL Playground: `http://localhost:8000/graphql`
- Status check: `http://localhost:8000`

## Message Queue Integration

This service publishes notification events to a RabbitMQ message queue when users interact with posts:
- **Comment events**: Notifies post owners when someone comments on their post
- **Reaction events**: Notifies post owners when someone reacts to their post

The MQ connection is configured via environment variables (`MQ_HOST`, `MQ_PORT`, `MQ_USER`, `MQ_PASSWORD`, `MQ_QUEUE`).

## Project Structure
```
app/
├── api/
│   └── graphql/
│       ├── mutations/      # GraphQL mutations
│       ├── queries/        # GraphQL queries
│       └── types/          # GraphQL types
│
├── core/                   # Core configs
│
├── db/                     # Database configuration
│
├── events/                 # Event publishing
│
├── models/                 # Database models
│
├── mq/                     # Message queue connection
│
├── repositories/           # Data access
│
├── schemas/                # Pydantic schemas
│
├── services/               # Business logic
│
└── utils/                  # Helpers
```