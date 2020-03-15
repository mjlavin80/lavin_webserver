"""empty message

Revision ID: 2df0fd1a1b48
Revises: 645a146ab428
Create Date: 2020-02-21 12:03:14.712452

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2df0fd1a1b48'
down_revision = '645a146ab428'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('extracted_parsed', 'reviewed_author_name',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_author_viaf_match',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_genre',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_price',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_pub_date',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_publisher',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_publisher_viaf_match',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_title',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('review', 'perceived_author_gender',
               existing_type=mysql.VARCHAR(length=99),
               type_=sa.String(length=128),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_author_name',
               existing_type=mysql.VARCHAR(length=99),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_genre',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_price',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_pub_date',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_publisher',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_title',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('user_profile', 'approved',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('user_profile', 'authenticated',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('user_profile', 'is_admin',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_profile', 'is_admin',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('user_profile', 'authenticated',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('user_profile', 'approved',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_title',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_publisher',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_pub_date',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_price',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_book_genre',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('review', 'reviewed_author_name',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=99),
               existing_nullable=True)
    op.alter_column('review', 'perceived_author_gender',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=99),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_title',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_publisher_viaf_match',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_publisher',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_pub_date',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_price',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_book_genre',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_author_viaf_match',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    op.alter_column('extracted_parsed', 'reviewed_author_name',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=True)
    # ### end Alembic commands ###
