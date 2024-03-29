"""empty message

Revision ID: b6c14a0b384d
Revises: 
Create Date: 2019-09-15 00:24:01.100225

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'b6c14a0b384d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('creation_time', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'creation_time')
    # ### end Alembic commands ###
