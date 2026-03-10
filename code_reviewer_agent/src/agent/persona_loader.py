"""Persona configuration loader."""

import yaml
from pathlib import Path
from typing import Optional
import logging

from src.models.persona import PersonaConfiguration, ReviewStandards, QualityThresholds


class PersonaLoader:
    """Loads and validates persona configurations from YAML."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_persona(self, config_path: str) -> PersonaConfiguration:
        """Load persona configuration from YAML file."""
        self.logger.info(f"Loading persona from {config_path}")

        if not Path(config_path).exists():
            raise FileNotFoundError(f"Persona configuration not found: {config_path}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            # Validate required fields
            self._validate_config(config_data)

            # Parse review standards
            standards_data = config_data["review_standards"]
            review_standards = ReviewStandards(
                security_weight=standards_data["security_weight"],
                maintainability_weight=standards_data["maintainability_weight"],
                performance_weight=standards_data["performance_weight"],
                style_consistency_weight=standards_data["style_consistency_weight"],
                documentation_weight=standards_data["documentation_weight"],
            )

            # Parse quality thresholds
            thresholds_data = config_data["quality_thresholds"]
            quality_thresholds = QualityThresholds(
                minimum_acceptable_score=thresholds_data["minimum_acceptable_score"],
                critical_issue_threshold=thresholds_data["critical_issue_threshold"],
                complexity_warning_level=thresholds_data["complexity_warning_level"],
                test_coverage_minimum=thresholds_data["test_coverage_minimum"],
            )

            # Create persona configuration
            persona = PersonaConfiguration(
                role=config_data["role"],
                expertise_areas=config_data["expertise_areas"],
                review_standards=review_standards,
                quality_thresholds=quality_thresholds,
                communication_style=config_data["communication_style"],
                focus_priorities=config_data["focus_priorities"],
            )

            self.logger.info(f"Successfully loaded persona: {persona.role}")
            return persona

        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error: {e}")
            raise ValueError(f"Invalid YAML in persona configuration: {e}")
        except KeyError as e:
            self.logger.error(f"Missing required field: {e}")
            raise ValueError(f"Missing required field in persona configuration: {e}")
        except Exception as e:
            self.logger.error(f"Error loading persona: {e}")
            raise

    def _validate_config(self, config_data: dict):
        """Validate persona configuration structure."""
        required_fields = [
            "role",
            "expertise_areas",
            "review_standards",
            "quality_thresholds",
            "communication_style",
            "focus_priorities",
        ]

        for field in required_fields:
            if field not in config_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate review standards
        standards = config_data["review_standards"]
        required_weights = [
            "security_weight",
            "maintainability_weight",
            "performance_weight",
            "style_consistency_weight",
            "documentation_weight",
        ]
        for weight in required_weights:
            if weight not in standards:
                raise ValueError(f"Missing review standard: {weight}")

        # Validate quality thresholds
        thresholds = config_data["quality_thresholds"]
        required_thresholds = [
            "minimum_acceptable_score",
            "critical_issue_threshold",
            "complexity_warning_level",
            "test_coverage_minimum",
        ]
        for threshold in required_thresholds:
            if threshold not in thresholds:
                raise ValueError(f"Missing quality threshold: {threshold}")
