"""create posts table

Revision ID: 16b7814852cb
Create Date: 2022-07-11 19:22:31.098489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16b7814852cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    #we are only creating two columns 
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
