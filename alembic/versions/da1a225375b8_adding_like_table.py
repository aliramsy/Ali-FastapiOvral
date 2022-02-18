"""adding like table

Revision ID: da1a225375b8
Revises: 88022ec12865
Create Date: 2022-02-18 19:14:24.083166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da1a225375b8'
down_revision = '88022ec12865'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("likes",
    sa.Column("post_id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("user_id", sa.Integer, primary_key=True, nullable=False)
    )
    pass


def downgrade():
    op.drop_table("likes")
    pass
