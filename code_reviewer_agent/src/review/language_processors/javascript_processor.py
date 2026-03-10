"""JavaScript-specific code analysis."""

from typing import List, Dict, Any
import re


class JavaScriptProcessor:
    """JavaScript-specific code analysis and processing."""

    def check_common_issues(self, content: str) -> List[str]:
        """Check for common JavaScript issues."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for var usage (prefer let/const)
            if re.search(r"\bvar\s+\w+", line):
                issues.append(f"Line {i}: Use 'let' or 'const' instead of 'var'")

            # Check for == instead of ===
            if "==" in line and "===" not in line and "!=" in line and "!==" not in line:
                issues.append(f"Line {i}: Use '===' instead of '=='")

            # Check for console.log (should be removed in production)
            if "console.log" in line:
                issues.append(f"Line {i}: Remove console.log in production code")

        return issues

    def detect_async_patterns(self, content: str) -> Dict[str, Any]:
        """Detect async/await patterns."""
        async_count = len(re.findall(r"\basync\s+function", content))
        await_count = len(re.findall(r"\bawait\s+", content))
        promise_count = len(re.findall(r"\.then\(", content))

        return {
            "async_functions": async_count,
            "await_usage": await_count,
            "promise_chains": promise_count,
            "uses_modern_async": async_count > 0 or await_count > 0,
        }
