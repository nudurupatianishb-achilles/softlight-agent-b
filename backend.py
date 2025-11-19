from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from playwright.sync_api import sync_playwright, Page


class BrowserBackend(ABC):
    """Abstract browser backend interface."""

    @abstractmethod
    def open(self) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def goto(self, url: str) -> None: ...
    @abstractmethod
    def click(self, **locator_params: Any) -> None: ...
    @abstractmethod
    def fill(self, value: str, **locator_params: Any) -> None: ...
    @abstractmethod
    def wait_for(self, selector: str, timeout: int = 5000) -> None: ...
    @abstractmethod
    def screenshot(self, path: Path) -> None: ...
    @property
    @abstractmethod
    def current_url(self) -> str: ...


class PlaywrightBackend(BrowserBackend):
    """Playwright-based implementation for real browser automation."""

    def __init__(self, headless: bool = True) -> None:
        self._play = None
        self._browser = None
        self._page: Optional[Page] = None
        self.headless = headless

    def open(self) -> None:
        self._play = sync_playwright().start()
        self._browser = self._play.chromium.launch(headless=self.headless)
        self._page = self._browser.new_page()

    def close(self) -> None:
        if self._browser:
            self._browser.close()
        if self._play:
            self._play.stop()
        self._browser = None
        self._play = None
        self._page = None

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Backend is not opened. Call open() first.")
        return self._page

    @property
    def current_url(self) -> str:
        return self.page.url

    def goto(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def click(self, **locator_params: Any) -> None:
        from .selectors import find_element
        elem = find_element(self.page, **locator_params)
        elem.click()

    def fill(self, value: str, **locator_params: Any) -> None:
        from .selectors import find_element
        elem = find_element(self.page, **locator_params)
        elem.fill(value)

    def wait_for(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def screenshot(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path), full_page=True)


class MockBackend(BrowserBackend):
    """Simple mock backend for tests (no real browser)."""

    def __init__(self) -> None:
        self._url = "about:blank"

    def open(self) -> None:
        print("[MockBackend] open")

    def close(self) -> None:
        print("[MockBackend] close")

    @property
    def current_url(self) -> str:
        return self._url

    def goto(self, url: str) -> None:
        self._url = url
        print(f"[MockBackend] goto -> {url}")

    def click(self, **locator_params: Any) -> None:
        print(f"[MockBackend] click with {locator_params}")

    def fill(self, value: str, **locator_params: Any) -> None:
        print(f"[MockBackend] fill '{value}' with {locator_params}")

    def wait_for(self, selector: str, timeout: int = 5000) -> None:
        print(f"[MockBackend] wait_for selector={selector}, timeout={timeout}")

    def screenshot(self, path: Path) -> None:
        print(f"[MockBackend] screenshot -> {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(b"mock screenshot")
