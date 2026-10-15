# Expense Tracker API

A small REST API for creating and inspecting expenses. The service is built with
[FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/),
and Pydantic.

## Features

- Create an expense with an amount, category, and description.
- Retrieve an expense identifier.
- Search by category and specify a result limit.
- Automatically create the `expenses` table when the application starts.
- Expose interactive API documentation through FastAPI.

## Requirements

- Python 3.10 or newer
- A database supported by SQLAlchemy
- The SQLAlchemy database driver required by your database

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the application dependencies:

   ```powershell
   pip install fastapi uvicorn sqlalchemy python-dotenv
   ```

   Install the appropriate SQLAlchemy database driver separately when needed.
   For example, PostgreSQL deployments commonly use:

   ```powershell
   pip install psycopg[binary]
   ```

3. Create a `.env` file in the project root and set the database connection
   string:

   ```env
   DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/expense_tracker
   ```

   `DATABASE_URL` is required. The application raises an error at startup when
   it is not configured. Do not commit `.env`; it is ignored by Git.

## Run the API

Start the development server from the project root:

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Interactive documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### `GET /hello`

Returns a greeting:

```json
{
  "message": "Hello, Avinash."
}
```

### `GET /expenses/{expense_id}`

Returns a confirmation for the supplied expense identifier:

```json
{
  "expense_id": 1,
  "message": "Expense retrieved successfully."
}
```

### `GET /search`

Searches by category and accepts an optional `limit` query parameter. The
default limit is `100`.

Example:

```text
GET /search?category=food&limit=25
```

Response:

```json
{
  "category": "food",
  "limit": 25
}
```

### `POST /expenses`

Creates an expense. The request body must contain:

| Field | Type | Rules |
| --- | --- | --- |
| `amount` | number | Greater than `0` |
| `category` | string | 1–50 characters |
| `description` | string | 1–200 characters |

Example request:

```json
{
  "amount": 24.50,
  "category": "food",
  "description": "Lunch"
}
```

Example response:

```json
{
  "id": 1,
  "amount": 24.5,
  "category": "food",
  "description": "Lunch"
}
```

## Project structure

```text
.
├── database.py   # Database URL, SQLAlchemy engine, sessions, and base class
├── main.py       # FastAPI application and route handlers
├── models.py     # SQLAlchemy expense model
└── README.md
```

## Database model

The `expenses` table contains:

- `id`: auto-incrementing integer primary key
- `amount`: required numeric value with precision `10,2`
- `category`: required string up to 50 characters
- `description`: required string up to 200 characters

## Notes

The current `GET /expenses/{expense_id}` and `GET /search` handlers return
confirmation data rather than querying and returning stored expense records.
