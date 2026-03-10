"""Academy tool catalog resolver with mock fallback."""

import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from src.models.academy_models import AcademyToolDefinition


class AcademyResolver:
    """Resolves tools from Academy catalog with caching and fallback."""

    def __init__(self, catalog_url: Optional[str] = None, cache_ttl_minutes: int = 60):
        self.catalog_url = catalog_url or os.getenv(
            "ACADEMY_CATALOG_URL", "https://academy.stmetro.local/api/v1/catalog"
        )
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self.logger = logging.getLogger(__name__)

        self._cache: Dict[str, List[AcademyToolDefinition]] = {}
        self._cache_timestamp: Optional[datetime] = None

    def resolve_tools(self, tool_group: str = "code_review") -> List[AcademyToolDefinition]:
        """Resolve tools from Academy catalog."""
        # Check cache first
        if self._is_cache_valid() and tool_group in self._cache:
            self.logger.info(f"Using cached tools for group: {tool_group}")
            return self._cache[tool_group]

        # Try to fetch from Academy
        try:
            tools = self._fetch_from_academy(tool_group)
            self._update_cache(tool_group, tools)
            return tools
        except Exception as e:
            self.logger.warning(f"Could not fetch from Academy: {e}, using mock tools")

            # Use cached tools if available
            if tool_group in self._cache:
                self.logger.info("Using stale cached tools")
                return self._cache[tool_group]

            # Fall back to mock tools
            return self._get_mock_tools(tool_group)

    def _fetch_from_academy(self, tool_group: str) -> List[AcademyToolDefinition]:
        """Fetch tools from Academy catalog API."""
        try:
            import aiohttp
            import asyncio

            # For this implementation, we'll use mock data
            # In production, this would make an actual HTTP request
            self.logger.info(f"Fetching tools from Academy: {self.catalog_url}")
            raise NotImplementedError("Academy API integration not yet implemented")

        except ImportError:
            self.logger.warning("aiohttp not available for Academy integration")
            raise

    def _get_mock_tools(self, tool_group: str) -> List[AcademyToolDefinition]:
        """Return mock tools for development/testing."""
        if tool_group == "code_review":
            return [
                AcademyToolDefinition(
                    tool_name="ast_analyzer",
                    tool_group="code_review",
                    version="1.0.0",
                    interface_schema={"input": "file_path", "output": "analysis_result"},
                    capabilities=["syntax_analysis", "complexity_metrics", "structure_parsing"],
                    execution_parameters={"max_complexity": 10, "max_function_lines": 50},
                ),
                AcademyToolDefinition(
                    tool_name="security_scanner",
                    tool_group="code_review",
                    version="1.0.0",
                    interface_schema={"input": "file_content", "output": "security_issues"},
                    capabilities=[
                        "vulnerability_detection",
                        "secret_scanning",
                        "pattern_matching",
                    ],
                    execution_parameters={"scan_depth": "deep"},
                ),
                AcademyToolDefinition(
                    tool_name="pattern_matcher",
                    tool_group="code_review",
                    version="1.0.0",
                    interface_schema={"input": "file_content", "output": "pattern_matches"},
                    capabilities=[
                        "anti_pattern_detection",
                        "code_smell_detection",
                        "duplication_detection",
                    ],
                    execution_parameters={"threshold": "medium"},
                ),
            ]
        return []

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self._cache_timestamp:
            return False
        return datetime.now() - self._cache_timestamp < self.cache_ttl

    def _update_cache(self, tool_group: str, tools: List[AcademyToolDefinition]):
        """Update cache with new tools."""
        self._cache[tool_group] = tools
        self._cache_timestamp = datetime.now()
        self.logger.info(f"Updated cache for tool group: {tool_group}")
