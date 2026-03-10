"""Review operation data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class CodeReviewRequest:
    """Request parameters for code review operation."""

    repository_url: Optional[str] = None
    file_paths: Optional[List[str]] = None
    target_branch: str = "main"
    review_scope: str = "full"  # full, incremental, targeted
    output_format: str = "json"
    priority_focus: Optional[List[str]] = None


@dataclass
class ReviewFinding:
    """Individual finding from code review."""

    finding_id: str
    severity: str  # critical, high, medium, low
    category: str  # security, maintainability, performance, style
    file_path: str
    line_number: Optional[int]
    description: str
    evidence_snippet: str
    remediation_suggestion: str
    confidence_score: float

    def __post_init__(self):
        """Validate severity and category."""
        valid_severities = ["critical", "high", "medium", "low"]
        if self.severity not in valid_severities:
            raise ValueError(f"Invalid severity: {self.severity}")

        valid_categories = ["security", "maintainability", "performance", "style", "documentation"]
        if self.category not in valid_categories:
            raise ValueError(f"Invalid category: {self.category}")


@dataclass
class QualityMetrics:
    """Quality metrics calculated from review."""

    overall_score: float
    security_score: float
    maintainability_score: float
    performance_score: float
    style_score: float
    documentation_score: float
    lines_analyzed: int
    files_reviewed: int


@dataclass
class RepositoryInfo:
    """Information about analyzed repository."""

    url: str
    commit_hash: str
    branch: str
    languages_detected: List[str]
    total_files: int
    total_lines: int


@dataclass
class ReviewReport:
    """Complete review report."""

    review_id: str
    timestamp: datetime
    repository_info: RepositoryInfo
    quality_metrics: QualityMetrics
    findings: List[ReviewFinding]
    summary: str
    recommendations: List[str]
    reviewer_persona: str
