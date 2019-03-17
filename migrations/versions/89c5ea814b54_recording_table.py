"""recording table

Revision ID: 89c5ea814b54
Revises: 95f7b375ab29
Create Date: 2019-02-24 15:16:58.578350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c5ea814b54'
down_revision = '95f7b375ab29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recording',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('record_name', sa.String(length=80), nullable=True),
    sa.Column('label', sa.String(length=20), nullable=True),
    sa.Column('label_number', sa.String(length=20), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('cover', sa.Boolean(), nullable=True),
    sa.Column('word', sa.Boolean(), nullable=True),
    sa.Column('count_cassette', sa.Integer(), nullable=True),
    sa.Column('count_lp', sa.Integer(), nullable=True),
    sa.Column('count_45', sa.Integer(), nullable=True),
    sa.Column('count_78', sa.Integer(), nullable=True),
    sa.Column('count_cd', sa.Integer(), nullable=True),
    sa.Column('count_digital', sa.Integer(), nullable=True),
    sa.Column('count_copy_cassette', sa.Integer(), nullable=True),
    sa.Column('count_copy_cd', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recording_record_name'), 'recording', ['record_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_recording_record_name'), table_name='recording')
    op.drop_table('recording')
    # ### end Alembic commands ###
