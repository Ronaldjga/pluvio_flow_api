# Importe TODOS os models para que se registrem no Base.metadata
from app.models.user import User
from app.models.occurrence import Occurrence
# ... todos os outros

__all__ = ["User", "Occurrence"]