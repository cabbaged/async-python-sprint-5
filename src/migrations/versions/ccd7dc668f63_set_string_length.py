"""set_string_length

Revision ID: ccd7dc668f63
Revises: 893e1bfab57d
Create Date: 2024-04-11 18:45:06.181182

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ccd7dc668f63'
down_revision: Union[str, None] = '893e1bfab57d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_link_created_at', table_name='link')
    op.drop_table('link')
    op.alter_column('file', 'path',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('file', 'path',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_table('link',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('full_url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('shortened_url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('usages', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('last_usage', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='link_pkey'),
    sa.UniqueConstraint('full_url', name='link_full_url_key'),
    sa.UniqueConstraint('shortened_url', name='link_shortened_url_key')
    )
    op.create_index('ix_link_created_at', 'link', ['created_at'], unique=False)
    # ### end Alembic commands ###
