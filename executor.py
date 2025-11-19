from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from agent.schema import TaskPlan, Step, ActionType
from .backend import BrowserBackend
from .capture import capture_state
import json


class TaskExecutor:
    """Executes a TaskPlan using a browser backend and captures UI states."""

    def __init__(self, backend: BrowserBackend, out_dir: str = "dataset") -> None:
        self.backend = backend
        self.out_dir = Path(out_dir)

    def run_task(self, plan: TaskPlan, task_id: str) -> None:
        task_dir = self.out_dir / plan.app_name / task_id
        steps_dir = task_dir / "steps"
        steps_dir.mkdir(parents=True, exist_ok=True)

        metadata: Dict[str, Any] = {
            "task_id": task_id,
            "app_name": plan.app_name,
            "original_request": plan.original_request,
            "created_at": datetime.utcnow().isoformat(),
            "steps": [],
        }

        self.backend.open()
        try:
            for idx, step in enumerate(plan.steps, start=1):
                print(f"\n[TaskExecutor] Step {idx}: {step.description} ({step.action.value})")
                self._execute_step(step)

                screenshot_path: Optional[Path] = None
                if step.capture:
                    label = step.params.get("label") or f"step_{idx}"
                    screenshot_path = capture_state(self.backend, steps_dir, idx, label)

                metadata["steps"].append(
                    {
                        "index": idx,
                        "description": step.description,
                        "action": step.action.value,
                        "params": step.params,
                        "url": self.backend.current_url,
                        "screenshot": str(screenshot_path) if screenshot_path else None,
                    }
                )
        finally:
            self.backend.close()

        meta_path = task_dir / "meta.json"
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        print(f"\n[TaskExecutor] Finished task '{task_id}'. Dataset at: {task_dir}")

    def _execute_step(self, step: Step) -> None:
        if step.action == ActionType.OPEN_URL:
            url = step.params["url"]
            self.backend.goto(url)

        elif step.action == ActionType.CLICK:
            self.backend.click(**step.params)

        elif step.action == ActionType.FILL:
            value = step.params.get("value", "")
            params = {k: v for k, v in step.params.items() if k != "value"}
            self.backend.fill(value=value, **params)

        elif step.action == ActionType.WAIT_FOR:
            selector = step.params["selector"]
            timeout = int(step.params.get("timeout", 5000))
            self.backend.wait_for(selector=selector, timeout=timeout)

        elif step.action == ActionType.SCREENSHOT:
            print("[TaskExecutor] Explicit screenshot step (handled by capture_state)")

        else:
            print(f"[TaskExecutor] Unknown action: {step.action}")
