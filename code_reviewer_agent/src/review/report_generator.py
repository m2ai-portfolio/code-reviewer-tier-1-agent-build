"""Review report formatting and generation."""

import json
from typing import Dict, Any
from datetime import datetime

from src.models.review_models import ReviewReport, ReviewFinding


class ReportGenerator:
    """Generates review reports in multiple formats."""

    def generate_json(self, report: ReviewReport) -> str:
        """Generate JSON format report."""
        report_dict = self._report_to_dict(report)
        return json.dumps(report_dict, indent=2, default=str)

    def generate_markdown(self, report: ReviewReport) -> str:
        """Generate Markdown format report."""
        lines = []

        # Header
        lines.append(f"# Code Review Report")
        lines.append(f"")
        lines.append(f"**Review ID:** {report.review_id}")
        lines.append(f"**Date:** {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Reviewer:** {report.reviewer_persona}")
        lines.append(f"")

        # Repository Info
        lines.append(f"## Repository Information")
        lines.append(f"")
        lines.append(f"- **URL:** {report.repository_info.url}")
        lines.append(f"- **Branch:** {report.repository_info.branch}")
        lines.append(f"- **Commit:** {report.repository_info.commit_hash}")
        lines.append(f"- **Languages:** {', '.join(report.repository_info.languages_detected)}")
        lines.append(
            f"- **Scope:** {report.repository_info.total_files} files, {report.repository_info.total_lines} lines"
        )
        lines.append(f"")

        # Quality Metrics
        lines.append(f"## Quality Metrics")
        lines.append(f"")
        lines.append(f"| Metric | Score |")
        lines.append(f"|--------|-------|")
        lines.append(f"| **Overall Quality** | **{report.quality_metrics.overall_score}/100** |")
        lines.append(f"| Security | {report.quality_metrics.security_score}/100 |")
        lines.append(f"| Maintainability | {report.quality_metrics.maintainability_score}/100 |")
        lines.append(f"| Performance | {report.quality_metrics.performance_score}/100 |")
        lines.append(f"| Style | {report.quality_metrics.style_score}/100 |")
        lines.append(f"| Documentation | {report.quality_metrics.documentation_score}/100 |")
        lines.append(f"")

        # Summary
        lines.append(f"## Summary")
        lines.append(f"")
        lines.append(report.summary)
        lines.append(f"")

        # Findings by severity
        lines.append(f"## Findings")
        lines.append(f"")

        findings_by_severity = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
        }

        for finding in report.findings:
            findings_by_severity[finding.severity].append(finding)

        for severity in ["critical", "high", "medium", "low"]:
            findings = findings_by_severity[severity]
            if findings:
                lines.append(f"### {severity.upper()} Severity ({len(findings)})")
                lines.append(f"")

                for finding in findings[:10]:  # Limit to 10 per severity
                    lines.append(f"#### {finding.description}")
                    lines.append(f"")
                    lines.append(f"- **File:** `{finding.file_path}`")
                    if finding.line_number:
                        lines.append(f"- **Line:** {finding.line_number}")
                    lines.append(f"- **Category:** {finding.category}")
                    lines.append(f"- **Confidence:** {finding.confidence_score:.0%}")
                    lines.append(f"")
                    if finding.evidence_snippet:
                        lines.append(f"**Evidence:**")
                        lines.append(f"```")
                        lines.append(finding.evidence_snippet)
                        lines.append(f"```")
                        lines.append(f"")
                    lines.append(f"**Remediation:**")
                    lines.append(finding.remediation_suggestion)
                    lines.append(f"")

                if len(findings) > 10:
                    lines.append(f"*... and {len(findings) - 10} more {severity} severity issues*")
                    lines.append(f"")

        # Recommendations
        lines.append(f"## Recommendations")
        lines.append(f"")
        for i, recommendation in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {recommendation}")
        lines.append(f"")

        return "\n".join(lines)

    def save_report(self, report: ReviewReport, output_path: str, format: str = "json"):
        """Save report to file."""
        if format == "json":
            content = self.generate_json(report)
        elif format == "markdown":
            content = self.generate_markdown(report)
        else:
            raise ValueError(f"Unsupported format: {format}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _report_to_dict(self, report: ReviewReport) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "review_id": report.review_id,
            "timestamp": report.timestamp.isoformat(),
            "reviewer_persona": report.reviewer_persona,
            "repository": {
                "url": report.repository_info.url,
                "commit_hash": report.repository_info.commit_hash,
                "branch": report.repository_info.branch,
                "languages": report.repository_info.languages_detected,
                "total_files": report.repository_info.total_files,
                "total_lines": report.repository_info.total_lines,
            },
            "quality_metrics": {
                "overall_score": report.quality_metrics.overall_score,
                "security_score": report.quality_metrics.security_score,
                "maintainability_score": report.quality_metrics.maintainability_score,
                "performance_score": report.quality_metrics.performance_score,
                "style_score": report.quality_metrics.style_score,
                "documentation_score": report.quality_metrics.documentation_score,
                "lines_analyzed": report.quality_metrics.lines_analyzed,
                "files_reviewed": report.quality_metrics.files_reviewed,
            },
            "summary": report.summary,
            "findings": [
                {
                    "finding_id": f.finding_id,
                    "severity": f.severity,
                    "category": f.category,
                    "file_path": f.file_path,
                    "line_number": f.line_number,
                    "description": f.description,
                    "evidence_snippet": f.evidence_snippet,
                    "remediation_suggestion": f.remediation_suggestion,
                    "confidence_score": f.confidence_score,
                }
                for f in report.findings
            ],
            "recommendations": report.recommendations,
        }
