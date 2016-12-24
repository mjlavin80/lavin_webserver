"""empty message

Revision ID: f694ab85897a
Revises: 083675052d82
Create Date: 2016-12-21 19:41:38.677721

"""

# revision identifiers, used by Alembic.
revision = 'f694ab85897a'
down_revision = '083675052d82'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('basics', sa.Column('hypoth', sa.String(length=500), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('basics', 'hypoth')
    ### end Alembic commands ###
