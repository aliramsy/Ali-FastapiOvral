"""add published column to post table

Revision ID: 88022ec12865
Revises: a83b0c950f18
Create Date: 2022-02-18 19:10:45.731031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88022ec12865'
down_revision = 'a83b0c950f18'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
    sa.Column("published",sa.Boolean, server_default='True',nullable=False)
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    pass
