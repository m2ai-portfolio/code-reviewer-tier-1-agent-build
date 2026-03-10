"""Claude AI interface using Anthropic SDK."""

import os
from typing import Optional, List, Dict, Any
import logging


class ClaudeInterface:
    """Interface to Claude AI via Anthropic SDK."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.logger = logging.getLogger(__name__)

        if not self.api_key:
            self.logger.warning("ANTHROPIC_API_KEY not set, Claude integration disabled")

        try:
            from anthropic import Anthropic

            self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.logger.warning("anthropic package not installed")
            self.client = None

    def analyze_code(
        self, code_snippet: str, context: str, persona_instructions: str
    ) -> Dict[str, Any]:
        """Analyze code using Claude with persona instructions."""
        if not self.client:
            self.logger.warning("Claude client not available, returning mock response")
            return {"analysis": "Claude integration not configured", "suggestions": []}

        try:
            prompt = f"""You are a {persona_instructions}

Context: {context}

Analyze the following code and provide insights:

{code_snippet}

Provide your analysis focusing on:
1. Code quality and maintainability
2. Potential bugs or issues
3. Security concerns
4. Performance implications
5. Best practice recommendations
"""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text if message.content else ""

            return {"analysis": response_text, "suggestions": self._extract_suggestions(response_text)}

        except Exception as e:
            self.logger.error(f"Error calling Claude API: {e}")
            return {"analysis": f"Error: {str(e)}", "suggestions": []}

    def _extract_suggestions(self, analysis_text: str) -> List[str]:
        """Extract actionable suggestions from analysis text."""
        # Simple extraction: look for numbered lists or bullet points
        suggestions = []
        lines = analysis_text.split("\n")

        for line in lines:
            line = line.strip()
            if line and (
                line[0].isdigit()
                or line.startswith("-")
                or line.startswith("*")
                or line.startswith("•")
            ):
                # Clean up the suggestion
                suggestion = line.lstrip("0123456789.-*• ").strip()
                if len(suggestion) > 10:  # Ignore very short lines
                    suggestions.append(suggestion)

        return suggestions[:10]  # Limit to top 10 suggestions
