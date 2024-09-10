"""Add id column and remove number column from classes table

Revision ID: 162b3ffbaeba
Revises: 
Create Date: 2024-08-26 22:57:50.744446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = '162b3ffbaeba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)

    # Find the foreign key constraint on the 'courses' table that references 'classes.number'
    fk_constraints = inspector.get_foreign_keys('courses')
    for fk in fk_constraints:
        if 'classes.number' in fk['referred_columns']:
            constraint_name = fk['name']
            op.drop_constraint(constraint_name, 'courses', type_='foreignkey')
            break

    # Drop the 'number' column from the 'classes' table
    op.drop_column('classes', 'number')

    # Add the 'id' column to the 'classes' table and set it as the primary key
    op.add_column('classes', sa.Column('id', sa.Integer(), nullable=False))
    op.create_primary_key('pk_classes_id', 'classes', ['id'])

    # Add 'class_id' to 'courses' to reference 'classes.id'
    op.add_column('courses', sa.Column('class_id', sa.Integer(), sa.ForeignKey('classes.id')))
    op.create_foreign_key('fk_courses_class_id', 'courses', 'classes', ['class_id'], ['id'])

def downgrade() -> None:
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)

    # Find the foreign key constraint on the 'courses' table that references 'classes.id'
    fk_constraints = inspector.get_foreign_keys('courses')
    for fk in fk_constraints:
        if 'classes.id' in fk['referred_columns']:
            constraint_name = fk['name']
            op.drop_constraint(constraint_name, 'courses', type_='foreignkey')
            break

    # Re-add the 'number' column to the 'classes' table
    op.add_column('classes', sa.Column('number', sa.Integer(), autoincrement=True, nullable=False))
    op.create_primary_key('pk_classes_number', 'classes', ['number'])

    # Remove 'class_id' from 'courses' and re-add 'class_num' to reference 'classes.number'
    op.drop_column('courses', 'class_id')
    op.add_column('courses', sa.Column('class_num', sa.Integer(), sa.ForeignKey('classes.number')))
    op.create_foreign_key('fk_courses_class_num', 'courses', 'classes', ['class_num'], ['number'])