# Project context for Claude Code

This file is read automatically by Claude Code sessions in this repo. Keep it
updated as the project evolves — it's the only context Claude Code has here;
it does not share memory with claude.ai conversations.

## What this is

Portfolio project demonstrating Selenium + Python automation skills, built while
transitioning from manual QA (8 years, Avature) to automation QA. Target site:
https://www.saucedemo.com. This is a from-scratch demonstration repo, separate
from `python-selenium-practice` (the course exercises repo).

## Environment

- **OS: Ubuntu (Linux).** Never suggest Windows/Mac-specific paths, drivers, or
  syntax. Course examples (Rahul Shetty Academy) are often macOS/Windows and need
  adaptation.
- Selenium 4.x with **Selenium Manager** — no `Service` object, no
  `webdriver_manager`, no manual chromedriver. Just pass `options` to
  `webdriver.Chrome()`.
- Linux-specific ChromeOptions: `--no-sandbox` and `--disable-dev-shm-usage`
  are required (instructor examples on macOS don't need these).
- pytest, not unittest. `pytest-html` for reports.
- Uses system-level Python packages or a project venv (`.venv/`) — check
  `requirements.txt`, don't assume global installs.

## Tech stack & structure

- **Design pattern:** Page Object Model — one class per page in `pages/`
  (`LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`). Tests in `tests/`
  never call Selenium directly; they call page object methods.
- **Why POM:** a locator only needs to change in one place when the site
  changes, instead of in every test that touches that element.
- **Data-driven tests:** JSON files under `data/`, parsed as lists of dicts,
  used with `pytest.mark.parametrize`. Optional fields (e.g. `expected_error`)
  should be read with `.get()`, not `[...]`, since not every row has them.
- **conftest.py:** `driver` fixture, `--browser_name` CLI flag (chrome/firefox),
  headless + Linux flags applied conditionally via `os.environ.get("CI")`.
- **CI:** GitHub Actions (`.github/workflows/tests.yml`), runs pytest headless
  on every push.

## Test coverage matrix (see `Test_Coverage_Matrix.md`)

20 cases across Login (L1-L7), Inventory/Catalog (I1-I5), Cart (C1-C4), and
Checkout (CO1-CO6). Test function names should stay traceable to these IDs
(see comments in each `tests/test_*.py` file). Negative cases are deliberate —
each maps to a distinct failure mode (auth rejection, field validation, state
persistence, calculation logic), not repeated variations of the same one.
Known-broken/known-slow users (`problem_user`, `performance_glitch_user`) are
tested on purpose, not skipped.

## Conventions and preferences

- **No overselling.** Don't write comments, docstrings, or README content that
  claims something works if it hasn't been implemented and run yet. "In
  progress" beats a confident claim that turns out wrong in an interview.
- **Understand-before-copy.** Every method should be explainable in a technical
  interview without sounding memorized. If a suggested solution feels like
  "magic," prefer the simpler version that's fully understood, even if it's
  less elegant.
- **Multi-line terminal commands** often paste as a single line for Melina —
  prefer breaking multi-step instructions into individual commands run one at
  a time, rather than one large heredoc or chained command.
- Communication in Argentine Spanish (voseo) is fine and preferred if Claude
  Code is asked in Spanish.

## Current status

Check `Portfolio_Project_Plan.md`'s status checklist for the authoritative
state. As of the last update: Login page object and tests are complete —
L1-L8, 10 passing test cases (L8 is a manually-found visual-overflow bug in
the error banner, added as a documented exception to the "visual regression
out of scope" rule; see `Test_Coverage_Matrix.md`'s scope note). An
accessibility observation on the login fields' error icon was deliberately
deferred to v2, also noted there.

`InventoryPage.is_loaded()` is implemented (needed to assert successful
login); everything else in Inventory/Cart/Checkout is still stubs with
`# TODO` markers matching their matrix case IDs.

`conftest.py`'s `driver` fixture does **not** set a global implicit wait —
it was removed because it made any "assert element is absent" check pay the
full timeout. Page objects use an explicit `WebDriverWait` inside the
specific method that needs to wait (see `LoginPage.get_error_message()` and
`InventoryPage.is_loaded()` as examples). Follow that pattern in new page
objects rather than reintroducing `driver.implicitly_wait()`.
