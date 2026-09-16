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
  (`LoginPage`, `InventoryPage`, `CartPage`, `ProductPage`, `CheckoutPage`).
  Tests in `tests/` never call Selenium directly; they call page object
  methods.
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

`InventoryPage` (sort, product listing, add/remove to cart, cart badge count)
and `CartPage` are implemented. Inventory sort tests I1-I5 pass (I5 is
`xfail`-marked, documenting `problem_user`'s broken sort on purpose). Cart
tests C1-C4 (add single/multiple items, remove item from both the inventory
and cart pages, cart persists across navigation) all pass. `ProductPage`
(product detail page: add/remove to cart, back to products) is implemented,
used by C4. `CheckoutPage` and all of `test_checkout.py` (CO1-CO6) are still
stubs with `# TODO` markers matching their matrix case IDs.

`InventoryPage.add_to_cart(product_name)` takes the product's visible name
and builds its `data-test` selector directly (lowercase, spaces to hyphens)
— don't reintroduce a multi-candidate "guess the selector" fallback here.

**Known headless-Chrome click quirk on this site:** a native WebDriver
`.click()` can silently stop registering (no exception, handler just
doesn't fire) whenever `document.hasFocus()` is `False` — this happens both
after ~10s of page idle and right after a same-page click/navigation (e.g.
clicking "Continue Shopping" right after clicking the cart icon). Any
page-object method that clicks something right after a prior click in the
same test is a candidate for this. Fixed by clicking via
`self.driver.execute_script("arguments[0].click();", element)` instead of
`element.click()` — already applied to `CartPage.remove_item`,
`CartPage.continue_shopping`, `CartPage.go_to_checkout`, `CartPage.click_item`,
`InventoryPage.go_to_cart`, and `ProductPage.back_to_products`.
`InventoryPage.add_to_cart` is the one exception still on a native click
since it always fires right after page load, before any other click. If a
new click-based method starts intermittently "succeeding" without producing
the expected DOM change, apply the same JS-click fix rather than
re-debugging from scratch — see memory `project_headless_click_idle_quirk`
for the full writeup.

`conftest.py`'s `driver` fixture does **not** set a global implicit wait —
it was removed because it made any "assert element is absent" check pay the
full timeout. Page objects use an explicit `WebDriverWait` inside the
specific method that needs to wait (see `LoginPage.get_error_message()` and
`InventoryPage.is_loaded()` as examples). Follow that pattern in new page
objects rather than reintroducing `driver.implicitly_wait()`.
