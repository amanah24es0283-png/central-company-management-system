from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "50c07565c8c6"
down_revision = "85a7239c7efa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    companies_columns = {c["name"] for c in inspector.get_columns("companies")}
    branches_columns = {c["name"] for c in inspector.get_columns("branches")}

    if "uuid" not in companies_columns:
        op.add_column(
            "companies",
            sa.Column(
                "uuid",
                sa.UUID(),
                nullable=False,
                server_default=sa.text("gen_random_uuid()"),
            ),
        )

    if "uuid" not in branches_columns:
        op.add_column(
            "branches",
            sa.Column(
                "uuid",
                sa.UUID(),
                nullable=False,
                server_default=sa.text("gen_random_uuid()"),
            ),
        )

    indexes = {i["name"] for i in inspector.get_indexes("companies")}
    if "ix_companies_uuid" not in indexes:
        op.create_index("ix_companies_uuid", "companies", ["uuid"], unique=True)

    indexes = {i["name"] for i in inspector.get_indexes("branches")}
    if "ix_branches_uuid" not in indexes:
        op.create_index("ix_branches_uuid", "branches", ["uuid"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_branches_uuid", table_name="branches")
    op.drop_index("ix_companies_uuid", table_name="companies")
    op.drop_column("branches", "uuid")
    op.drop_column("companies", "uuid")
