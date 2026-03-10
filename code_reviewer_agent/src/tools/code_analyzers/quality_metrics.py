"""Quality metrics calculator."""

from typing import List, Dict, Any
from ..code_analyzers.ast_analyzer import ASTAnalysisResult
from ..code_analyzers.security_scanner import SecurityIssue
from ..code_analyzers.pattern_matcher import PatternMatch
from src.models.review_models import QualityMetrics, ReviewFinding


class QualityMetricsCalculator:
    """Calculates quality scores from analysis results."""

    def __init__(
        self,
        security_weight: float = 0.3,
        maintainability_weight: float = 0.3,
        performance_weight: float = 0.15,
        style_weight: float = 0.15,
        documentation_weight: float = 0.1,
    ):
        self.security_weight = security_weight
        self.maintainability_weight = maintainability_weight
        self.performance_weight = performance_weight
        self.style_weight = style_weight
        self.documentation_weight = documentation_weight

    def calculate_metrics(
        self,
        findings: List[ReviewFinding],
        ast_results: List[ASTAnalysisResult],
        lines_analyzed: int,
        files_reviewed: int,
    ) -> QualityMetrics:
        """Calculate overall quality metrics from findings."""

        # Calculate category-specific scores
        security_score = self._calculate_security_score(findings)
        maintainability_score = self._calculate_maintainability_score(findings, ast_results)
        performance_score = self._calculate_performance_score(findings)
        style_score = self._calculate_style_score(findings)
        documentation_score = self._calculate_documentation_score(findings, ast_results)

        # Calculate weighted overall score
        overall_score = (
            security_score * self.security_weight
            + maintainability_score * self.maintainability_weight
            + performance_score * self.performance_weight
            + style_score * self.style_weight
            + documentation_score * self.documentation_weight
        )

        return QualityMetrics(
            overall_score=round(overall_score, 2),
            security_score=round(security_score, 2),
            maintainability_score=round(maintainability_score, 2),
            performance_score=round(performance_score, 2),
            style_score=round(style_score, 2),
            documentation_score=round(documentation_score, 2),
            lines_analyzed=lines_analyzed,
            files_reviewed=files_reviewed,
        )

    def _calculate_security_score(self, findings: List[ReviewFinding]) -> float:
        """Calculate security score (0-100)."""
        security_findings = [f for f in findings if f.category == "security"]

        if not security_findings:
            return 100.0

        # Deduct points based on severity
        score = 100.0
        severity_penalties = {
            "critical": 25,
            "high": 15,
            "medium": 8,
            "low": 3,
        }

        for finding in security_findings:
            penalty = severity_penalties.get(finding.severity, 5)
            score -= penalty

        return max(0.0, score)

    def _calculate_maintainability_score(
        self, findings: List[ReviewFinding], ast_results: List[ASTAnalysisResult]
    ) -> float:
        """Calculate maintainability score (0-100)."""
        maintainability_findings = [f for f in findings if f.category == "maintainability"]

        score = 100.0

        # Deduct points for findings
        severity_penalties = {
            "critical": 20,
            "high": 12,
            "medium": 6,
            "low": 2,
        }

        for finding in maintainability_findings:
            penalty = severity_penalties.get(finding.severity, 4)
            score -= penalty

        # Additional deductions for complexity
        for ast_result in ast_results:
            if ast_result.max_complexity > 15:
                score -= 10
            elif ast_result.max_complexity > 10:
                score -= 5

            # Penalize for too many anti-patterns
            if len(ast_result.anti_patterns) > 10:
                score -= 15
            elif len(ast_result.anti_patterns) > 5:
                score -= 8

        return max(0.0, score)

    def _calculate_performance_score(self, findings: List[ReviewFinding]) -> float:
        """Calculate performance score (0-100)."""
        performance_findings = [f for f in findings if f.category == "performance"]

        if not performance_findings:
            return 95.0  # Default good score if no performance issues found

        score = 100.0
        severity_penalties = {
            "critical": 20,
            "high": 12,
            "medium": 6,
            "low": 2,
        }

        for finding in performance_findings:
            penalty = severity_penalties.get(finding.severity, 4)
            score -= penalty

        return max(0.0, score)

    def _calculate_style_score(self, findings: List[ReviewFinding]) -> float:
        """Calculate style consistency score (0-100)."""
        style_findings = [f for f in findings if f.category == "style"]

        score = 100.0

        # Style issues are generally less severe
        for finding in style_findings:
            if finding.severity == "medium":
                score -= 4
            elif finding.severity == "low":
                score -= 1

        return max(0.0, score)

    def _calculate_documentation_score(
        self, findings: List[ReviewFinding], ast_results: List[ASTAnalysisResult]
    ) -> float:
        """Calculate documentation score (0-100)."""
        doc_findings = [f for f in findings if f.category == "documentation"]

        score = 100.0

        # Penalize for missing documentation
        for finding in doc_findings:
            score -= 3  # Each missing docstring

        # Check documentation coverage from AST
        for ast_result in ast_results:
            total_entities = len(ast_result.functions) + len(ast_result.classes)
            if total_entities > 0:
                # Estimate documentation ratio (this is simplified)
                # In real implementation, we'd track which entities have docs
                missing_docs = sum(
                    1
                    for ap in ast_result.anti_patterns
                    if ap.get("type") == "missing_docstring"
                )
                if missing_docs > total_entities * 0.5:
                    score -= 20
                elif missing_docs > total_entities * 0.3:
                    score -= 10

        return max(0.0, score)
