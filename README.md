# Metroplex Academy - Code Reviewer Agent

## Overview

An autonomous Claude-powered agent for code quality review within the ST Metro ecosystem. This intelligent system analyzes code repositories, identifies issues, and generates structured review reports with actionable feedback.

## Tech Stack

- **Python**: 3.11+
- **Core Dependencies**:
  - PyYAML - YAML configuration parsing
  - anthropic SDK - Claude AI integration
  - asyncio - Asynchronous operations
  - GitPython - Git repository analysis
  - Pydantic - Data validation and schemas
  - pytest - Testing framework

## Features

1. **Persona Config Loading** - Load and manage reviewer personas from YAML configuration files
2. **Academy Tool Catalog Integration** - Integrate with ST Metro Academy's tool ecosystem
3. **Autonomous Code Repository Analysis** - Automatically analyze code repositories for quality metrics
4. **Multi-Language Quality Assessment** - Evaluate code quality across multiple programming languages
5. **Structured Review Report Generation** - Generate comprehensive, actionable review reports in structured formats

## Setup Instructions

To set up the development environment, run:

```bash
bash init.sh
```

This script will:
- Verify Python 3.11+ is installed
- Create a virtual environment
- Install all required dependencies from requirements.txt
- Display the successful completion message

Once setup is complete, you can run tests with:

```bash
python -m pytest tests/
```

## Development

Ensure you have Python 3.11+ installed before running the init.sh script. The virtual environment will be created in the `venv/` directory.
