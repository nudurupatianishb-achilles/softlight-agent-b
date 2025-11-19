from enum import Enum
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    OPEN_URL = "open_url"
    CLICK = "click"
    FILL = "fill"
    WAIT_FOR = "wait_for"
    SCREENSHOT = "screenshot"


class Step(BaseModel):
    action: ActionType
    description: str
    # Avoid shared mutable defaults
    params: Dict[str, Any] = Field(default_factory=dict)
    capture: bool = False


class TaskPlan(BaseModel):
    app_name: str
    original_request: str
    steps: List[Step]
