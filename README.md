Task Marketplace API (FastAPI)

A backend system for a task marketplace built with FastAPI, SQLAlchemy, and JWT authentication. The project provides user registration, authentication, and protected endpoints with role-based structure.

Tech Stack
FastAPI
SQLAlchemy (ORM)
PostgreSQL
Pydantic
JWT (python-jose)
Passlib (bcrypt)
Uvicorn


app/
│
├── main.py              # Application entry point
│
├── api/
│   └── auth.py         # Authentication routes (login/register)
│
├── core/
│   ├── config.py       # Environment settings
│   ├── security.py     # JWT + password hashing logic
│   └── deps.py         # Dependencies (DB session, auth)
│
├── database/
│   └── session.py      # SQLAlchemy engine and session setup
│
├── models/
│   ├── user.py         # User model
│   ├── wallet.py       # Wallet model
│   ├── task.py         # Task model
│   └── comment.py      # Comment model



Database Models:

User

Represents system users.

Fields:

id — primary key
email — unique user email
hashed_password — hashed password (bcrypt)
role — user role (e.g. executor, admin)
created_at — timestamp of creation

Relationships:

wallet → one-to-one or one-to-many
tasks (as creator or executor)
comments


Wallet

Represents a user's balance.

Fields:

id
balance — numeric balance
user_id — foreign key to User

Relationship:

Belongs to User


Task

Represents a marketplace task.

Fields:

id
title
description
status (new / in_progress / done)
price
creator_id — FK to User
executor_id — FK to User (optional)

Relationships:

Created by User
Assigned to User
Has many comments


Comment

Represents task comments.

Fields:

id
text
task_id — FK to Task
user_id — FK to User
created_at

Relationships:

Belongs to Task
Belongs to User