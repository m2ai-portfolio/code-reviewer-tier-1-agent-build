"""Java-specific code analysis."""

from typing import List, Dict, Any
import re


class JavaProcessor:
    """Java-specific code analysis and processing."""

    def check_naming_conventions(self, content: str) -> List[str]:
        """Check Java naming conventions."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check class names (should be PascalCase)
            class_match = re.search(r"class\s+([a-z]\w*)", line)
            if class_match:
                issues.append(
                    f"Line {i}: Class name '{class_match.group(1)}' should start with uppercase"
                )

            # Check constants (should be UPPER_SNAKE_CASE)
            const_match = re.search(r"static\s+final\s+\w+\s+([a-z]\w*)", line)
            if const_match:
                issues.append(f"Line {i}: Constant '{const_match.group(1)}' should be UPPER_CASE")

        return issues

    def detect_null_checks(self, content: str) -> Dict[str, Any]:
        """Detect null check patterns."""
        null_checks = len(re.findall(r"if\s*\([^)]*==\s*null", content))
        null_pointer_safe = len(re.findall(r"Optional<", content))

        return {"null_checks": null_checks, "optional_usage": null_pointer_safe}
