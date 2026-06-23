# Task Marketplace API

Backend REST API for the freelance task platform.  
Users can create tasks, execute them, leave comments and manage the balance through the wallet system.

---

## Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL
- **Validation:** Pydantic v2
- **Auth:** JWT (python-jose)
- **Password hashing:** Passlib + bcrypt
- **Server:** Uvicorn
- **Migrations:** Alembic

---

## Architecture


app/
│
├── main.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── deps.py
│
├── database/
│   ├── base.py
│   └── session.py
│
├── models/
│   ├── user.py
│   ├── wallet.py
│   ├── task.py
│   ├── comment.py
│   ├── category.py
│   ├── transaction.py
│   └── attachment.py
│
├── auth/
│   ├── router.py
│   ├── service.py
│   └── schemas.py
│
├── users/
│   ├── router.py
│   ├── service.py
│   ├── repository.py
│   └── schemas.py
│
├── tasks/
│   ├── router.py
│   ├── service.py
│   ├── repository.py
│   └── schemas.py
│
└── repositories/
    └── base.py