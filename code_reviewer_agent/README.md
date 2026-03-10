# Code Reviewer Agent

Autonomous code quality assessment agent powered by Claude AI, performing comprehensive multi-dimensional analysis of code repositories.

## Overview

This agent provides automated code review capabilities with:
- **Security vulnerability detection** (SQL injection, hardcoded secrets, dangerous functions)
- **Code quality analysis** (complexity metrics, anti-patterns, maintainability)
- **Multi-language support** (Python, JavaScript, TypeScript, Java, Go)
- **Configurable persona** with customizable review standards
- **Detailed reporting** in JSON and Markdown formats

## Features

### Core Analysis Capabilities

1. **AST-Based Analysis**
   - Cyclomatic complexity calculation
   - Function and class metrics
   - Deep nesting detection
   - Long function/god class identification

2. **Security Scanning**
   - Hardcoded credentials detection
   - SQL injection patterns
   - Dangerous function usage (eval, exec)
   - Weak cryptography detection
   - Path traversal vulnerabilities

3. **Pattern Matching**
   - Magic numbers and strings
   - Duplicate code detection
   - Commented-out code
   - Missing docstrings
   - Mutable default arguments

4. **Quality Metrics**
   - Overall quality score (0-100)
   - Category-specific scores (security, maintainability, performance, style, documentation)
   - Weighted scoring based on persona configuration

## Installation

```bash
# Clone or navigate to the project
cd code_reviewer_agent

# Run setup script
chmod +x init.sh
./init.sh

# Verify installation
venv/bin/python scripts/validate_setup.py
```

## Quick Start

```python
from src.models.review_models import CodeReviewRequest
from src.review.orchestrator import ReviewOrchestrator
from src.review.report_generator import ReportGenerator

# Initialize orchestrator
orchestrator = ReviewOrchestrator()

# Create review request
request = CodeReviewRequest(
    file_paths=["path/to/code.py"],
    target_branch="main",
    review_scope="targeted",
    output_format="json",
)

# Execute review
report = orchestrator.execute_review(request)

# Generate report
generator = ReportGenerator()
generator.save_report(report, "review_report.md", format="markdown")

print(f"Overall Score: {report.quality_metrics.overall_score}/100")
print(f"Found {len(report.findings)} issues")
```

## Configuration

### Persona Configuration

Edit `config/personas/code_reviewer.yaml` to customize review behavior:

```yaml
review_standards:
  security_weight: 0.30
  maintainability_weight: 0.30
  performance_weight: 0.15
  style_consistency_weight: 0.15
  documentation_weight: 0.10

quality_thresholds:
  minimum_acceptable_score: 70.0
  critical_issue_threshold: 0
  complexity_warning_level: 10
```

### Environment Variables

```bash
ANTHROPIC_API_KEY=your_api_key_here  # Optional: for Claude integration
PERSONA_CONFIG_PATH=config/personas/code_reviewer.yaml
MAX_FILE_SIZE_KB=500
CONCURRENT_REVIEWS=3
```

## Testing

```bash
# Run all tests
venv/bin/python -m pytest tests/ -v

# Run specific test suites
venv/bin/python -m pytest tests/test_code_analysis.py -v
venv/bin/python -m pytest tests/test_review_generation.py -v
venv/bin/python -m pytest tests/test_persona_loading.py -v
```

## Architecture

```
┌─────────────────────────────────────────┐
│        Review Orchestrator             │
├─────────────────────────────────────────┤
│  ┌────────────┐  ┌──────────────────┐  │
│  │ Repository │  │   Code Analyzers │  │
│  │  Handler   │  │   - AST Analyzer │  │
│  └────────────┘  │   - Security     │  │
│                  │   - Patterns     │  │
│                  │   - Metrics      │  │
│                  └──────────────────┘  │
└─────────────────────────────────────────┘
              │
              ▼
    ┌────────────────────┐
    │   Review Report    │
    │  - Quality Metrics │
    │  - Findings        │
    │  - Recommendations │
    └────────────────────┘
```

## Project Structure

```
code_reviewer_agent/
├── src/
│   ├── agent/              # Agent core (persona, Claude interface)
│   ├── tools/              # Analysis tools
│   │   └── code_analyzers/ # AST, security, patterns, metrics
│   ├── review/             # Review orchestration
│   │   └── language_processors/  # Language-specific analysis
│   └── models/             # Data models
├── config/                 # Configuration files
│   └── personas/          # Persona YAML files
├── tests/                  # Test suite
│   └── fixtures/          # Test data
├── scripts/               # Utility scripts
└── requirements.txt       # Dependencies
```

## Example Output

```
--- Quality Metrics ---
Overall Score:        47.95/100
Security Score:       10.0/100
Maintainability:      34.0/100
Performance:          95.0/100
Style:                100.0/100
Documentation:        55.0/100

--- Findings Summary ---
Critical: 3
High:     1
Medium:   6
Low:      30
Total:    40

--- Recommendations ---
1. Address 3 critical security vulnerabilities immediately
2. Review and implement security best practices across the codebase
3. Refactor complex functions to improve maintainability
4. Add docstrings to public functions and classes
```

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please ensure all tests pass before submitting PRs.
