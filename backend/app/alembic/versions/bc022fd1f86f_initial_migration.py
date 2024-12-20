"""Initial migration

Revision ID: bc022fd1f86f
Revises:
Create Date: 2024-11-29 23:09:04.633438

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bc022fd1f86f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "url",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("original_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("short_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_url_short_id"), "url", ["short_id"], unique=True)
    op.create_table(
        "hitstats",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("hits", sa.Integer(), nullable=False),
        sa.Column("url_id", sa.Uuid(), nullable=False),
        sa.Column("last_hit", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["url_id"],
            ["url.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("hitstats")
    op.drop_index(op.f("ix_url_short_id"), table_name="url")
    op.drop_table("url")
    # ### end Alembic commands ###
