"""Track pending captures and refunds for safe provider reconciliation."""

from alembic import op
import sqlalchemy as sa


revision = "0010_payment_action_recovery"
down_revision = "0009_add_user_names"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("orders", sa.Column("refund_id", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("capture_request_id", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("refund_request_id", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("payment_action_started_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("orders", "payment_action_started_at")
    op.drop_column("orders", "refund_request_id")
    op.drop_column("orders", "capture_request_id")
    op.drop_column("orders", "refund_id")
