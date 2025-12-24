"""Migrate channels.owner_id from BIGINT to UUID using users.telegram_id lookup."""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "facc64635826"
down_revision: Union[str, None] = "9bed1e128633"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    op.add_column("channels", sa.Column("owner_id_tmp", sa.UUID(), nullable=True))

    op.execute(
        sa.text(
            """
            UPDATE channels c
            SET owner_id_tmp = u.uuid
            FROM users u
            WHERE c.owner_id = u.telegram_id
            """
        )
    )

    unresolved = conn.execute(sa.text("SELECT count(*) FROM channels WHERE owner_id_tmp IS NULL"))
    unresolved_count = unresolved.scalar_one()
    if unresolved_count:
        raise RuntimeError(
            f"Cannot migrate channels.owner_id to UUID: {unresolved_count} rows had no matching users.telegram_id"
        )

    op.alter_column("channels", "owner_id_tmp", nullable=False)
    op.drop_column("channels", "owner_id")
    op.alter_column("channels", "owner_id_tmp", new_column_name="owner_id")
    op.create_foreign_key(
        "fk_channels_owner_id_users", "channels", "users", ["owner_id"], ["uuid"]
    )


def downgrade() -> None:
    conn = op.get_bind()

    op.drop_constraint("fk_channels_owner_id_users", "channels", type_="foreignkey")
    op.add_column("channels", sa.Column("owner_id_tmp", sa.BigInteger(), nullable=True))

    op.execute(
        sa.text(
            """
            UPDATE channels c
            SET owner_id_tmp = u.telegram_id
            FROM users u
            WHERE c.owner_id = u.uuid
            """
        )
    )

    unresolved = conn.execute(sa.text("SELECT count(*) FROM channels WHERE owner_id_tmp IS NULL"))
    unresolved_count = unresolved.scalar_one()
    if unresolved_count:
        raise RuntimeError(
            f"Cannot downgrade channels.owner_id to BIGINT: {unresolved_count} rows had no matching users.uuid"
        )

    op.alter_column("channels", "owner_id_tmp", nullable=False)
    op.drop_column("channels", "owner_id")
    op.alter_column("channels", "owner_id_tmp", new_column_name="owner_id")
