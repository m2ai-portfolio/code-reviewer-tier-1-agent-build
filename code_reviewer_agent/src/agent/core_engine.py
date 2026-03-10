"""Main agent orchestration engine."""

import logging
from typing import Optional

from src.models.persona import PersonaConfiguration
from src.models.review_models import CodeReviewRequest, ReviewReport
from .persona_loader import PersonaLoader
from .claude_interface import ClaudeInterface
from src.review.orchestrator import ReviewOrchestrator
from src.review.report_generator import ReportGenerator


class AgentCoreEngine:
    """Core agent engine coordinating persona, tools, and review process."""

    def __init__(self, persona_config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)

        # Load persona if provided
        self.persona: Optional[PersonaConfiguration] = None
        if persona_config_path:
            persona_loader = PersonaLoader()
            self.persona = persona_loader.load_persona(persona_config_path)

        # Initialize components
        self.claude_interface = ClaudeInterface()
        self.review_orchestrator = self._create_orchestrator()
        self.report_generator = ReportGenerator()

    def _create_orchestrator(self) -> ReviewOrchestrator:
        """Create review orchestrator with persona weights."""
        if self.persona:
            standards = self.persona.review_standards
            return ReviewOrchestrator(
                security_weight=standards.security_weight,
                maintainability_weight=standards.maintainability_weight,
                performance_weight=standards.performance_weight,
                style_weight=standards.style_consistency_weight,
                documentation_weight=standards.documentation_weight,
            )
        else:
            return ReviewOrchestrator()

    def execute_review(self, request: CodeReviewRequest) -> ReviewReport:
        """Execute code review with persona-guided analysis."""
        self.logger.info(
            f"Starting review: repository={request.repository_url or 'local'}, scope={request.review_scope}"
        )

        # Execute review
        report = self.review_orchestrator.execute_review(request)

        # Apply persona context to summary if available
        if self.persona:
            report.reviewer_persona = self.persona.role

        self.logger.info(f"Review completed: {report.review_id}")
        return report

    def generate_report(
        self, report: ReviewReport, output_path: Optional[str] = None, format: str = "json"
    ) -> str:
        """Generate review report in specified format."""
        if format == "json":
            content = self.report_generator.generate_json(report)
        elif format == "markdown":
            content = self.report_generator.generate_markdown(report)
        else:
            raise ValueError(f"Unsupported format: {format}")

        if output_path:
            self.report_generator.save_report(report, output_path, format)
            self.logger.info(f"Report saved to {output_path}")

        return content
