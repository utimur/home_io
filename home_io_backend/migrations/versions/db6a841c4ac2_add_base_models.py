'''add base models

Revision ID: db6a841c4ac2
Revises:
Create Date: 2019-10-05 12:18:33.101643

'''
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


revision = 'db6a841c4ac2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('_password_hash', sa.Binary(), nullable=False),
    sa.Column('created_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('device',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('registred_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.Column('device_type', sa.Enum('humidity_sensor', 'blinker', 'rangefinder', name='typeenum'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('device_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('log', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('created_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.Column('device_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_device_log_created_at'), 'device_log', ['created_at'], unique=False)
    op.create_table('device_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_id', sqlalchemy_utils.types.uuid.UUIDType, nullable=False),
    sa.Column('task', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('created_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )


def downgrade():
    op.drop_table('device_task')
    op.drop_index(op.f('ix_device_log_created_at'), table_name='device_log')
    op.drop_table('device_log')
    op.drop_table('device')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
