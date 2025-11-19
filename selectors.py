from playwright.sync_api import Page


def find_element(
    page: Page,
    text: str | None = None,
    placeholder: str | None = None,
    role: str | None = None,
    selector: str | None = None,
    **_: object,
):
    """Generic locator strategy using semantic cues.

    Tries (in order):
      - text content
      - placeholder
      - ARIA role + name
      - raw CSS selector
    """
    if text:
        loc = page.get_by_text(text, exact=False)
        if loc.count():
            return loc.first

    if placeholder:
        loc = page.get_by_placeholder(placeholder)
        if loc.count():
            return loc.first

    if role and text:
        loc = page.get_by_role(role, name=text)
        if loc.count():
            return loc.first

    if selector:
        loc = page.locator(selector)
        if loc.count():
            return loc.first

    raise RuntimeError(
        f"Could not find element for params: "
        f"text={text!r}, placeholder={placeholder!r}, role={role!r}, selector={selector!r}"
    )
