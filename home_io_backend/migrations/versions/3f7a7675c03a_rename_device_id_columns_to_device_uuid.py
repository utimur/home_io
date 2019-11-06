'''rename device_id columns to device_uuid

Revision ID: 3f7a7675c03a
Revises: 4d6d50fa6cf8
Create Date: 2019-11-02 13:26:24.382201

'''
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import UUIDType

revision = '3f7a7675c03a'
down_revision = '4d6d50fa6cf8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'device', ['uuid'])
    op.add_column('device_log', sa.Column('device_uuid', UUIDType(), nullable=False))
    op.create_unique_constraint(None, 'device_log', ['id'])
    op.drop_constraint('device_log_device_id_fkey', 'device_log', type_='foreignkey')
    op.create_foreign_key(None, 'device_log', 'device', ['device_uuid'], ['uuid'], ondelete='CASCADE')
    op.drop_column('device_log', 'device_id')
    op.add_column('device_task', sa.Column('device_uuid', UUIDType(), nullable=False))
    op.create_unique_constraint(None, 'device_task', ['id'])
    op.drop_constraint('device_task_device_id_fkey', 'device_task', type_='foreignkey')
    op.create_foreign_key(None, 'device_task', 'device', ['device_uuid'], ['uuid'], ondelete='CASCADE')
    op.drop_column('device_task', 'device_id')


def downgrade():
    op.add_column('device_task', sa.Column('device_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'device_task', type_='foreignkey')
    op.create_foreign_key('device_task_device_id_fkey', 'device_task', 'device', ['device_id'], ['uuid'], ondelete='CASCADE')
    op.drop_constraint(None, 'device_task', type_='unique')
    op.drop_column('device_task', 'device_uuid')
    op.add_column('device_log', sa.Column('device_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'device_log', type_='foreignkey')
    op.create_foreign_key('device_log_device_id_fkey', 'device_log', 'device', ['device_id'], ['uuid'], ondelete='CASCADE')
    op.drop_constraint(None, 'device_log', type_='unique')
    op.drop_column('device_log', 'device_uuid')
    op.drop_constraint(None, 'device', type_='unique')
