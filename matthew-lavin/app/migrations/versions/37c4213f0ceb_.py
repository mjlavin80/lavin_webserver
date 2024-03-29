"""empty message

Revision ID: 37c4213f0ceb
Revises: 
Create Date: 2018-12-14 22:30:26.154156

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '37c4213f0ceb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('blog_post', 'post_path',
               existing_type=mysql.VARCHAR(length=512),
               nullable=True)
    op.alter_column('blog_post', 'public',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.alter_column('tag', 'public',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.alter_column('tag', 'tag_path',
               existing_type=mysql.VARCHAR(length=500),
               nullable=True)
    op.alter_column('user_profile', 'custom_blog_path',
               existing_type=mysql.VARCHAR(length=512),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_profile', 'custom_blog_path',
               existing_type=mysql.VARCHAR(length=512),
               nullable=False)
    op.alter_column('tag', 'tag_path',
               existing_type=mysql.VARCHAR(length=500),
               nullable=False)
    op.alter_column('tag', 'public',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.alter_column('blog_post', 'public',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.alter_column('blog_post', 'post_path',
               existing_type=mysql.VARCHAR(length=512),
               nullable=False)
    # ### end Alembic commands ###
