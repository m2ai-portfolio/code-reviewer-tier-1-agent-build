"""Python-specific code analysis."""

import ast
from typing import List, Dict, Any


class PythonProcessor:
    """Python-specific code analysis and processing."""

    def analyze_imports(self, content: str) -> Dict[str, Any]:
        """Analyze Python imports."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {"error": "Syntax error in Python file"}

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"type": "import", "module": alias.name, "alias": alias.asname})
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append(
                        {
                            "type": "from_import",
                            "module": node.module,
                            "name": alias.name,
                            "alias": alias.asname,
                        }
                    )

        return {"imports": imports, "count": len(imports)}

    def check_pep8_compliance(self, content: str) -> List[str]:
        """Check basic PEP 8 compliance issues."""
        issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check line length (PEP 8: max 79 characters)
            if len(line) > 79:
                issues.append(f"Line {i}: Line too long ({len(line)} > 79 characters)")

            # Check for tabs
            if "\t" in line:
                issues.append(f"Line {i}: Uses tabs instead of spaces")

            # Check for trailing whitespace
            if line and line != line.rstrip():
                issues.append(f"Line {i}: Trailing whitespace")

        return issues

    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(
                    {
                        "name": node.name,
                        "line": node.lineno,
                        "args": len(node.args.args),
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                    }
                )

        return functions

    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                classes.append({"name": node.name, "line": node.lineno, "methods": methods})

        return classes
