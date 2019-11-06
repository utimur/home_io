'''fix constraint issue

Revision ID: 5539359db16b
Revises: db6a841c4ac2
Create Date: 2019-10-09 19:27:02.922711

'''
from alembic import op

revision = '5539359db16b'
down_revision = 'db6a841c4ac2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'device', ['id'])
    op.create_unique_constraint(None, 'device_log', ['id'])
    op.create_unique_constraint(None, 'device_task', ['id'])


def downgrade():
    op.drop_constraint(None, 'device_task', type_='unique')
    op.drop_constraint(None, 'device_log', type_='unique')
    op.drop_constraint(None, 'device', type_='unique')
