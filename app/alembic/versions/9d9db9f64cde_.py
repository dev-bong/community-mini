"""empty message

Revision ID: 9d9db9f64cde
Revises: c4dd07b87ca8
Create Date: 2024-08-03 22:35:21.480288

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9d9db9f64cde"
down_revision: Union[str, None] = "c4dd07b87ca8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "full_name", existing_type=sa.VARCHAR(length=30), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "full_name", existing_type=sa.VARCHAR(length=30), nullable=True
    )
    # ### end Alembic commands ###
