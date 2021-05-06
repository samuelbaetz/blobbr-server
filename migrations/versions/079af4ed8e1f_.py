"""empty message

Revision ID: 079af4ed8e1f
Revises: eaaa37d76f7e
Create Date: 2021-04-21 18:24:17.101579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '079af4ed8e1f'
down_revision = 'eaaa37d76f7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('likes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'likes')
    # ### end Alembic commands ###