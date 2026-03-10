"""Persona configuration data models."""

from dataclasses import dataclass
from typing import List


@dataclass
class ReviewStandards:
    """Weight distribution for different review aspects."""

    security_weight: float
    maintainability_weight: float
    performance_weight: float
    style_consistency_weight: float
    documentation_weight: float

    def __post_init__(self):
        """Validate weights sum to approximately 1.0."""
        total = (
            self.security_weight
            + self.maintainability_weight
            + self.performance_weight
            + self.style_consistency_weight
            + self.documentation_weight
        )
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Review standards weights must sum to 1.0, got {total}")


@dataclass
class QualityThresholds:
    """Quality thresholds for review acceptance."""

    minimum_acceptable_score: float
    critical_issue_threshold: int
    complexity_warning_level: int
    test_coverage_minimum: float


@dataclass
class PersonaConfiguration:
    """Complete persona configuration loaded from YAML."""

    role: str
    expertise_areas: List[str]
    review_standards: ReviewStandards
    quality_thresholds: QualityThresholds
    communication_style: str
    focus_priorities: List[str]
