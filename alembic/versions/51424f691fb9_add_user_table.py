"""add user table

Revision ID: 51424f691fb9
Revises: 4ffff66ec21c
Create Date: 2022-07-11 19:30:50.141896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51424f691fb9'
down_revision = '4ffff66ec21c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
