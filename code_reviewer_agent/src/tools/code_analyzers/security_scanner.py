"""Security vulnerability scanner."""

import ast
import re
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SecurityIssue:
    """Represents a security vulnerability."""

    vulnerability_type: str
    line_number: int
    severity: str
    description: str
    evidence: str
    remediation: str


class SecurityScanner:
    """Scans code for security vulnerabilities."""

    def __init__(self):
        # Regex patterns for common security issues
        self.secret_patterns = [
            (r"password\s*=\s*['\"][^'\"]{4,}['\"]", "hardcoded_password"),
            (r"api[_-]?key\s*=\s*['\"][^'\"]{10,}['\"]", "hardcoded_api_key"),
            (r"secret\s*=\s*['\"][^'\"]{8,}['\"]", "hardcoded_secret"),
            (r"token\s*=\s*['\"][^'\"]{10,}['\"]", "hardcoded_token"),
            (
                r"['\"][A-Za-z0-9+/]{40,}={0,2}['\"]",
                "potential_base64_secret",
            ),  # Base64 encoded secrets
        ]

        self.sql_injection_patterns = [
            (r"execute\s*\([^)]*%s[^)]*\)", "sql_string_formatting"),
            (r"execute\s*\([^)]*\+[^)]*\)", "sql_concatenation"),
            (r"\.format\s*\([^)]*\)\s*INTO", "sql_format_injection"),
        ]

        self.dangerous_functions = [
            "eval",
            "exec",
            "__import__",
            "compile",
            "open",
            "input",
        ]

    def scan_file(self, file_path: str, content: str) -> List[SecurityIssue]:
        """Scan a file for security vulnerabilities."""
        issues = []

        # Pattern-based scanning
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            issues.extend(self._scan_line_patterns(line, i))

        # AST-based scanning for Python files
        if file_path.endswith(".py"):
            try:
                tree = ast.parse(content, filename=file_path)
                issues.extend(self._scan_ast(tree, lines))
            except SyntaxError:
                pass  # Skip AST analysis for files with syntax errors

        return issues

    def _scan_line_patterns(self, line: str, line_number: int) -> List[SecurityIssue]:
        """Scan a line for pattern-based vulnerabilities."""
        issues = []

        # Check for hardcoded secrets
        for pattern, vuln_type in self.secret_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        vulnerability_type=vuln_type,
                        line_number=line_number,
                        severity="critical",
                        description=f"Hardcoded secret detected: {vuln_type.replace('_', ' ')}",
                        evidence=line.strip(),
                        remediation="Use environment variables or secure credential management systems",
                    )
                )

        # Check for SQL injection patterns
        for pattern, vuln_type in self.sql_injection_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        vulnerability_type=vuln_type,
                        line_number=line_number,
                        severity="critical",
                        description="Potential SQL injection vulnerability",
                        evidence=line.strip(),
                        remediation="Use parameterized queries or prepared statements",
                    )
                )

        # Check for insecure random
        if re.search(r"random\.(random|randint|choice)", line):
            issues.append(
                SecurityIssue(
                    vulnerability_type="weak_random",
                    line_number=line_number,
                    severity="medium",
                    description="Use of non-cryptographic random function",
                    evidence=line.strip(),
                    remediation="Use secrets module for security-sensitive operations",
                )
            )

        # Check for weak cryptography
        if re.search(r"hashlib\.(md5|sha1)", line):
            issues.append(
                SecurityIssue(
                    vulnerability_type="weak_hash",
                    line_number=line_number,
                    severity="high",
                    description="Use of weak cryptographic hash function",
                    evidence=line.strip(),
                    remediation="Use SHA-256 or stronger hash algorithms",
                )
            )

        # Check for shell injection
        if re.search(r"os\.system|subprocess\.call.*shell\s*=\s*True", line):
            issues.append(
                SecurityIssue(
                    vulnerability_type="shell_injection",
                    line_number=line_number,
                    severity="critical",
                    description="Potential shell injection vulnerability",
                    evidence=line.strip(),
                    remediation="Avoid shell=True, use list arguments instead",
                )
            )

        # Check for path traversal
        if re.search(r"open\s*\([^)]*\+[^)]*\)", line):
            issues.append(
                SecurityIssue(
                    vulnerability_type="path_traversal",
                    line_number=line_number,
                    severity="high",
                    description="Potential path traversal vulnerability",
                    evidence=line.strip(),
                    remediation="Validate and sanitize file paths, use os.path.join()",
                )
            )

        return issues

    def _scan_ast(self, tree: ast.AST, lines: List[str]) -> List[SecurityIssue]:
        """Scan AST for security vulnerabilities."""
        issues = []

        for node in ast.walk(tree):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node.func)
                if func_name in self.dangerous_functions:
                    line_num = node.lineno
                    evidence = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                    severity = "critical" if func_name in ["eval", "exec"] else "high"
                    issues.append(
                        SecurityIssue(
                            vulnerability_type=f"dangerous_function_{func_name}",
                            line_number=line_num,
                            severity=severity,
                            description=f"Use of dangerous function: {func_name}()",
                            evidence=evidence,
                            remediation=f"Avoid using {func_name}(), consider safer alternatives",
                        )
                    )

            # Check for assert statements in production code
            elif isinstance(node, ast.Assert):
                line_num = node.lineno
                evidence = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                issues.append(
                    SecurityIssue(
                        vulnerability_type="assert_in_production",
                        line_number=line_num,
                        severity="low",
                        description="Assert statement can be disabled with -O flag",
                        evidence=evidence,
                        remediation="Use proper exception handling instead of assert",
                    )
                )

            # Check for broad exception catching
            elif isinstance(node, ast.ExceptHandler):
                if node.type is None or (
                    isinstance(node.type, ast.Name) and node.type.id == "Exception"
                ):
                    line_num = node.lineno
                    evidence = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                    issues.append(
                        SecurityIssue(
                            vulnerability_type="broad_exception",
                            line_number=line_num,
                            severity="low",
                            description="Catching broad exception may hide errors",
                            evidence=evidence,
                            remediation="Catch specific exceptions",
                        )
                    )

        return issues

    def _get_function_name(self, node: ast.AST) -> str:
        """Extract function name from call node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""
