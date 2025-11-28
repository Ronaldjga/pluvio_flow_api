# Importe TODOS os models para que se registrem no Base.metadata
from app.models.user import User
from app.models.occurrence import Occurrence
from app.models.severity import Severity
# ... todos os outros

__all__ = ["User", "Occurrence", "Severity"]