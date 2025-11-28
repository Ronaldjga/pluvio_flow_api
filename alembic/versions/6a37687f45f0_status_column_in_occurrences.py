from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6a37687f45f0'
down_revision = 'a15d18326b75'
branch_labels = None
depends_on = None


def upgrade():
    # Criar o ENUM no PostgreSQL
    op.execute("CREATE TYPE occurrence_status AS ENUM ('ativa', 'pendente', 'resolvida');")

    # Adicionar a coluna usando o tipo recém-criado
    op.add_column(
        'occurrences',
        sa.Column('status', sa.Enum('ativa', 'pendente', 'resolvida', name='occurrence_status'), nullable=False, server_default='pendente')
    )

    # Remover o default para futuras inserções ficarem sob controle da aplicação
    op.alter_column('occurrences', 'status', server_default=None)


def downgrade():
    # Remover coluna
    op.drop_column('occurrences', 'status')

    # Remover o tipo ENUM
    op.execute("DROP TYPE occurrence_status;")
