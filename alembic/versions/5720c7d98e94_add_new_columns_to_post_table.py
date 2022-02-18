"""add new columns to post table

Revision ID: 5720c7d98e94
Revises: 084fc169e269
Create Date: 2022-02-18 17:37:43.691657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5720c7d98e94'
down_revision = '084fc169e269'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_column("posts","created_at")
    pass
