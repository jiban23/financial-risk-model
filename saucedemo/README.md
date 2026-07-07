# SauceDemo — Selenium (Python)

UI tests for [saucedemo.com](https://www.saucedemo.com/) using Selenium + pytest.

## Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Chrome must be installed. Selenium Manager (built into Selenium 4.6+) downloads the
matching `chromedriver` automatically — no manual driver setup needed.

## Run

```powershell
pytest              # visible browser
pytest --headless   # no browser window
pytest -v           # verbose
```
