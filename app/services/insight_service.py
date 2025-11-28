from app.repositories.insight_repository import InsightRepository
from app.schemas.insight import InsightResponse, InsightSummary


class InsightService:
    def __init__(self, insight_repository: InsightRepository):
        self.insight_repo = insight_repository

    def get_insights(self) -> InsightResponse:
        summary_data = self.insight_repo.get_occurrences_summary()
        top_categories = self.insight_repo.get_top_categories()
        severity_distribution = self.insight_repo.get_severity_distribution()
        avg_resolution_time = self.insight_repo.get_average_resolution_time()

        summary = InsightSummary(**summary_data)

        return InsightResponse(
            summary=summary,
            top_categories=top_categories,
            severity_distribution=severity_distribution,
            average_resolution_time=avg_resolution_time,
        )
