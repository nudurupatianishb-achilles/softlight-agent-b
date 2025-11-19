from pathlib import Path

from .backend import BrowserBackend


def capture_state(backend: BrowserBackend, steps_dir: Path, index: int, label: str) -> Path:
    filename = f"{index:02d}_{label}.png"
    path = steps_dir / filename
    backend.screenshot(path)
    return path
