"""TypeScript-specific code analysis."""

from typing import List, Dict, Any
import re


class TypeScriptProcessor:
    """TypeScript-specific code analysis and processing."""

    def check_type_annotations(self, content: str) -> Dict[str, Any]:
        """Check for type annotation coverage."""
        # Count functions with and without type annotations
        function_pattern = r"function\s+\w+\s*\([^)]*\)\s*:\s*\w+"
        untyped_function_pattern = r"function\s+\w+\s*\([^)]*\)\s*\{"

        typed_functions = len(re.findall(function_pattern, content))
        total_functions = len(re.findall(r"function\s+\w+", content))

        return {
            "typed_functions": typed_functions,
            "total_functions": total_functions,
            "type_coverage": typed_functions / total_functions if total_functions > 0 else 1.0,
        }

    def detect_any_usage(self, content: str) -> List[int]:
        """Detect usage of 'any' type (should be avoided)."""
        lines = content.split("\n")
        any_usage_lines = []

        for i, line in enumerate(lines, 1):
            if re.search(r":\s*any\b", line):
                any_usage_lines.append(i)

        return any_usage_lines
