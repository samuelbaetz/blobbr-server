"""empty message

Revision ID: eaaa37d76f7e
Revises: af8a3d569b88
Create Date: 2021-04-21 17:07:09.398424

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eaaa37d76f7e'
down_revision = 'af8a3d569b88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('content', sa.String(length=280), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###
