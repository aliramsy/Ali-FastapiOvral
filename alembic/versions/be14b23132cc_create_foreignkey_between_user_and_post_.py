"""create foreignkey between user and post table

Revision ID: be14b23132cc
Revises: f74ed83bf32f
Create Date: 2022-02-18 18:35:49.902735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be14b23132cc'
down_revision = 'f74ed83bf32f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
    sa.Column("owner_id",sa.Integer,nullable=False)
    )
    pass


def downgrade():
    op.drop_column("posts", "owner_id")
    pass
