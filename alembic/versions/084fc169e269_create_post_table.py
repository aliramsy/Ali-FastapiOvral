"""create post table

Revision ID: 084fc169e269
Revises: 
Create Date: 2022-02-18 16:58:37.517873

"""
from ast import Index
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '084fc169e269'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
    sa.Column("id",sa.Integer,primary_key=True,index=True,nullable=False),
    sa.Column("title",sa.String,index=True,nullable=False),
    sa.Column("content",sa.String,index=True,nullable=False)    
    )
    pass

def downgrade():
    op.drop_table("posts")
    pass