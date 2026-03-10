#!/usr/bin/env python3
"""Validate agent setup and configuration."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def validate_setup():
    """Validate that all components are properly set up."""
    print("=== Code Reviewer Agent - Setup Validation ===\n")

    errors = []
    warnings = []

    # Check Python version
    print("Checking Python version...")
    if sys.version_info < (3, 11):
        errors.append(f"Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check required modules
    print("\nChecking required modules...")
    required_modules = [
        "yaml",
        "git",
        "pydantic",
        "pytest",
    ]

    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            errors.append(f"Missing required module: {module}")
            print(f"  ✗ {module} (missing)")

    # Check project structure
    print("\nChecking project structure...")
    required_dirs = [
        "src/agent",
        "src/tools/code_analyzers",
        "src/review/language_processors",
        "src/models",
        "config/personas",
        "tests/fixtures",
    ]

    base_dir = Path(__file__).parent.parent
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"  ✓ {dir_path}")
        else:
            errors.append(f"Missing directory: {dir_path}")
            print(f"  ✗ {dir_path}")

    # Check configuration files
    print("\nChecking configuration files...")
    config_files = [
        "config/personas/code_reviewer.yaml",
        "config/agent_config.yaml",
        "requirements.txt",
    ]

    for config_file in config_files:
        full_path = base_dir / config_file
        if full_path.exists():
            print(f"  ✓ {config_file}")
        else:
            errors.append(f"Missing config file: {config_file}")
            print(f"  ✗ {config_file}")

    # Try importing core modules
    print("\nChecking core modules...")
    try:
        from src.models.review_models import CodeReviewRequest
        print("  ✓ review_models")
    except Exception as e:
        errors.append(f"Cannot import review_models: {e}")
        print(f"  ✗ review_models")

    try:
        from src.tools.code_analyzers.ast_analyzer import ASTAnalyzer
        print("  ✓ ast_analyzer")
    except Exception as e:
        errors.append(f"Cannot import ast_analyzer: {e}")
        print(f"  ✗ ast_analyzer")

    try:
        from src.review.orchestrator import ReviewOrchestrator
        print("  ✓ orchestrator")
    except Exception as e:
        errors.append(f"Cannot import orchestrator: {e}")
        print(f"  ✗ orchestrator")

    # Check environment variables
    print("\nChecking environment variables...")
    env_vars = {
        "ANTHROPIC_API_KEY": False,  # Optional
        "PERSONA_CONFIG_PATH": False,  # Optional
    }

    for var, required in env_vars.items():
        if os.getenv(var):
            print(f"  ✓ {var} (set)")
        else:
            if required:
                errors.append(f"Missing required environment variable: {var}")
                print(f"  ✗ {var} (required)")
            else:
                warnings.append(f"Optional environment variable not set: {var}")
                print(f"  ○ {var} (optional, not set)")

    # Summary
    print("\n" + "=" * 50)
    if errors:
        print(f"\n❌ Validation FAILED with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ Validation PASSED!")

    if warnings:
        print(f"\n⚠ {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  - {warning}")

    return len(errors) == 0


if __name__ == "__main__":
    success = validate_setup()
    sys.exit(0 if success else 1)
