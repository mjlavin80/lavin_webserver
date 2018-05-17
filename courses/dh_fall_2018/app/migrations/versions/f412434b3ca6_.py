"""empty message

Revision ID: f412434b3ca6
Revises: d24eddc5e40d
Create Date: 2017-07-04 14:36:27.792045

"""

# revision identifiers, used by Alembic.
revision = 'f412434b3ca6'
down_revision = 'd24eddc5e40d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'activity', 'users', ['user_id'], ['id'])
    op.add_column('assignment', sa.Column('public', sa.String(length=128), nullable=True))
    op.add_column('assignment', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'assignment', 'users', ['user_id'], ['id'])
    op.add_column('basics', sa.Column('public', sa.String(length=128), nullable=True))
    op.add_column('basics', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'basics', 'users', ['user_id'], ['id'])
    op.add_column('collection', sa.Column('order', sa.String(length=100), nullable=True))
    op.add_column('collection', sa.Column('public', sa.String(length=128), nullable=True))
    op.add_column('collection', sa.Column('target_id', sa.Integer(), nullable=True))
    op.add_column('collection', sa.Column('target_table', sa.String(length=200), nullable=True))
    op.add_column('policy', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'policy', 'users', ['user_id'], ['id'])
    op.add_column('reading', sa.Column('public', sa.String(length=128), nullable=True))
    op.add_column('reading', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reading', 'users', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reading', type_='foreignkey')
    op.drop_column('reading', 'user_id')
    op.drop_column('reading', 'public')
    op.drop_constraint(None, 'policy', type_='foreignkey')
    op.drop_column('policy', 'user_id')
    op.drop_column('collection', 'target_table')
    op.drop_column('collection', 'target_id')
    op.drop_column('collection', 'public')
    op.drop_column('collection', 'order')
    op.drop_constraint(None, 'basics', type_='foreignkey')
    op.drop_column('basics', 'user_id')
    op.drop_column('basics', 'public')
    op.drop_constraint(None, 'assignment', type_='foreignkey')
    op.drop_column('assignment', 'user_id')
    op.drop_column('assignment', 'public')
    op.drop_constraint(None, 'activity', type_='foreignkey')
    op.drop_column('activity', 'user_id')
    ### end Alembic commands ###
