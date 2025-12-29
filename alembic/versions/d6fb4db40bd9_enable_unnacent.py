"""enable unnacent

Revision ID: d6fb4db40bd9
Revises: 8ec26313c8d7
Create Date: 2025-12-29 13:45:17.703629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6fb4db40bd9'
down_revision: Union[str, Sequence[str], None] = '8ec26313c8d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Habilita a extensão unaccent
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")


def downgrade() -> None:
    # Desabilita a extensão
    op.execute("DROP EXTENSION IF EXISTS unaccent;")