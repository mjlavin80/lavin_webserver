"""empty message

Revision ID: 7f477f1edc3e
Revises: 8e91a78bafcc
Create Date: 2021-08-25 13:44:38.820321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f477f1edc3e'
down_revision = '8e91a78bafcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('syllabus', sa.Column('course_name', sa.String(length=1024), nullable=False))
    op.add_column('syllabus', sa.Column('current', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('syllabus', 'current')
    op.drop_column('syllabus', 'course_name')
    # ### end Alembic commands ###
