"""Migrate2

Revision ID: e42a2e15c504
Revises: f90ad2865da5
Create Date: 2023-04-05 21:34:03.778506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e42a2e15c504'
down_revision = 'f90ad2865da5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'login_histories', ['id'], schema='auth')
    op.create_unique_constraint(None, 'roles', ['id'], schema='auth')
    op.create_unique_constraint(None, 'user_roles', ['id'], schema='auth')
    op.create_unique_constraint(None, 'users', ['id'], schema='auth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', schema='auth', type_='unique')
    op.drop_constraint(None, 'user_roles', schema='auth', type_='unique')
    op.drop_constraint(None, 'roles', schema='auth', type_='unique')
    op.drop_constraint(None, 'login_histories', schema='auth', type_='unique')
    # ### end Alembic commands ###
