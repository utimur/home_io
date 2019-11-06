'''add script model

Revision ID: f3f6dff48664
Revises: 6468651f0dfa
Create Date: 2019-10-31 20:16:22.140316

'''
import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import ArrowType

revision = 'f3f6dff48664'
down_revision = '6468651f0dfa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('script',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=False),
    sa.Column('src_path', sa.String(length=4096), nullable=False),
    sa.Column('calls', sa.Integer(), nullable=True),
    sa.Column('runtime', sa.Integer(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.Column('updated_at', ArrowType(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_script_id'), 'script', ['id'], unique=False)
    op.create_unique_constraint(None, 'device', ['id'])
    op.create_unique_constraint(None, 'device_log', ['id'])
    op.create_unique_constraint(None, 'device_task', ['id'])


def downgrade():
    op.drop_constraint(None, 'device_task', type_='unique')
    op.drop_constraint(None, 'device_log', type_='unique')
    op.drop_constraint(None, 'device', type_='unique')
    op.drop_index(op.f('ix_script_id'), table_name='script')
    op.drop_table('script')
