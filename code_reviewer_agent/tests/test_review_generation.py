"""Tests for review report generation."""

import pytest
from datetime import datetime
from pathlib import Path

from src.models.review_models import (
    ReviewReport,
    ReviewFinding,
    QualityMetrics,
    RepositoryInfo,
)
from src.review.report_generator import ReportGenerator


@pytest.fixture
def sample_report():
    """Create a sample review report for testing."""
    repo_info = RepositoryInfo(
        url="https://github.com/test/repo",
        commit_hash="abc1234",
        branch="main",
        languages_detected=["Python", "JavaScript"],
        total_files=10,
        total_lines=500,
    )

    metrics = QualityMetrics(
        overall_score=75.5,
        security_score=65.0,
        maintainability_score=80.0,
        performance_score=90.0,
        style_score=85.0,
        documentation_score=70.0,
        lines_analyzed=500,
        files_reviewed=10,
    )

    findings = [
        ReviewFinding(
            finding_id="F001",
            severity="critical",
            category="security",
            file_path="src/auth.py",
            line_number=42,
            description="Hardcoded password detected",
            evidence_snippet='password = "admin123"',
            remediation_suggestion="Use environment variables for credentials",
            confidence_score=0.95,
        ),
        ReviewFinding(
            finding_id="F002",
            severity="high",
            category="maintainability",
            file_path="src/utils.py",
            line_number=100,
            description="Function complexity too high",
            evidence_snippet="def complex_function():",
            remediation_suggestion="Refactor into smaller functions",
            confidence_score=0.85,
        ),
        ReviewFinding(
            finding_id="F003",
            severity="medium",
            category="style",
            file_path="src/main.py",
            line_number=25,
            description="Magic number should be a constant",
            evidence_snippet="if x > 100:",
            remediation_suggestion="Define as named constant",
            confidence_score=0.75,
        ),
    ]

    return ReviewReport(
        review_id="REV123",
        timestamp=datetime(2024, 1, 15, 10, 30, 0),
        repository_info=repo_info,
        quality_metrics=metrics,
        findings=findings,
        summary="Code review identified 3 issues requiring attention.",
        recommendations=[
            "Address critical security vulnerability immediately",
            "Refactor complex functions",
            "Define magic numbers as constants",
        ],
        reviewer_persona="Code Reviewer Agent",
    )


class TestReportGenerator:
    """Test report generation functionality."""

    def test_generate_json_report(self, sample_report):
        """Test JSON report generation."""
        generator = ReportGenerator()
        json_report = generator.generate_json(sample_report)

        assert json_report is not None
        assert isinstance(json_report, str)
        assert "REV123" in json_report
        assert "security" in json_report
        assert "75.5" in json_report

        # Verify it's valid JSON
        import json

        parsed = json.loads(json_report)
        assert parsed["review_id"] == "REV123"
        assert parsed["quality_metrics"]["overall_score"] == 75.5
        assert len(parsed["findings"]) == 3

    def test_generate_markdown_report(self, sample_report):
        """Test Markdown report generation."""
        generator = ReportGenerator()
        md_report = generator.generate_markdown(sample_report)

        assert md_report is not None
        assert isinstance(md_report, str)

        # Check for key sections
        assert "# Code Review Report" in md_report
        assert "## Repository Information" in md_report
        assert "## Quality Metrics" in md_report
        assert "## Summary" in md_report
        assert "## Findings" in md_report
        assert "## Recommendations" in md_report

        # Check for specific content
        assert "REV123" in md_report
        assert "abc1234" in md_report
        assert "CRITICAL Severity" in md_report
        assert "Hardcoded password" in md_report

    def test_save_json_report(self, sample_report, tmp_path):
        """Test saving JSON report to file."""
        generator = ReportGenerator()
        output_file = tmp_path / "review_report.json"

        generator.save_report(sample_report, str(output_file), format="json")

        assert output_file.exists()

        # Verify content
        import json

        with open(output_file, "r") as f:
            data = json.load(f)
            assert data["review_id"] == "REV123"

    def test_save_markdown_report(self, sample_report, tmp_path):
        """Test saving Markdown report to file."""
        generator = ReportGenerator()
        output_file = tmp_path / "review_report.md"

        generator.save_report(sample_report, str(output_file), format="markdown")

        assert output_file.exists()

        # Verify content
        with open(output_file, "r") as f:
            content = f.read()
            assert "# Code Review Report" in content
            assert "REV123" in content

    def test_report_includes_all_findings(self, sample_report):
        """Test that report includes all findings."""
        generator = ReportGenerator()
        json_report = generator.generate_json(sample_report)

        import json

        parsed = json.loads(json_report)
        assert len(parsed["findings"]) == 3

        # Check severity distribution
        severities = [f["severity"] for f in parsed["findings"]]
        assert "critical" in severities
        assert "high" in severities
        assert "medium" in severities

    def test_report_includes_metrics(self, sample_report):
        """Test that report includes all quality metrics."""
        generator = ReportGenerator()
        json_report = generator.generate_json(sample_report)

        import json

        parsed = json.loads(json_report)
        metrics = parsed["quality_metrics"]

        assert metrics["overall_score"] == 75.5
        assert metrics["security_score"] == 65.0
        assert metrics["maintainability_score"] == 80.0
        assert metrics["performance_score"] == 90.0
        assert metrics["style_score"] == 85.0
        assert metrics["documentation_score"] == 70.0
        assert metrics["lines_analyzed"] == 500
        assert metrics["files_reviewed"] == 10

    def test_markdown_report_formatting(self, sample_report):
        """Test Markdown report formatting."""
        generator = ReportGenerator()
        md_report = generator.generate_markdown(sample_report)

        # Check table formatting
        assert "| Metric | Score |" in md_report
        assert "|--------|-------|" in md_report

        # Check code blocks
        assert "```" in md_report

        # Check headings
        assert md_report.count("###") >= 3  # At least 3 severity levels

    def test_unsupported_format_raises_error(self, sample_report, tmp_path):
        """Test that unsupported format raises error."""
        generator = ReportGenerator()
        output_file = tmp_path / "report.xml"

        with pytest.raises(ValueError, match="Unsupported format"):
            generator.save_report(sample_report, str(output_file), format="xml")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
