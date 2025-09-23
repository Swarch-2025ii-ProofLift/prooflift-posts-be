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
```

This ensures the service connects to your locally installed PostgreSQL instance.

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

When running the service with Docker, the database host should point to the database service defined in `docker-compose.yml`:

```
DB_HOST=prooflift-posts-db
```

This ensures the service connects to the Postgres container inside the Docker network.

#### 3. Build and run with Docker Compose
```bash
docker-compose up --build
```

### Accessing the API

The API will be available at (both locally and with Docker)
- GraphQL Playground: `http://localhost:8000/graphql`
- Status check: `http://localhost:8000`

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
├── models/                 # Database models
│
├── repositories/           # Data access
│
├── schemas/                # Pydantic schemas
│
├── services/               # Business logic
│
└── utils/                  # Helpers
```