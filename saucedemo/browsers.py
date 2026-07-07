"""Shared cross-browser WebDriver factory.

Used by the browser_compatibility/ and login/ suites so the browser setup lives
in one place. Chrome and Edge use Selenium Manager to auto-provision drivers.
Firefox startup can be slow on first launch, so creation is retried. Opera is
Chromium-based and driven through chromedriver with binary_location pointed at
the Opera executable.
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

SUPPORTED = ["chrome", "firefox", "edge", "opera"]

_OPERA_CANDIDATES = [
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\opera.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\launcher.exe"),
    r"C:\Program Files\Opera\opera.exe",
    r"C:\Program Files (x86)\Opera\opera.exe",
]


def _find_opera():
    return next((p for p in _OPERA_CANDIDATES if os.path.exists(p)), None)


def _build(name, headless):
    if name == "chrome":
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        return webdriver.Chrome(options=opts)

    if name == "edge":
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        return webdriver.Edge(options=opts)

    if name == "firefox":
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        return webdriver.Firefox(options=opts)

    if name == "opera":
        opera_bin = _find_opera()
        if not opera_bin:
            raise RuntimeError("Opera is not installed on this machine")
        opts = ChromeOptions()
        opts.binary_location = opera_bin
        if headless:
            opts.add_argument("--headless=new")
        return webdriver.Chrome(options=opts)

    raise ValueError(f"Unknown browser: {name!r}")


def new_driver(name, headless, retries=2):
    """Create a driver, retrying transient startup failures (e.g. slow Firefox).

    Raises the last exception if every attempt fails, so the caller can decide
    whether to skip (browser genuinely unavailable) or fail.
    """
    last_error = None
    for _ in range(retries + 1):
        try:
            return _build(name, headless)
        except Exception as exc:  # noqa: BLE001 - retry any startup failure
            last_error = exc
    raise last_error
