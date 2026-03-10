"""Abstract Syntax Tree analyzer for Python code."""

import ast
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ComplexityMetric:
    """Complexity metrics for code entity."""

    name: str
    line_number: int
    cyclomatic_complexity: int
    lines_of_code: int
    num_parameters: int
    nested_depth: int


@dataclass
class ASTAnalysisResult:
    """Results from AST analysis."""

    functions: List[ComplexityMetric]
    classes: List[ComplexityMetric]
    total_complexity: int
    max_complexity: int
    anti_patterns: List[Dict[str, Any]]
    imports: List[str]


class ASTAnalyzer:
    """Analyzes Python code using Abstract Syntax Tree parsing."""

    def __init__(self, max_complexity: int = 10, max_function_lines: int = 50):
        self.max_complexity = max_complexity
        self.max_function_lines = max_function_lines

    def analyze_file(self, file_path: str, content: str) -> ASTAnalysisResult:
        """Analyze a Python file and extract metrics."""
        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError as e:
            # Return empty result if file can't be parsed
            return ASTAnalysisResult(
                functions=[],
                classes=[],
                total_complexity=0,
                max_complexity=0,
                anti_patterns=[
                    {
                        "type": "syntax_error",
                        "line": e.lineno,
                        "message": f"Syntax error: {e.msg}",
                    }
                ],
                imports=[],
            )

        functions = []
        classes = []
        imports = []
        anti_patterns = []

        # Analyze top-level entities
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metric = self._analyze_function(node)
                functions.append(metric)

                # Check for anti-patterns
                if metric.cyclomatic_complexity > self.max_complexity:
                    anti_patterns.append(
                        {
                            "type": "high_complexity",
                            "entity": metric.name,
                            "line": metric.line_number,
                            "value": metric.cyclomatic_complexity,
                            "threshold": self.max_complexity,
                        }
                    )

                if metric.lines_of_code > self.max_function_lines:
                    anti_patterns.append(
                        {
                            "type": "long_function",
                            "entity": metric.name,
                            "line": metric.line_number,
                            "value": metric.lines_of_code,
                            "threshold": self.max_function_lines,
                        }
                    )

                if metric.num_parameters > 5:
                    anti_patterns.append(
                        {
                            "type": "too_many_parameters",
                            "entity": metric.name,
                            "line": metric.line_number,
                            "value": metric.num_parameters,
                            "threshold": 5,
                        }
                    )

                if metric.nested_depth > 4:
                    anti_patterns.append(
                        {
                            "type": "deep_nesting",
                            "entity": metric.name,
                            "line": metric.line_number,
                            "value": metric.nested_depth,
                            "threshold": 4,
                        }
                    )

            elif isinstance(node, ast.ClassDef):
                metric = self._analyze_class(node)
                classes.append(metric)

                # Check for god objects
                if metric.lines_of_code > 500:
                    anti_patterns.append(
                        {
                            "type": "god_class",
                            "entity": metric.name,
                            "line": metric.line_number,
                            "value": metric.lines_of_code,
                            "threshold": 500,
                        }
                    )

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.extend(self._extract_imports(node))

        total_complexity = sum(f.cyclomatic_complexity for f in functions)
        max_complexity = max((f.cyclomatic_complexity for f in functions), default=0)

        return ASTAnalysisResult(
            functions=functions,
            classes=classes,
            total_complexity=total_complexity,
            max_complexity=max_complexity,
            anti_patterns=anti_patterns,
            imports=imports,
        )

    def _analyze_function(self, node: ast.FunctionDef) -> ComplexityMetric:
        """Analyze a function node."""
        complexity = self._calculate_complexity(node)
        lines = self._count_lines(node)
        params = len(node.args.args) + len(node.args.posonlyargs) + len(node.args.kwonlyargs)
        nested_depth = self._calculate_nested_depth(node)

        return ComplexityMetric(
            name=node.name,
            line_number=node.lineno,
            cyclomatic_complexity=complexity,
            lines_of_code=lines,
            num_parameters=params,
            nested_depth=nested_depth,
        )

    def _analyze_class(self, node: ast.ClassDef) -> ComplexityMetric:
        """Analyze a class node."""
        complexity = sum(
            self._calculate_complexity(n)
            for n in ast.walk(node)
            if isinstance(n, ast.FunctionDef)
        )
        lines = self._count_lines(node)
        methods = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))

        return ComplexityMetric(
            name=node.name,
            line_number=node.lineno,
            cyclomatic_complexity=complexity,
            lines_of_code=lines,
            num_parameters=methods,  # Store method count here
            nested_depth=0,
        )

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for a node."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(
                child,
                (
                    ast.If,
                    ast.While,
                    ast.For,
                    ast.ExceptHandler,
                    ast.With,
                    ast.Assert,
                    ast.comprehension,
                ),
            ):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _count_lines(self, node: ast.AST) -> int:
        """Count lines of code in a node."""
        if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
            return node.end_lineno - node.lineno + 1
        return 0

    def _calculate_nested_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Calculate maximum nesting depth."""
        max_depth = depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                child_depth = self._calculate_nested_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth

    def _extract_imports(self, node: ast.AST) -> List[str]:
        """Extract import names."""
        imports = []
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        return imports
