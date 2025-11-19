import argparse
import sys
from typing import Optional, List

from agent import TaskPlanner
from browser import PlaywrightBackend, TaskExecutor


def run_task_for_request(
    app_name: str,
    request: str,
    task_id: str,
    out_dir: str = "dataset",
    headless: bool = False,
) -> None:
    planner = TaskPlanner()
    plan = planner.plan(app_name=app_name, request=request)

    backend = PlaywrightBackend(headless=headless)
    executor = TaskExecutor(backend=backend, out_dir=out_dir)
    executor.run_task(plan, task_id)


def main(argv: Optional[List[str]] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Softlight Agent B runner")
    parser.add_argument(
        "--app",
        default="linear",
        help="App name, e.g. 'linear' or 'notion' (default: 'linear')",
    )
    parser.add_argument(
        "--request",
        default="How do I create a project in Linear?",
        help="Natural language request",
    )
    parser.add_argument(
        "--task-id",
        default="demo_task",
        help="Identifier for this task run (used in dataset folder name)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default: False)",
    )

    args, _unknown = parser.parse_known_args(argv)

    run_task_for_request(
        app_name=args.app,
        request=args.request,
        task_id=args.task_id,
        out_dir="dataset",
        headless=args.headless,
    )


if __name__ == "__main__":
    main()
