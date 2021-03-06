"""Added user_likes table, updated post and user tables

Revision ID: 02c8fcf8b221
Revises: 9c74095d9532
Create Date: 2022-07-20 19:23:27.259300

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '02c8fcf8b221'
down_revision = '9c74095d9532'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id', 'user_id', 'post_id'),
                    sa.UniqueConstraint('user_id', 'post_id')
                    )
    op.create_index(op.f('ix_like_id'), 'like', ['id'], unique=False)
    op.alter_column('user', 'access_token_expires',
                    existing_type=postgresql.TIMESTAMP(),
                    type_=sa.DateTime(timezone=True),
                    existing_nullable=True)
    op.alter_column('user', 'refresh_token_expires',
                    existing_type=postgresql.TIMESTAMP(),
                    type_=sa.DateTime(timezone=True),
                    existing_nullable=True)
    op.create_unique_constraint('user_access_token_key', 'user', ['access_token'])
    op.create_unique_constraint('user_refresh_token_key', 'user', ['refresh_token'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_access_token_key', 'user', type_='unique')
    op.drop_constraint('user_refresh_token_key', 'user', type_='unique')
    op.alter_column('user', 'refresh_token_expires',
                    existing_type=sa.DateTime(timezone=True),
                    type_=postgresql.TIMESTAMP(),
                    existing_nullable=True)
    op.alter_column('user', 'access_token_expires',
                    existing_type=sa.DateTime(timezone=True),
                    type_=postgresql.TIMESTAMP(),
                    existing_nullable=True)
    op.drop_index(op.f('ix_like_id'), table_name='like')
    op.drop_table('like')
    # ### end Alembic commands ###
