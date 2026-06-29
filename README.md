# Task Marketplace

A FastAPI backend for a task marketplace with an internal virtual wallet system.

## Features

- JWT authentication with role-based access (`admin`, `customer`, `executor`)
- Virtual wallet: balance freezing on task creation, auto-transfer on approval
- Full task lifecycle: `open → in_progress → submitted → approved / cancelled`
- Task filtering by status, author, date range with limit/offset pagination
- Categories, tags (M2M), comments per task

## Tech Stack

- **FastAPI** + **SQLAlchemy 2.0** (async) + **PostgreSQL**
- **Alembic** for migrations
- **bcrypt** / **JWT** for auth
- **Docker** + **Docker Compose**

## Project Structure

```
app/
├── auth/          # register, login, JWT
├── core/          # config, dependencies
├── database/      # base, session
├── models/        # User, Task, Wallet, Transaction, Category, Tag, Comment
├── tasks/         # router, service, repository, schemas
├── users/         # router, service, repository, schemas
└── wallet/        # router, service, repository, schemas
alembic/           # migrations
```

## Wallet Logic

| Event | Effect |
|---|---|
| Customer creates task | `balance -= reward`, `frozen_balance += reward` |
| Manager approves task | `frozen_balance -= reward`, executor `balance += reward` |
| Task cancelled / deleted | `frozen_balance -= reward`, `balance += reward` |

## Quick Start

**1. Clone & configure**

```bash
git clone https://github.com/Olevsky-Ivan/Task-Marketplace.git
cd Task-Marketplace
cp .env.example .env
```

**.env example**

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=task_marketplace
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**2. Run**

```bash
docker compose up --build
```

Migrations run automatically on startup. API available at `http://localhost:8000`.

## API Overview

| Group | Endpoints |
|---|---|
| Auth | `POST /auth/register`, `POST /auth/login` |
| Tasks | `GET/POST /tasks/`, `GET/PUT/DELETE /tasks/{id}` |
| Task actions | `POST /tasks/{id}/assign\|submit\|approve\|reject\|cancel` |
| Tags | `GET/POST /tasks/tags`, `DELETE /tasks/tags/{id}` |
| Categories | `GET/POST /tasks/categories`, `DELETE /tasks/categories/{id}` |
| Comments | `GET/POST /tasks/{id}/comments`, `DELETE /tasks/{id}/comments/{id}` |
| Users | `GET /users/me`, `PUT /users/me`, `GET /users/{id}` |
| Wallet | `GET /wallet/me`, `POST /wallet/deposit`, `GET /wallet/transactions` |

Interactive docs: `http://localhost:8000/docs`