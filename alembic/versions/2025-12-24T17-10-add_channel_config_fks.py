"""Add FKs to channel_configs for channel and updater."""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "add_channel_config_fks"
down_revision: Union[str, None] = "2bf89298285e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns (nullable to avoid failures if data exists)
    op.add_column(
        "channel_configs",
        sa.Column("channel_id", sa.dialects.postgresql.UUID(), nullable=True),
    )
    op.add_column(
        "channel_configs",
        sa.Column("updated_by_id", sa.dialects.postgresql.UUID(), nullable=True),
    )

    # One-to-one to channels (unique) and FK to users for updated_by
    op.create_unique_constraint(
        "uq_channel_configs_channel_id", "channel_configs", ["channel_id"]
    )
    op.create_foreign_key(
        "fk_channel_configs_channel_id_channels",
        "channel_configs",
        "channels",
        ["channel_id"],
        ["uuid"],
    )
    op.create_foreign_key(
        "fk_channel_configs_updated_by_id_users",
        "channel_configs",
        "users",
        ["updated_by_id"],
        ["uuid"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_channel_configs_updated_by_id_users", "channel_configs", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_channel_configs_channel_id_channels", "channel_configs", type_="foreignkey"
    )
    op.drop_constraint("uq_channel_configs_channel_id", "channel_configs", type_="unique")
    op.drop_column("channel_configs", "updated_by_id")
    op.drop_column("channel_configs", "channel_id")
