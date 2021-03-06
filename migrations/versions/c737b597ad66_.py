"""empty message

Revision ID: c737b597ad66
Revises: 
Create Date: 2020-02-14 23:50:41.095661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c737b597ad66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doctor',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('lastname', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('cedula', sa.String(length=80), nullable=False),
    sa.Column('phone', sa.String(length=80), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('certificado', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cedula'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('paciente',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('lastname', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('cedula', sa.String(length=80), nullable=False),
    sa.Column('phone', sa.String(length=80), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cedula'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('tratamiento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tratamiento_name', sa.String(length=125), nullable=False),
    sa.Column('descripcion', sa.String(length=500), nullable=True),
    sa.Column('price', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descripcion'),
    sa.UniqueConstraint('tratamiento_name')
    )
    op.create_table('cita',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('state', sa.Boolean(), nullable=True),
    sa.Column('price_tot', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['paciente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cita')
    op.drop_table('tratamiento')
    op.drop_table('paciente')
    op.drop_table('doctor')
    # ### end Alembic commands ###
