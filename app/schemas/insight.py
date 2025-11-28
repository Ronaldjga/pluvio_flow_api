from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class InsightSummary(BaseModel):
    total_occurrences: int
    occurrences_by_status: dict
    occurrences_by_category: dict
    occurrences_by_severity: dict
    recent_activity: int


class CategoryStats(BaseModel):
    category: str
    count: int
    percentage: float


class SeverityStats(BaseModel):
    severity_name: str
    count: int
    color: Optional[str] = None  # Tornar opcional


class InsightResponse(BaseModel):
    summary: InsightSummary
    top_categories: List[CategoryStats]
    severity_distribution: List[SeverityStats]
    average_resolution_time: Optional[float] = None
