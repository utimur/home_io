'''fix typo in word registered

Revision ID: 6468651f0dfa
Revises: 5539359db16b
Create Date: 2019-10-25 21:37:35.488267

'''
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import ArrowType

revision = '6468651f0dfa'
down_revision = '5539359db16b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('device', sa.Column('registered_at', ArrowType(), nullable=True))
    op.create_unique_constraint(None, 'device', ['id'])
    op.drop_column('device', 'registred_at')
    op.create_unique_constraint(None, 'device_log', ['id'])
    op.create_unique_constraint(None, 'device_task', ['id'])


def downgrade():
    op.drop_constraint(None, 'device_task', type_='unique')
    op.drop_constraint(None, 'device_log', type_='unique')
    op.add_column('device', sa.Column('registred_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'device', type_='unique')
    op.drop_column('device', 'registered_at')
