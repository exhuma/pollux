"""Create DB

Revision ID: 15f481a5a7d
Revises:
Create Date: 2015-07-13 08:04:53.155750

"""

# revision identifiers, used by Alembic.
revision = '15f481a5a7d'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


historical_data = {}  # XXX TODO


def upgrade():
    op.create_table(
        'pollen_concentration',
        sa.Column('date', sa.DateTime(timezone=True)),
        sa.Column('genus', sa.Unicode),
        sa.Column('concentration', sa.Integer)
    )


def downgrade():
    op.drop_table('pollen_concentration')
