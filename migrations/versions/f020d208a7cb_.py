"""empty message

Revision ID: f020d208a7cb
Revises: 1c4300174377
Create Date: 2019-10-19 22:08:39.670172

"""
from alembic import op
import sqlalchemy as sa
import ormtypes
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f020d208a7cb'
down_revision = '1c4300174377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submissions', sa.Column('extra_compile_parameter', sa.String(length=128), nullable=False))
    op.drop_column('submissions', 'extra_compile_argument')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submissions', sa.Column('extra_compile_argument', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('submissions', 'extra_compile_parameter')
    # ### end Alembic commands ###
