"""empty message

Revision ID: 1c4300174377
Revises: eba6b07807ed
Create Date: 2019-10-19 22:03:50.711220

"""
from alembic import op
import sqlalchemy as sa
import ormtypes


# revision identifiers, used by Alembic.
revision = '1c4300174377'
down_revision = 'eba6b07807ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submissions', sa.Column('extra_compile_argument', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submissions', 'extra_compile_argument')
    # ### end Alembic commands ###
