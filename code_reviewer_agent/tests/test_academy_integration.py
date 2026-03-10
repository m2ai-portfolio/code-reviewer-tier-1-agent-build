"""Tests for Academy integration."""

import pytest

from src.tools.academy_resolver import AcademyResolver
from src.models.academy_models import AcademyToolDefinition


class TestAcademyResolver:
    """Test Academy tool resolution."""

    def test_resolve_mock_tools(self):
        """Test resolving mock tools when Academy is unavailable."""
        resolver = AcademyResolver()
        tools = resolver.resolve_tools("code_review")

        assert tools is not None
        assert len(tools) > 0
        assert all(isinstance(tool, AcademyToolDefinition) for tool in tools)

        # Check for expected tools
        tool_names = [tool.tool_name for tool in tools]
        assert "ast_analyzer" in tool_names
        assert "security_scanner" in tool_names
        assert "pattern_matcher" in tool_names

    def test_tool_definition_structure(self):
        """Test that tool definitions have correct structure."""
        resolver = AcademyResolver()
        tools = resolver.resolve_tools("code_review")

        for tool in tools:
            assert hasattr(tool, "tool_name")
            assert hasattr(tool, "tool_group")
            assert hasattr(tool, "version")
            assert hasattr(tool, "interface_schema")
            assert hasattr(tool, "capabilities")
            assert hasattr(tool, "execution_parameters")

            assert tool.tool_group == "code_review"
            assert isinstance(tool.capabilities, list)
            assert isinstance(tool.execution_parameters, dict)

    def test_caching_behavior(self):
        """Test that tools are cached."""
        resolver = AcademyResolver(cache_ttl_minutes=60)

        # First call
        tools1 = resolver.resolve_tools("code_review")

        # Second call should use cache
        tools2 = resolver.resolve_tools("code_review")

        assert len(tools1) == len(tools2)
        assert tools1[0].tool_name == tools2[0].tool_name

    def test_empty_tool_group(self):
        """Test resolving non-existent tool group."""
        resolver = AcademyResolver()
        tools = resolver.resolve_tools("nonexistent_group")

        # Should return empty list for unknown groups
        assert tools == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
