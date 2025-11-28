from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from app.models.occurrence import Occurrence
from app.models.severity import Severity


class InsightRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_occurrences_summary(self):
        # Total de ocorrências
        total = self.db.query(Occurrence).count()

        # Por status
        by_status = dict(
            self.db.query(Occurrence.status, func.count(Occurrence.id))
            .group_by(Occurrence.status)
            .all()
        )

        # Por categoria
        by_category = dict(
            self.db.query(Occurrence.category, func.count(Occurrence.id))
            .group_by(Occurrence.category)
            .all()
        )

        # Por severidade
        by_severity = dict(
            self.db.query(Severity.name, func.count(Occurrence.id))
            .join(Occurrence.severity)
            .group_by(Severity.name)
            .all()
        )

        # Atividade recente (últimos 7 dias)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent = (
            self.db.query(Occurrence).filter(Occurrence.created_at >= week_ago).count()
        )

        return {
            "total_occurrences": total,
            "occurrences_by_status": by_status,
            "occurrences_by_category": by_category,
            "occurrences_by_severity": by_severity,
            "recent_activity": recent,
        }

    def get_top_categories(self, limit: int = 5):
        categories = (
            self.db.query(Occurrence.category, func.count(Occurrence.id).label("count"))
            .group_by(Occurrence.category)
            .order_by(desc("count"))
            .limit(limit)
            .all()
        )

        total = self.db.query(Occurrence).count()

        result = []
        for category, count in categories:
            percentage = (count / total * 100) if total > 0 else 0
            result.append(
                {
                    "category": category,
                    "count": count,
                    "percentage": round(percentage, 2),
                }
            )

        return result

    def get_severity_distribution(self):
        severities = (
            self.db.query(
                Severity.name, Severity.color, func.count(Occurrence.id).label("count")
            )
            .join(Occurrence.severity)
            .group_by(Severity.name, Severity.color)
            .all()
        )

        return [
            {
                "severity_name": name,
                "count": count,
                "color": color or "#6B7280",  # Valor padrão se for None
            }
            for name, color, count in severities
        ]

    def get_average_resolution_time(self):
        # Para simplificar, vamos retornar None por enquanto
        # Você pode implementar essa lógica depois
        return None
