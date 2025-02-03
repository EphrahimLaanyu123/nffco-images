"""Initial migration

Revision ID: 2af5b6a8e8c0
Revises: ba59dd30e023
Create Date: 2025-02-03 08:50:34.865713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2af5b6a8e8c0'
down_revision = 'ba59dd30e023'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_data', sa.LargeBinary(), nullable=False))
        def upgrade():
    # Other upgrade steps
        batch_op.add_column(sa.Column('file_data', sa.LargeBinary(), nullable=False))


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_column('file_data')

    # ### end Alembic commands ###
