"""add user table

Revision ID: f74ed83bf32f
Revises: 5720c7d98e94
Create Date: 2022-02-18 18:07:08.529062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74ed83bf32f'
down_revision = '5720c7d98e94'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
    sa.Column("id",sa.Integer,unique=True, primary_key=True, index=True , nullable= False),
    sa.Column("email",sa.String,unique=True, index=True ,nullable=False),
    sa.Column("username",sa.String,unique=True ,index=True,nullable=False),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
    sa.Column("password",sa.String,nullable=False)
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
