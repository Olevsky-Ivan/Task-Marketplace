import os
from alembic import op
from passlib.context import CryptContext
from typing import Sequence, Union

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

revision: str = "861b5ea35631"
down_revision: Union[str, Sequence[str], None] = "1d67890c1cea"
branch_labels = None
depends_on = None


def upgrade():
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_PASSWORD"]

    op.execute(f"""
        INSERT INTO users (email, hashed_password, role, created_at)
        VALUES (
            '{email}',
            '{pwd_context.hash(password)}',
            'ADMIN',
            NOW()
        )
        ON CONFLICT (email) DO NOTHING
        """)


def downgrade():
    op.execute("DELETE FROM users WHERE role='admin'")
