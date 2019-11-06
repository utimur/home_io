'''change device id to uuid and remove device_type field

Revision ID: 4d6d50fa6cf8
Revises: f3f6dff48664
Create Date: 2019-11-02 13:04:39.031560

'''
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import UUIDType

revision = '4d6d50fa6cf8'
down_revision = 'f3f6dff48664'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('device', sa.Column('uuid', UUIDType(), nullable=False))
    op.drop_constraint('device_id_key', 'device', type_='unique')
    op.drop_constraint('device_id_key1', 'device', type_='unique')
    op.drop_constraint('device_id_key2', 'device', type_='unique')
    op.drop_constraint('device_log_device_id_fkey', 'device_log', type_='foreignkey')
    op.drop_constraint('device_task_device_id_fkey', 'device_task', type_='foreignkey')
    op.drop_column('device', 'device_type')
    op.drop_column('device', 'id')
    op.create_unique_constraint(None, 'device', ['uuid'])
    op.create_foreign_key(None, 'device_log', 'device', ['device_id'], ['uuid'], ondelete='CASCADE')
    op.create_foreign_key(None, 'device_task', 'device', ['device_id'], ['uuid'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint(None, 'device_task', type_='foreignkey')
    op.create_foreign_key('device_task_device_id_fkey', 'device_task', 'device', ['device_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'device_log', type_='foreignkey')
    op.create_foreign_key('device_log_device_id_fkey', 'device_log', 'device', ['device_id'], ['id'], ondelete='CASCADE')
    op.add_column('device', sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.add_column('device', sa.Column('device_type', postgresql.ENUM('humidity_sensor', 'blinker', 'rangefinder', name='typeenum'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'device', type_='unique')
    op.create_unique_constraint('device_id_key2', 'device', ['id'])
    op.create_unique_constraint('device_id_key1', 'device', ['id'])
    op.create_unique_constraint('device_id_key', 'device', ['id'])
    op.drop_column('device', 'uuid')
