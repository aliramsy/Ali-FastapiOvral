"""adding foreign keys to like table

Revision ID: 39d9c08fc8a8
Revises: da1a225375b8
Create Date: 2022-02-18 19:18:53.844751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39d9c08fc8a8'
down_revision = 'da1a225375b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key("like_post_fk", source_table="likes", referent_table="posts", local_cols=["post_id"], remote_cols=["id"], ondelete="CASCADE")
    op.create_foreign_key("like_user_fk", source_table="likes", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("like_post_fk", table_name="likes")
    op.drop_constraint("like_user_fk", table_name="likes")
    pass
