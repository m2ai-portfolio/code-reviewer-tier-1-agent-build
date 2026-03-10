"""Review workflow orchestration."""

import os
import uuid
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import logging

from src.models.review_models import (
    CodeReviewRequest,
    ReviewFinding,
    ReviewReport,
    RepositoryInfo,
    QualityMetrics,
)
from src.tools.code_analyzers.ast_analyzer import ASTAnalyzer, ASTAnalysisResult
from src.tools.code_analyzers.security_scanner import SecurityScanner
from src.tools.code_analyzers.pattern_matcher import PatternMatcher
from src.tools.code_analyzers.quality_metrics import QualityMetricsCalculator
from .repository_handler import RepositoryHandler, RepositoryContext


class ReviewOrchestrator:
    """Orchestrates multi-dimensional code review process."""

    def __init__(
        self,
        max_file_size_kb: int = 500,
        security_weight: float = 0.3,
        maintainability_weight: float = 0.3,
        performance_weight: float = 0.15,
        style_weight: float = 0.15,
        documentation_weight: float = 0.1,
    ):
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.logger = logging.getLogger(__name__)

        # Initialize analyzers
        self.ast_analyzer = ASTAnalyzer()
        self.security_scanner = SecurityScanner()
        self.pattern_matcher = PatternMatcher()
        self.metrics_calculator = QualityMetricsCalculator(
            security_weight=security_weight,
            maintainability_weight=maintainability_weight,
            performance_weight=performance_weight,
            style_weight=style_weight,
            documentation_weight=documentation_weight,
        )
        self.repo_handler = RepositoryHandler()

    def execute_review(self, request: CodeReviewRequest) -> ReviewReport:
        """Execute complete code review workflow."""
        self.logger.info(f"Starting code review: scope={request.review_scope}")

        # Prepare repository
        repo_context = self.repo_handler.prepare_repository(
            repository_url=request.repository_url,
            local_path=request.file_paths[0] if request.file_paths else None,
            branch=request.target_branch,
        )

        try:
            # Determine files to analyze
            if request.review_scope == "incremental":
                files_to_analyze = self.repo_handler.get_changed_files(repo_context.local_path)
            elif request.file_paths:
                files_to_analyze = request.file_paths
            else:
                files_to_analyze = self._get_all_analyzable_files(repo_context.local_path)

            self.logger.info(f"Analyzing {len(files_to_analyze)} files")

            # Analyze files
            all_findings = []
            all_ast_results = []
            total_lines = 0

            for file_path in files_to_analyze:
                findings, ast_result, lines = self._analyze_file(file_path, repo_context.local_path)
                all_findings.extend(findings)
                if ast_result:
                    all_ast_results.append(ast_result)
                total_lines += lines

            # Calculate quality metrics
            metrics = self.metrics_calculator.calculate_metrics(
                findings=all_findings,
                ast_results=all_ast_results,
                lines_analyzed=total_lines,
                files_reviewed=len(files_to_analyze),
            )

            # Generate repository info
            repo_info = RepositoryInfo(
                url=request.repository_url or repo_context.local_path,
                commit_hash=repo_context.commit_hash,
                branch=repo_context.branch,
                languages_detected=self._detect_languages(files_to_analyze),
                total_files=len(files_to_analyze),
                total_lines=total_lines,
            )

            # Generate summary and recommendations
            summary = self._generate_summary(all_findings, metrics)
            recommendations = self._generate_recommendations(all_findings, metrics)

            # Create review report
            report = ReviewReport(
                review_id=str(uuid.uuid4())[:8],
                timestamp=datetime.now(),
                repository_info=repo_info,
                quality_metrics=metrics,
                findings=all_findings,
                summary=summary,
                recommendations=recommendations,
                reviewer_persona="Code Reviewer Agent",
            )

            self.logger.info(
                f"Review complete: {len(all_findings)} findings, score={metrics.overall_score}"
            )
            return report

        finally:
            # Cleanup temporary repository if needed
            self.repo_handler.cleanup(repo_context)

    def _analyze_file(
        self, file_path: str, repo_root: str
    ) -> tuple[List[ReviewFinding], Optional[ASTAnalysisResult], int]:
        """Analyze a single file."""
        # Check file size
        if os.path.getsize(file_path) > self.max_file_size_bytes:
            self.logger.warning(f"Skipping large file: {file_path}")
            return [], None, 0

        # Read file content
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            self.logger.error(f"Could not read file {file_path}: {e}")
            return [], None, 0

        lines = content.count("\n") + 1
        relative_path = os.path.relpath(file_path, repo_root)

        findings = []

        # Run security scanner
        security_issues = self.security_scanner.scan_file(file_path, content)
        for issue in security_issues:
            findings.append(
                ReviewFinding(
                    finding_id=str(uuid.uuid4())[:8],
                    severity=issue.severity,
                    category="security",
                    file_path=relative_path,
                    line_number=issue.line_number,
                    description=issue.description,
                    evidence_snippet=issue.evidence[:200],
                    remediation_suggestion=issue.remediation,
                    confidence_score=0.85,
                )
            )

        # Run pattern matcher
        pattern_matches = self.pattern_matcher.analyze_file(file_path, content)
        for match in pattern_matches:
            # Map pattern types to categories
            category = "maintainability"
            severity = "low"

            if match.pattern_type in ["unused_import", "commented_code"]:
                severity = "low"
            elif match.pattern_type in ["duplicate_code", "magic_number"]:
                severity = "medium"
            elif match.pattern_type == "missing_docstring":
                category = "documentation"
                severity = "low"

            findings.append(
                ReviewFinding(
                    finding_id=str(uuid.uuid4())[:8],
                    severity=severity,
                    category=category,
                    file_path=relative_path,
                    line_number=match.line_number,
                    description=match.description,
                    evidence_snippet=match.evidence[:200],
                    remediation_suggestion=match.suggestion,
                    confidence_score=0.75,
                )
            )

        # Run AST analyzer for Python files
        ast_result = None
        if file_path.endswith(".py"):
            ast_result = self.ast_analyzer.analyze_file(file_path, content)

            # Convert AST anti-patterns to findings
            for anti_pattern in ast_result.anti_patterns:
                severity = "medium"
                if anti_pattern["type"] == "high_complexity":
                    severity = "high"

                findings.append(
                    ReviewFinding(
                        finding_id=str(uuid.uuid4())[:8],
                        severity=severity,
                        category="maintainability",
                        file_path=relative_path,
                        line_number=anti_pattern.get("line", 0),
                        description=f"{anti_pattern['type'].replace('_', ' ').title()}: {anti_pattern.get('entity', 'N/A')}",
                        evidence_snippet=f"Value: {anti_pattern.get('value')}, Threshold: {anti_pattern.get('threshold')}",
                        remediation_suggestion="Refactor to reduce complexity and improve readability",
                        confidence_score=0.90,
                    )
                )

        return findings, ast_result, lines

    def _get_all_analyzable_files(self, repo_path: str) -> List[str]:
        """Get all files that can be analyzed."""
        analyzable_files = []
        code_extensions = {".py", ".js", ".ts", ".java", ".go"}

        for root, dirs, files in os.walk(repo_path):
            # Skip common non-code directories
            dirs[:] = [
                d
                for d in dirs
                if d not in {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist"}
            ]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext in code_extensions:
                    analyzable_files.append(os.path.join(root, file))

        return analyzable_files

    def _detect_languages(self, file_paths: List[str]) -> List[str]:
        """Detect programming languages from file extensions."""
        language_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".go": "Go",
            ".rb": "Ruby",
            ".cpp": "C++",
            ".c": "C",
        }

        languages = set()
        for file_path in file_paths:
            _, ext = os.path.splitext(file_path)
            if ext in language_map:
                languages.add(language_map[ext])

        return sorted(languages)

    def _generate_summary(self, findings: List[ReviewFinding], metrics: QualityMetrics) -> str:
        """Generate review summary."""
        critical_count = sum(1 for f in findings if f.severity == "critical")
        high_count = sum(1 for f in findings if f.severity == "high")
        medium_count = sum(1 for f in findings if f.severity == "medium")
        low_count = sum(1 for f in findings if f.severity == "low")

        summary_parts = [
            f"Code review completed for {metrics.files_reviewed} files ({metrics.lines_analyzed} lines).",
            f"Overall quality score: {metrics.overall_score}/100.",
            f"Found {len(findings)} issues: {critical_count} critical, {high_count} high, {medium_count} medium, {low_count} low severity.",
        ]

        if critical_count > 0:
            summary_parts.append("Critical issues require immediate attention.")
        elif metrics.overall_score >= 80:
            summary_parts.append("Code quality is good with minor issues.")
        elif metrics.overall_score >= 60:
            summary_parts.append("Code quality is acceptable but needs improvement.")
        else:
            summary_parts.append("Code quality needs significant improvement.")

        return " ".join(summary_parts)

    def _generate_recommendations(
        self, findings: List[ReviewFinding], metrics: QualityMetrics
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Security recommendations
        security_findings = [f for f in findings if f.category == "security"]
        if security_findings:
            critical_security = [f for f in security_findings if f.severity == "critical"]
            if critical_security:
                recommendations.append(
                    f"Address {len(critical_security)} critical security vulnerabilities immediately"
                )
            recommendations.append(
                "Review and implement security best practices across the codebase"
            )

        # Maintainability recommendations
        if metrics.maintainability_score < 70:
            recommendations.append(
                "Refactor complex functions and reduce code duplication to improve maintainability"
            )

        # Documentation recommendations
        if metrics.documentation_score < 60:
            recommendations.append(
                "Add docstrings to public functions and classes to improve documentation"
            )

        # Style recommendations
        style_findings = [f for f in findings if f.category == "style"]
        if len(style_findings) > 10:
            recommendations.append("Apply consistent code formatting using automated tools")

        # General recommendations
        if metrics.overall_score < 70:
            recommendations.append("Consider implementing pre-commit hooks for automated quality checks")

        if not recommendations:
            recommendations.append("Continue maintaining high code quality standards")

        return recommendations
