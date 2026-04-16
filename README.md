We are given a specification for a project called "Code Reviewer - Tier 1 Agent Build".
 We are to generate a README.md that follows the exact structure and rules provided.

 Steps:
 1. We are to write a one-line tagline from the spec (plain-speak description) for the banner block.
    Since the plain-speak description was not provided, we must write a concise one-liner from the spec.
    Looking at the spec, the project is an autonomous Claude-powered agent for code review.
    We can use: "Autonomous Claude-powered agent for senior-level code quality engineering and review."

 2. The "Problem this solves" is provided in the spec under "Problem Statement":
    "The Code Reviewer persona currently operates in manual mode, requiring human initiation and guidance for each review session. To enable seamless integration into CI/CD pipelines and provide continuous code quality assurance, this persona must be promoted to autonomous agent status with self-contained operation capabilities and dynamic tool resolution from the Academy catalog."

 3. We must follow the exact section order and content rules.

 Let's break down the sections:

 Section 1: Centered Banner Block (HTML)
   We are given the exact HTML to use, but note: the h3 must use the plain-speak description (our one-liner).

 Section 2: What is this?
   2-3 sentences explaining what the tool does and who it's for, plus a code block with command and output.

 Section 3: Problem
   Use the provided problem statement (lightly edited for grammar).

 Section 4: Features
   A markdown table with two columns: Feature | Description. 4-8 rows.

 Section 5: Quick Start
   Numbered steps: clone, install, first command.

 Section 6: Examples
   2-3 concrete usage examples, each with bold title, command, and realistic output.

 Section 7: File Structure
   Cleaned up file tree from the provided one.

 Section 8: Tech Stack
   Compact markdown table: Technology | Purpose.

 Section 9: Contributing
   Brief: fork, edit, test, PR (4 lines max).

 Section 10: License
   MIT

 Section 11: Author
   Given: Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)

 Quality Rules:
   - Examples must show both input and output (no placeholders).
   - Use realistic data.
   - Feature table rows must describe actual capabilities from the code/spec.
   - Total length 150-250 lines.
   - No em-dashes.

 Let's create each section.

 Note: We are to output raw markdown only, no code fences around the entire output.

 Important: The banner block uses HTML and we are to use the plain-speak description in the h3.

 Implementation:

 1. Banner Block:
    We are given:
      <p align="center">
        <img src="assets/infographic.png" alt="Code Reviewer - Tier 1 Agent Build" width="800">
      </p>

      <h3 align="center">USE THE PLAIN-SPEAK DESCRIPTION PROVIDED ABOVE -- DO NOT INVENT</h3>

    But we are to replace the h3 content with our one-liner.

    However, note: the spec says "Plain-speak description (use this verbatim as the one-line tagline in the banner block -- do NOT invent a new tagline)".
    Since it was not provided, we invented one from the spec: "Autonomous Claude-powered agent for senior-level code quality engineering and review."

    But wait: the spec says "do NOT invent a new tagline" and then says "(not provided -- write a concise one-liner from the spec)".
    So we are allowed to write one from the spec.

    Let's use: "Autonomous Claude-powered agent for senior-level code quality engineering and review."

 2. What is this?
    We'll write 2-3 sentences and then a code block.

    Example: 
      The Code Reviewer agent is an autonomous AI-powered tool that performs senior-level code reviews 
      by analyzing code patterns, security vulnerabilities, and architectural compliance. 
      It integrates with the ST Metro ecosystem to provide continuous code quality assurance in CI/CD pipelines.

      Usage example:
        $ code-reviewer --repo https://github.com/example/project --output markdown
        [Realistic output: a markdown report showing quality score, issues, and suggestions]

 3. Problem: Use the provided problem statement (lightly edited for grammar).

    Original: 
      "The Code Reviewer persona currently operates in manual mode, requiring human initiation and guidance for each review session. To enable seamless integration into CI/CD pipelines and provide continuous code quality assurance, this persona must be promoted to autonomous agent status with self-contained operation capabilities and dynamic tool resolution from the Academy catalog."

    We can leave it as is or lightly edit for grammar. It's already good.

 4. Features: We need 4-8 rows.

    From the spec, we have:
      - Persona Configuration Loading
      - Academy Tool Catalog Integration
      - Autonomous Code Repository Analysis

    We can break down the core features into more specific ones or use the three and add one more from the spec.

    Looking at the spec, we also have:
      - Review Orchestrator (with sub-features: Code Pattern Analyzer, Security Scan Engine, Architecture Compliance Check)
      - Report Generation (Quality Score Report, Issue Classifications, Remediation Suggestions, Architecture Feedback)

    Let's pick 4-8 from the detailed features in the spec.

    We'll choose:
      Feature 1: Persona Configuration Loading -> Dynamically loads Senior Code Quality Engineer persona from YAML to guide analysis.
      Feature 2: Academy Tool Catalog Integration -> Resolves and loads code review tools from ST Metro Academy catalog without hardcoded dependencies.
      Feature 3: Multi-dimensional Code Analysis -> Analyzes code patterns, security vulnerabilities, and architectural compliance using AST and specialized tools.
      Feature 4: Autonomous Repository Operations -> Clones repositories and performs incremental analysis for large codebases.
      Feature 5: Configurable Review Orchestration -> Adjusts analysis depth and parallelism via environment variables for performance tuning.
      Feature 6: Structured Report Generation -> Outputs detailed reviews in JSON, Markdown, or YAML with quality scores and actionable feedback.

    That's 6 features.

 5. Quick Start:
    Steps:
      1. Clone the repository: `git clone <repo-url>`
      2. Install dependencies: `pip install -r requirements.txt` (or use pyproject.toml with pip install .)
      3. Set environment variables (ANTHROPIC_API_KEY, PERSONA_CONFIG_PATH, ACADEMY_CATALOG_URL)
      4. Run the agent: `python -m code_reviewer_agent --repo <repository-url>`

    But note: the file tree shows an `init.sh` and a `pyproject.toml`. We can use:
        Step 1: git clone
        Step 2: cd into the directory and run `pip install -e .` (if it's a package) or `pip install -r requirements.txt`
        Step 3: Set up .env file or export variables
        Step 4: Run the agent via a script or module.

    Looking at the file tree, there's an `init.sh` in the root and in the code_reviewer_agent directory? Actually, the root has init.sh and the code_reviewer_agent directory also has one? 
    But the root file tree shows:
        init.sh
        pyproject.toml
        requirements.txt

    So we can do:
        1. git clone [repository-url]
        2. cd Code-Reviewer-Tier-1-Agent-Build
        3. pip install -r requirements.txt   (or pip install -e . if using pyproject.toml)
        4. Copy .env.example to .env and fill in the required variables
        5. Run: python -m code_reviewer_agent.src.agent.core_engine   (but we don't know the exact entry point)

    However, the spec says to use actual package/command names from the file tree and spec.

    The file tree shows a `code_reviewer_agent` directory at the root? Actually, the root has:
        metroplex-academy-promo-code-reviewer-1772558138632/
          ... and then inside: code_reviewer_agent, config, screenshots, src, tests, etc.

    But the root of the project (as per the file tree) is the directory named "metroplex-academy-promo-code-reviewer-1772558138632", which is not very nice.

    However, in the README we are to use the project title: "Code Reviewer - Tier 1 Agent Build", so we assume the repository is named accordingly.

    Let's assume the repository is named "code-reviewer-tier-1-agent-build".

    Steps for Quick Start:
      1. Clone the repo: `git clone https://github.com/your-org/code-reviewer-tier-1-agent-build.git`
      2. cd code-reviewer-tier-1-agent-build
      3. Install dependencies: `pip install -r requirements.txt`
      4. Configure: copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY`, `PERSONA_CONFIG_PATH`, `ACADEMY_CATALOG_URL`
      5. Run a review: `python -m code_reviewer_agent --repo https://github.com/example/python-project --format markdown`

    But note: the file tree shows a `src` directory at the same level as `code_reviewer_agent`? Actually, the root has both:
        code_reviewer_agent/   (which seems to be the main package) and
        src/                   (which also has agent, models, review, etc.)

    This is confusing. Looking again:

        metroplex-academy-promo-code-reviewer-1772558138632/
          ├── assets
          ├── code_reviewer_agent   [this is a directory]
          │   ├── config
          │   ├── scripts
          │   ├── src
          │   ├── tests
          │   ├── .env.example
          │   ├── init.sh
          │   ├── pyproject.toml
          │   └── requirements.txt
          ├── config
          ├── screenshots
          ├── src                   [another src directory?]
          ├── tests
          ├── ... (files at root)

    This seems duplicated. But note: the spec says to clean up the file tree.

    We are to use the provided file tree but clean it up.

    Let's look at the provided file tree again and remove noise.

    We see two sets of similar directories: one under `code_reviewer_agent` and one at the root (src, tests). 
    The root also has a `code_reviewer_agent` directory that contains its own src, tests, etc.

    It appears the project might be structured with the main package in `code_reviewer_agent` and the root having some additional configuration.

    However, for the sake of the README, we are to show a cleaned up file tree.

    We'll focus on the `code_reviewer_agent` directory as the main source, and note that the root has config and screenshots.

    But the Quick Start should work from the root of the repository.

    Given the complexity, we'll assume the entry point is in the `code_reviewer_agent` directory.

    The `code_reviewer_agent` directory has:
        pyproject.toml
        requirements.txt
        init.sh
        and a src directory inside it.

    So likely, the package is installed from `code_reviewer_agent`.

    Steps:
        1. git clone <repo>
        2. cd code-reviewer-tier-1-agent-build   [assuming the repo name is changed to something readable]
        3. cd code_reviewer_agent
        4. pip install -r requirements.txt
        5. Set environment variables (or copy .env.example to .env and edit)
        6. Run: python -m src.agent.core_engine --help   (or whatever the entry point is)

    However, we don't have the exact entry point. The spec doesn't specify.

    We can look for a main function or a script. The `scripts` directory has `validate_setup.py`, but that's for validation.

    Alternatively, the `init.sh` might be the setup script.

    Since we don't have exact details, we'll make a reasonable assumption.

    Let's say the agent is run by:
        python -m code_reviewer_agent.agent.core_engine   [if installed] 
        or from the code_reviewer_agent directory: python -m src.agent.core_engine

    But note: the `code_reviewer_agent` directory has a `src` inside it.

    We'll write:

        1. Clone the repository:
           git clone https://github.com/your-organization/code-reviewer-tier-1-agent-build.git
        2. Navigate to the project directory:
           cd code-reviewer-tier-1-agent-build
        3. Install dependencies:
           cd code_reviewer_agent
           pip install -r requirements.txt
        4. Configure the agent:
           cp .env.example .env
           Edit .env to set ANTHROPIC_APIKEY, PERSONA_CONFIG_PATH, and ACADEMY_CATALOG_URL
        5. Run your first code review:
           python -m src.agent.core_engine --repo https://github.com/example/python-project --output-format markdown

    However, the spec says to use actual package/command names. We are using `src.agent.core_engine` which is present.

 6. Examples:
    We need 2-3 examples, each with:
        - Bold title
        - Command
        - Realistic output

    Example 1: Basic repository review
        **Basic Code Review**
        $ code-reviewer --repo https://github.com/open-source/project --output json
        {
          "quality_score": 8.7,
          "issues": [
            {
              "id": "SEC-001",
              "severity": "high",
              "message": "Potential SQL injection in user_login.py:45",
              "suggestion": "Use parameterized queries instead of string concatenation."
            }
          ],
          "architecture_feedback": "Consider moving business logic to service layer for better separation of concerns."
        }

    Example 2: Focused security scan
        **Security-Focused Analysis**
        $ code-reviewer --repo https://github.com/example/app --patterns security --threshold high
        Security Scan Complete
        ----------------------
        High Severity Issues Found: 2
        - [CRITICAL] Hardcoded API key in config/settings.py:12
        - [HIGH] Insecure deserialization in api/v1/data.py:87
        Recommendations: 
          1. Move API keys to environment variables or secret management service.
          2. Replace pickle with JSON for data serialization in trusted contexts.

    Example 3: Incremental review (if supported)
        **Incremental Review for Pull Request**
        $ code-reviewer --pr 123 --base main --output markdown
        # Code Review Report for PR #123
        ## Summary
        Quality Score: 9.2/10 (No new critical issues)
        ## New Issues
        None
        ## Improved Areas
        - Fixed: Removed unused import in utils/helpers.py (previously flagged)
        ## Recommendations
        - Consider adding type hints to the new functions in models/user.py

    But note: we don't know if the agent supports PRs. The spec says it can do repository or targeted file sets.

    We'll stick to repository and file set examples.

    However, the spec says: "Execute multi-dimensional code analysis using AST parsing and pattern recognition" and "Support incremental analysis for large codebases with change-focused reviews".

    So incremental is a feature.

    Let's do:
        Example 1: Full repository review (JSON output)
        Example 2: Security-only review (Markdown output)
        Example 3: Incremental review since last commit (YAML output)

 7. File Structure:
    We are to clean up the provided file tree.

    Provided file tree (root of the repo):

        metroplex-academy-promo-code-reviewer-1772558138632/
          ├── assets
          │   └── infographic.png
          ├── code_reviewer_agent
          │   ├── config
          │   │   ├── personas
          │   │   │   └── code_reviewer.yaml
          │   │   └── agent_config.yaml
          │   ├── scripts
          │   │   └── validate_setup.py
          │   ├── src
          │   │   ├── agent
          │   │   │   ├── __init__.py
          │   │   │   ├── claude_interface.py
          │   │   │   ├── core_engine.py
          │   │   │   └── persona_loader.py
          │   │   ├── models
          │   │   │   ├── __init__.py
          │   │   │   ├── academy_models.py
          │   │   │   ├── persona.py
          │   │   │   └── review_models.py
          │   │   ├── review
          │   │   │   ├── language_processors
          │   │   │   ├── __init__.py
          │   │   │   ├── orchestrator.py
          │   │   │   ├── report_generator.py
          │   │   │   └── repository_handler.py
          │   │   ├── tools
          │   │   │   ├── code_analyzers
          │   │   │   ├── __init__.py
          │   │   │   └── academy_resolver.py
          │   │   └── __init__.py
          │   ├── tests
          │   │   ├── fixtures
          │   │   │   ├── sample_repositories
          │   │   │   └── __init__.py
          │   │   ├── integration
          │   │   │   └── __init__.py
          │   │   ├── __init__.py
          │   │   ├── test_academy_integration.py
          │   │   ├── test_code_analysis.py
          │   │   ├── test_persona_loading.py
          │   │   └── test_review_generation.py
          │   ├── .env.example
          │   ├── init.sh
          │   ├── pyproject.toml
          │   └── requirements.txt
          ├── config
          │   ├── personas
          │   │   └── code_reviewer.yaml
          │   └── agent_config.yaml
          ├── screenshots
          │   ├── M2A-178-test-results.png
          │   ├── M2A-182-implementation-summary.txt
          │   ├── M2A-182-json-report.json
          │   ├── M2A-182-markdown-report.md
          │   ├── M2A-182-qa-results.txt
          │   ├── M2A-182-sample-report.json
          │   ├── M2A-182-sample-report.md
          │   ├── M2A-182-test-results.txt
          │   ├── M2A-182-verification-complete.txt
          │   └── M2A-182-verification-summary.txt
          ├── src
          │   ├── agent
          │   │   ├── __init__.py
          │   │   ├── core_engine.py
          │   │   └── persona_loader.py
          │   ├── models
          │   │   ├── __init__.py
          │   │   ├── persona.py
          │   │   └── review_models.py
          │   ├── review
          │   │   ├── __init__.py
          │   │   └── report_generator.py
          │   └── __init__.py
          ├── tests
          │   ├── fixtures
          │   │   └── test_personas
          │   │       ├── invalid_weights.yaml
          │   │       ├── malformed.yaml
          │   │       ├── missing_fields.yaml
          │   │       ├── security_focused.yaml
          │   │       └── valid_persona.yaml
          │   ├── __init__.py
          │   ├── test_persona_loading.py
          │   └── test_review_generation.py
          ├── .claude_settings.json
          ├── .codebase_learnings.json
          ├── .gitignore
          ├── .linear_project.json
          ├── .parallel_plan.json
          ├── README.md
          ├── app_spec.txt
          ├── init.sh
          ├── pyproject.toml
          └── requirements.txt

    We are to clean it up: remove noise, group logically, add inline comments for key files.

    Noise files: 
        .claude_settings.json, .codebase_learnings.json, .gitignore, .linear_project.json, .parallel_plan.json, app_spec.txt, and the duplicate init.sh, pyproject.toml, requirements.txt at root? 
        Also, the screenshots directory (though we might keep one example image? but the banner uses assets/infographic.png).

    We note:
        - The root has a `code_reviewer_agent` directory that seems to be the main package (with its own src, tests, config, etc.)
        - The root also has a `config`, `screenshots`, `src`, `tests` directories and some files.

    This looks like a monorepo or a mistake. But the spec says to clean up.

    We'll assume that the `code_reviewer_agent` directory is the main project and the rest are either duplicates or auxiliary.

    However, the root has a `config` directory with personas and agent_config, and the `code_reviewer_agent` also has a config.

    To avoid confusion, we'll present the cleaned up tree as:

        Code Reviewer - Tier 1 Agent Build/
          code_reviewer_agent/          # Main package source
            src/                        # Python source code
              agent/                    # Agent core logic
                claude_interface.py     # Claude API integration
                core_engine.py          # Main agent orchestration
                persona_loader.py       # Loads persona configuration from YAML
              models/                   # Data models
                academy_models.py       # Academy tool catalog interfaces
                persona.py              # Persona configuration model
                review_models.py        # Review request/response models
              review/                   # Review execution components
                orchestrator.py         # Coordinates analysis modules
                report_generator.py     # Formats review results
                repository_handler.py   # Git operations and file traversal
              tools/                    # Tool resolution and analysis
                academy_resolver.py     # Dynamically loads tools from Academy catalog
                code_analyzers/         # Language-specific analyzers (if any)
            config/                     # Configuration files
              personas/
                code_reviewer.yaml      # Default persona configuration
              agent_config.yaml         # Agent runtime settings
            tests/                      # Test suite
              fixtures/                 # Test data
              test_academy_integration.py
              test_code_analysis.py
              test_persona_loading.py
              test_review_generation.py
            scripts/
              validate_setup.py         # Environment validation script
            .env.example                # Environment variable template
            init.sh                     # Setup script
            pyproject.toml              # Project dependencies and metadata
            requirements.txt            # Pip dependencies (if not using pyproject)
          config/                       # Global configuration (optional overrides)
            personas/
              code_reviewer.yaml
            agent_config.yaml
          screenshots/                  # Example reports and visuals
            M2A-182-sample-report.md
            M2A-182-sample-report.json
          assets/
            infographic.png             # Banner image
          README.md
          # Note: Other files like .gitignore, etc., are omitted for clarity.

    But note: the root also has a `src` and `tests` at the top level. We are omitting them because they appear to be duplicates or less important? 
    However, the spec says to use the provided file tree but clean it up.

    Alternatively, we might consider that the root `src` and `tests` are the actual source and the `code_reviewer_agent` is a misnomer? 
    But the `code_reviewer_agent` directory has a lot of detailed structure.

    Given the time, we'll go with the `code_reviewer_agent` as the main source and note that the root has some configuration and screenshots.

    We'll write the file tree as:

        Code Reviewer - Tier 1 Agent Build/
          code_reviewer_agent/          # Core agent implementation
            src/                        # Source code
              ... (as above)
          config/                       # Configuration files (can be overridden by code_reviewer_agent/config)
          screenshots/                  # Example outputs
          assets/                       # Images and media
          README.md

    And then we list the key files under code_reviewer_agent/src and code_reviewer_agent/config.

    But to be precise, we'll show:

        Code Reviewer - Tier 1 Agent Build/
          ├── code_reviewer_agent/
          │   ├── src/
          │   │   ├── agent/
          │   │   │   ├── __init__.py
          │   │   │   ├── claude_interface.py
          │   │   │   ├── core_engine.py
          │   │   │   └── persona_loader.py
          │   │   ├── models/
          │   │   │   ├── __init__.py
          │   │   │   ├── academy_models.py
          │   │   │   ├── persona.py
          │   │   │   └── review_models.py
          │   │   ├── review/
          │   │   │   ├── __init__.py
          │   │   │   ├── orchestrator.py
          │   │   │   ├── report_generator.py
          │   │   │   └── repository_handler.py
          │   │   ├── tools/
          │   │   │   ├── __init__.py
          │   │   │   ├── academy_resolver.py
          │   │   │   └── code_analyzers/
          │   │   └── __init__.py
          │   ├── config/
          │   │   ├── personas/
          │   │   │   └── code_reviewer.yaml
          │   │   └── agent_config.yaml
          │   ├── tests/
          │   │   ├── fixtures/
          │   │   │   └── sample_repositories/
          │   │   ├── test_academy_integration.py
          │   │   ├── test_code_analysis.py
          │   │   ├── test_persona_loading.py
          │   │   └── test_review_generation.py
          │   ├── scripts/
          │   │   └── validate_setup.py
          │   ├── .env.example
          │   ├── init.sh
          │   ├── pyproject.toml
          │   └── requirements.txt
          ├── config/
          │   ├── personas/
          │   │   └── code_reviewer.yaml   # Example: can override the one in code_reviewer_agent/config
          │   └── agent_config.yaml
          ├── screenshots/
          │   ├── M2A-182-sample-report.md
          │   └── M2A-182-sample-report.json
          └── assets/
              └── infographic.png

    We'll add comments for key files as inline comments in the tree.

 8. Tech Stack:
    From the spec:
        - Python 3.11+ with anthropic SDK for Claude Sonnet integration
        - YAML parsing with PyYAML for persona configuration loading
        - Tool resolution system interfacing with Academy tool group catalog
        - Asyncio for concurrent code analysis operations
        - Git integration