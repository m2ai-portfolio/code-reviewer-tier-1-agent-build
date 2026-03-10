"""Code pattern matcher for detecting anti-patterns."""

import ast
import re
from dataclasses import dataclass
from typing import List, Set, Dict
from collections import defaultdict


@dataclass
class PatternMatch:
    """Represents a matched code pattern."""

    pattern_type: str
    line_number: int
    description: str
    evidence: str
    suggestion: str


class PatternMatcher:
    """Detects code anti-patterns and smells."""

    def __init__(self):
        self.magic_number_threshold = 3

    def analyze_file(self, file_path: str, content: str) -> List[PatternMatch]:
        """Analyze file for code patterns."""
        matches = []
        lines = content.split("\n")

        # Pattern-based analysis
        matches.extend(self._detect_dead_code(lines))
        matches.extend(self._detect_duplicate_code(lines))
        matches.extend(self._detect_magic_numbers(lines))
        matches.extend(self._detect_commented_code(lines))

        # AST-based analysis for Python files
        if file_path.endswith(".py"):
            try:
                tree = ast.parse(content, filename=file_path)
                matches.extend(self._detect_unused_imports(tree, lines))
                matches.extend(self._detect_missing_docstrings(tree, lines))
                matches.extend(self._detect_mutable_defaults(tree, lines))
            except SyntaxError:
                pass

        return matches

    def _detect_dead_code(self, lines: List[str]) -> List[PatternMatch]:
        """Detect potentially dead code."""
        matches = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Unreachable code after return
            if i > 1 and "return" in lines[i - 2] and stripped and not stripped.startswith("#"):
                if not any(
                    keyword in stripped
                    for keyword in ["def ", "class ", "if ", "elif ", "else:", "except"]
                ):
                    matches.append(
                        PatternMatch(
                            pattern_type="unreachable_code",
                            line_number=i,
                            description="Potentially unreachable code after return statement",
                            evidence=stripped,
                            suggestion="Remove unreachable code or restructure logic",
                        )
                    )

        return matches

    def _detect_duplicate_code(self, lines: List[str]) -> List[PatternMatch]:
        """Detect duplicate code blocks."""
        matches = []
        line_hashes: Dict[str, List[int]] = defaultdict(list)

        # Find lines that appear multiple times
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if len(stripped) > 20 and not stripped.startswith("#"):
                line_hashes[stripped].append(i)

        # Report significant duplicates
        for line_content, line_numbers in line_hashes.items():
            if len(line_numbers) >= 3:  # Line appears 3+ times
                matches.append(
                    PatternMatch(
                        pattern_type="duplicate_code",
                        line_number=line_numbers[0],
                        description=f"Code duplicated {len(line_numbers)} times",
                        evidence=line_content[:80],
                        suggestion="Extract to a function or constant",
                    )
                )

        return matches

    def _detect_magic_numbers(self, lines: List[str]) -> List[PatternMatch]:
        """Detect magic numbers and strings."""
        matches = []

        # Common non-magic numbers to ignore
        ignore_numbers = {0, 1, -1, 2, 10, 100, 1000}

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip comments and imports
            if stripped.startswith("#") or "import" in stripped:
                continue

            # Find numeric literals
            numbers = re.findall(r"\b(\d+)\b", stripped)
            for num in numbers:
                num_int = int(num)
                if num_int not in ignore_numbers and "range(" not in stripped:
                    matches.append(
                        PatternMatch(
                            pattern_type="magic_number",
                            line_number=i,
                            description=f"Magic number {num} should be a named constant",
                            evidence=stripped[:80],
                            suggestion="Define as a constant with descriptive name",
                        )
                    )
                    break  # Only report once per line

            # Find string literals (potential magic strings)
            strings = re.findall(r"['\"]([^'\"]{15,})['\"]", stripped)
            for string in strings:
                if not any(
                    keyword in stripped
                    for keyword in ["print(", "log", "raise", "assert", "return"]
                ):
                    matches.append(
                        PatternMatch(
                            pattern_type="magic_string",
                            line_number=i,
                            description="Long string literal should be a constant",
                            evidence=stripped[:80],
                            suggestion="Define as a constant or configuration value",
                        )
                    )
                    break

        return matches

    def _detect_commented_code(self, lines: List[str]) -> List[PatternMatch]:
        """Detect commented-out code."""
        matches = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                # Check if it looks like code (contains common code patterns)
                comment_content = stripped[1:].strip()
                code_indicators = [
                    "def ",
                    "class ",
                    "import ",
                    "return ",
                    "if ",
                    "for ",
                    "while ",
                    " = ",
                    "self.",
                ]

                if any(indicator in comment_content for indicator in code_indicators):
                    matches.append(
                        PatternMatch(
                            pattern_type="commented_code",
                            line_number=i,
                            description="Commented-out code should be removed",
                            evidence=stripped[:80],
                            suggestion="Remove commented code, use version control instead",
                        )
                    )

        return matches

    def _detect_unused_imports(self, tree: ast.AST, lines: List[str]) -> List[PatternMatch]:
        """Detect unused imports (simplified detection)."""
        matches = []
        imports: Dict[str, int] = {}

        # Collect all imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node.lineno

        # Simple heuristic: check if import name appears elsewhere in code
        content = "\n".join(lines)
        for import_name, line_num in imports.items():
            # Count occurrences (should be > 1 if used, 1 is just the import itself)
            pattern = r"\b" + re.escape(import_name) + r"\b"
            occurrences = len(re.findall(pattern, content))

            if occurrences <= 1:  # Only the import line
                evidence = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                matches.append(
                    PatternMatch(
                        pattern_type="unused_import",
                        line_number=line_num,
                        description=f"Import '{import_name}' appears to be unused",
                        evidence=evidence,
                        suggestion="Remove unused import",
                    )
                )

        return matches

    def _detect_missing_docstrings(self, tree: ast.AST, lines: List[str]) -> List[PatternMatch]:
        """Detect missing docstrings in functions and classes."""
        matches = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Skip private methods and simple properties
                if node.name.startswith("_") and not node.name.startswith("__"):
                    continue

                # Check if it has a docstring
                has_docstring = (
                    ast.get_docstring(node) is not None
                    or (
                        len(node.body) > 0
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[0].value.value, str)
                    )
                )

                if not has_docstring:
                    evidence = lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                    entity_type = "Class" if isinstance(node, ast.ClassDef) else "Function"
                    matches.append(
                        PatternMatch(
                            pattern_type="missing_docstring",
                            line_number=node.lineno,
                            description=f"{entity_type} '{node.name}' missing docstring",
                            evidence=evidence,
                            suggestion="Add docstring describing purpose and parameters",
                        )
                    )

        return matches

    def _detect_mutable_defaults(self, tree: ast.AST, lines: List[str]) -> List[PatternMatch]:
        """Detect mutable default arguments."""
        matches = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        evidence = lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                        matches.append(
                            PatternMatch(
                                pattern_type="mutable_default",
                                line_number=node.lineno,
                                description="Mutable default argument (list/dict/set)",
                                evidence=evidence,
                                suggestion="Use None as default and initialize inside function",
                            )
                        )
                        break

        return matches
