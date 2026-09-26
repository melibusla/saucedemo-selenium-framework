# Robot Framework — Selenium keyword-driven tests

Practical exercise applying Robot Framework + SeleniumLibrary to the same
SauceDemo site covered by the main pytest/Page Object suite in this repo.

**Scope:** self-taught, not used in a production environment. Built to
demonstrate familiarity with keyword-driven syntax as a complement to the
Selenium/Python skills shown in the rest of this repository — not a
replacement or a claim of professional RF experience.

## What's covered

- Login + add to cart
- Remove item from cart
- Full checkout flow (custom keyword with arguments)
- Sort products A→Z and Z→A (custom keyword with a FOR loop)

## Structure

- `common.resource` — shared keywords (equivalent role to `conftest.py` +
  Page Objects in the pytest suite, adapted to RF's keyword model)
- `sauce_demo_smoke.robot` — test cases

## Running

```bash
pip install robotframework robotframework-seleniumlibrary
robot --outputdir robot_tests/results robot_tests/
```

Optional headless run:
```bash
robot --outputdir robot_tests/results --variable HEADLESS:True robot_tests/
```

Reports (`log.html`, `report.html`) are generated in `robot_tests/results/`
and gitignored — not committed, regenerate locally to view.