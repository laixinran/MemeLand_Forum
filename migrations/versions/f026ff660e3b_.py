"""empty message

Revision ID: f026ff660e3b
Revises: e6b5ab6ff6fe
Create Date: 2024-07-06 21:22:37.530657

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f026ff660e3b'
down_revision = 'e6b5ab6ff6fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('comments_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'posts', ['post_id'], ['id'])
        batch_op.drop_column('comment_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('comments_ibfk_2', 'posts', ['comment_id'], ['id'])
        batch_op.drop_column('post_id')

    # ### end Alembic commands ###