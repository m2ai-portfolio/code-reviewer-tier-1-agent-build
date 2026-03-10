"""Tests for persona loading."""

import pytest
from pathlib import Path
import yaml

from src.agent.persona_loader import PersonaLoader
from src.models.persona import PersonaConfiguration


@pytest.fixture
def test_persona_path(tmp_path):
    """Create a temporary test persona file."""
    persona_data = {
        "role": "Test Code Reviewer",
        "expertise_areas": ["Python", "Testing"],
        "review_standards": {
            "security_weight": 0.3,
            "maintainability_weight": 0.3,
            "performance_weight": 0.15,
            "style_consistency_weight": 0.15,
            "documentation_weight": 0.1,
        },
        "quality_thresholds": {
            "minimum_acceptable_score": 70.0,
            "critical_issue_threshold": 0,
            "complexity_warning_level": 10,
            "test_coverage_minimum": 0.8,
        },
        "communication_style": "professional",
        "focus_priorities": ["Security", "Quality"],
    }

    persona_file = tmp_path / "test_persona.yaml"
    with open(persona_file, "w") as f:
        yaml.dump(persona_data, f)

    return str(persona_file)


class TestPersonaLoader:
    """Test persona loader functionality."""

    def test_load_valid_persona(self, test_persona_path):
        """Test loading a valid persona configuration."""
        loader = PersonaLoader()
        persona = loader.load_persona(test_persona_path)

        assert persona is not None
        assert isinstance(persona, PersonaConfiguration)
        assert persona.role == "Test Code Reviewer"
        assert len(persona.expertise_areas) == 2
        assert persona.review_standards.security_weight == 0.3
        assert persona.quality_thresholds.minimum_acceptable_score == 70.0

    def test_load_nonexistent_file(self):
        """Test loading a nonexistent persona file."""
        loader = PersonaLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_persona("/nonexistent/path/persona.yaml")

    def test_load_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML."""
        invalid_file = tmp_path / "invalid.yaml"
        with open(invalid_file, "w") as f:
            f.write("{ invalid yaml content")

        loader = PersonaLoader()
        with pytest.raises(ValueError, match="Invalid YAML"):
            loader.load_persona(str(invalid_file))

    def test_load_missing_required_field(self, tmp_path):
        """Test loading persona with missing required fields."""
        incomplete_data = {
            "role": "Test Reviewer",
            # Missing other required fields
        }

        incomplete_file = tmp_path / "incomplete.yaml"
        with open(incomplete_file, "w") as f:
            yaml.dump(incomplete_data, f)

        loader = PersonaLoader()
        with pytest.raises(ValueError, match="Missing required field"):
            loader.load_persona(str(incomplete_file))

    def test_review_standards_validation(self, tmp_path):
        """Test that review standards weights are validated."""
        invalid_weights = {
            "role": "Test Reviewer",
            "expertise_areas": ["Python"],
            "review_standards": {
                "security_weight": 0.5,  # Total > 1.0
                "maintainability_weight": 0.5,
                "performance_weight": 0.5,
                "style_consistency_weight": 0.5,
                "documentation_weight": 0.5,
            },
            "quality_thresholds": {
                "minimum_acceptable_score": 70.0,
                "critical_issue_threshold": 0,
                "complexity_warning_level": 10,
                "test_coverage_minimum": 0.8,
            },
            "communication_style": "professional",
            "focus_priorities": ["Security"],
        }

        invalid_file = tmp_path / "invalid_weights.yaml"
        with open(invalid_file, "w") as f:
            yaml.dump(invalid_weights, f)

        loader = PersonaLoader()
        with pytest.raises(ValueError, match="weights must sum to 1.0"):
            loader.load_persona(str(invalid_file))

    def test_load_real_persona(self):
        """Test loading the actual code_reviewer persona if it exists."""
        persona_path = Path(__file__).parent.parent / "config" / "personas" / "code_reviewer.yaml"

        if persona_path.exists():
            loader = PersonaLoader()
            persona = loader.load_persona(str(persona_path))

            assert persona is not None
            assert "Code" in persona.role or "Reviewer" in persona.role
            assert len(persona.expertise_areas) > 0
            assert persona.review_standards.security_weight > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
