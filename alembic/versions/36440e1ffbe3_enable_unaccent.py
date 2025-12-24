"""enable_unaccent

Revision ID: 36440e1ffbe3
Revises: 8818a8f52d7c
Create Date: 2025-12-24 10:16:27.007355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36440e1ffbe3'
down_revision: Union[str, Sequence[str], None] = '8818a8f52d7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Habilita a extensão unaccent
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")


def downgrade() -> None:
    # Desabilita a extensão
    op.execute("DROP EXTENSION IF EXISTS unaccent;")
