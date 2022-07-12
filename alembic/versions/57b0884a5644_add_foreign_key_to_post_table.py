"""add foreign key to post table

Revision ID: 57b0884a5644
Revises: 51424f691fb9
Create Date: 2022-07-11 19:44:31.505600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57b0884a5644'
down_revision = '51424f691fb9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
