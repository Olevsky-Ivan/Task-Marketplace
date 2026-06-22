# Task Marketplace API

A backend REST API for a freelance task marketplace. Users can post tasks, assign executors, leave comments, and manage wallets.

> **This is the initial commit.** Includes project foundation: models, database setup, core configuration, and security utilities. API routes are not yet implemented.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) |
| Hashing | Passlib (bcrypt) |
| Server | Uvicorn |

---

## Project Structure

```
app/
├── main.py                 # FastAPI app instance
├── core/
│   ├── config.py           # Environment settings
│   ├── security.py         # JWT + bcrypt utilities
│   └── deps.py             # DB session & auth dependencies
├── database/
│   └── session.py          # SQLAlchemy engine and session factory
└── models/
    ├── user.py
    ├── wallet.py
    ├── task.py
    └── comment.py
```

---

## Database Models

### User
| Field | Type | Description |
|---|---|---|
| `id` | Integer PK | Primary key |
| `email` | String, unique | User email |
| `hashed_password` | String | bcrypt hash |
| `role` | String | `executor` or `admin` |
| `created_at` | DateTime | Auto-set on creation |

### Wallet
| Field | Type | Description |
|---|---|---|
| `id` | Integer PK | Primary key |
| `user_id` | FK → User | Owner |
| `balance` | Numeric | Current balance |

### Task
| Field | Type | Description |
|---|---|---|
| `id` | Integer PK | Primary key |
| `title` | String | Task title |
| `description` | Text | Full description |
| `status` | Enum | `new` / `in_progress` / `done` |
| `price` | Numeric | Reward amount |
| `creator_id` | FK → User | Posted by |
| `executor_id` | FK → User (nullable) | Assigned to |

### Comment
| Field | Type | Description |
|---|---|---|
| `id` | Integer PK | Primary key |
| `text` | Text | Comment body |
| `task_id` | FK → Task | Parent task |
| `user_id` | FK → User | Author |
| `created_at` | DateTime | Auto-set on creation |

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- `.env` file based on `.env.example`

### Install & Run

```bash
git clone https://github.com/your-username/task-marketplace-api.git
cd task-marketplace-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```
