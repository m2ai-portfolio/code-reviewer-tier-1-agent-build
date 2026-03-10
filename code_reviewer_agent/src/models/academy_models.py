"""Academy tool integration data models."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AcademyToolDefinition:
    """Definition of a tool from Academy catalog."""

    tool_name: str
    tool_group: str
    version: str
    interface_schema: Dict
    capabilities: List[str]
    execution_parameters: Dict
