"""alterado nome col usuario-grupo

Revision ID: 8c6362ad371a
Revises: be2370634419
Create Date: 2026-01-12 20:11:54.922645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c6362ad371a'
down_revision: Union[str, Sequence[str], None] = 'be2370634419'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Renomeia a coluna existente (Preserva os dados!)
    # No PostgreSQL/Alembic, usamos alter_column com new_column_name
    op.alter_column('usuarios', 'grupo_id', new_column_name='grupo_familiar_id')

    # 2. Remove a constraint antiga (que estava vinculada ao nome antigo)
    # Nota: O nome da constraint pode variar, certifique-se que é 'usuarios_grupo_id_fkey'
    op.drop_constraint('usuarios_grupo_id_fkey', 'usuarios', type_='foreignkey')

    # 3. Cria a nova constraint vinculada ao novo nome da coluna
    op.create_foreign_key(
        'usuarios_grupo_familiar_id_fkey', # Nome da nova FK
        'usuarios', 'grupos_familiares', 
        ['grupo_familiar_id'], ['id'], 
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # 1. Volta o nome da coluna para o original
    op.alter_column('usuarios', 'grupo_familiar_id', new_column_name='grupo_id')

    # 2. Remove a constraint do nome novo
    op.drop_constraint('usuarios_grupo_familiar_id_fkey', 'usuarios', type_='foreignkey')

    # 3. Recria a constraint com o nome original
    op.create_foreign_key(
        'usuarios_grupo_id_fkey', 
        'usuarios', 'grupos_familiares', 
        ['grupo_id'], ['id'], 
        ondelete='SET NULL'
    )