"""empty message

Revision ID: 3db1e89c53fb
Revises: 1cf90a453c8e
Create Date: 2016-12-24 20:00:33.634026

"""

# revision identifiers, used by Alembic.
revision = '3db1e89c53fb'
down_revision = '1cf90a453c8e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('order', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity', 'order')
    ### end Alembic commands ###
