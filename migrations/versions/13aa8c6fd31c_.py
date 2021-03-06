"""empty message

Revision ID: 13aa8c6fd31c
Revises: d3ed8f6bfb77
Create Date: 2021-05-06 14:42:45.404360

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '13aa8c6fd31c'
down_revision = 'd3ed8f6bfb77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_comments',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('comment_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'comment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_comments')
    # ### end Alembic commands ###
