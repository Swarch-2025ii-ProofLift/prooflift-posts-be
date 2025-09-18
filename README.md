# Posting Service

This service provides functionalities related to posts, comments, and reactions for ProofLift.

## Running the Service

### 1. Clone the repository
```bash
git clone https://github.com/Swarch-2025ii-ProofLift/prooflift-posts-be
cd prooflift-posts-be
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the service locally
```bash
uvicorn app.main:app --reload
```

### 5. Access the API
The API will be available at:
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