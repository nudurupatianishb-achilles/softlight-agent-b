from typing import Any, List

from .schema import TaskPlan, Step, ActionType


class TaskPlanner:
    """Very simple rule-based planner.

    In a production multi-agent system this would call an LLM to convert
    a natural language request into a sequence of generic UI steps.
    """

    def __init__(self, llm_client: Any | None = None) -> None:
        self.llm_client = llm_client

    def plan(self, app_name: str, request: str) -> TaskPlan:
        req_lower = request.lower()
        steps: List[Step] = []

        # Example 1: Linear – create project
        if "linear" in req_lower and "project" in req_lower:
            steps = [
                Step(
                    action=ActionType.OPEN_URL,
                    description="Open Linear workspace",
                    params={"url": "https://linear.app"},
                    capture=True,
                ),
                Step(
                    action=ActionType.CLICK,
                    description="Open Projects section",
                    params={"text": "Projects"},
                    capture=True,
                ),
                Step(
                    action=ActionType.CLICK,
                    description="Click 'Create project' button",
                    params={"text": "Create project"},
                    capture=True,
                ),
                Step(
                    action=ActionType.FILL,
                    description="Fill project name",
                    params={"placeholder": "Name", "value": "Softlight Demo Project"},
                    capture=True,
                ),
                Step(
                    action=ActionType.CLICK,
                    description="Submit project form",
                    params={"text": "Create"},
                    capture=True,
                ),
                Step(
                    action=ActionType.SCREENSHOT,
                    description="Capture success state / created project",
                    params={"label": "project_created"},
                    capture=True,
                ),
            ]

        # Example 2: Notion – filter database (adjust URL to your own DB)
        elif "notion" in req_lower and "filter" in req_lower:
            steps = [
                Step(
                    action=ActionType.OPEN_URL,
                    description="Open Notion workspace (database view)",
                    params={"url": "https://www.notion.so"},
                    capture=True,
                ),
                Step(
                    action=ActionType.CLICK,
                    description="Open database filter menu",
                    params={"text": "Filter"},
                    capture=True,
                ),
                Step(
                    action=ActionType.CLICK,
                    description="Add filter condition",
                    params={"text": "Add filter"},
                    capture=True,
                ),
                Step(
                    action=ActionType.SCREENSHOT,
                    description="Capture filtered database state",
                    params={"label": "filtered_state"},
                    capture=True,
                ),
            ]

        else:
            # Generic fallback plan so the system is always runnable
            steps = [
                Step(
                    action=ActionType.OPEN_URL,
                    description="Open homepage",
                    params={"url": "https://example.com"},
                    capture=True,
                ),
                Step(
                    action=ActionType.SCREENSHOT,
                    description="Capture initial state",
                    params={"label": "initial_state"},
                    capture=True,
                ),
            ]

        return TaskPlan(app_name=app_name, original_request=request, steps=steps)
