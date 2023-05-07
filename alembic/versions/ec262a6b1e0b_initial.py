"""initial

Revision ID: ec262a6b1e0b
Revises:
Create Date: 2023-03-30 03:08:50.408928

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ec262a6b1e0b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
