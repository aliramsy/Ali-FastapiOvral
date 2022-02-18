"""create foreing key2

Revision ID: a83b0c950f18
Revises: be14b23132cc
Create Date: 2022-02-18 18:57:59.708631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a83b0c950f18'
down_revision = 'be14b23132cc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key("post_user_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_user_fk", table_name="posts")
    pass
