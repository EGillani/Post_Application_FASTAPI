"""changed email to username for security purposes

Revision ID: 16cb2c8c5eec
Revises: 11c22cbe062d
Create Date: 2022-08-07 16:32:30.434620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16cb2c8c5eec'
down_revision = '11c22cbe062d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'username')
    # ### end Alembic commands ###