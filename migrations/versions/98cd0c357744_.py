"""empty message

Revision ID: 98cd0c357744
Revises: c039c132e00e
Create Date: 2021-01-03 10:07:48.874824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98cd0c357744'
down_revision = 'c039c132e00e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
