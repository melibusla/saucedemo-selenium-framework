# SauceDemo Selenium Framework

![tests](https://github.com/melibusla/saucedemo-selenium-framework/actions/workflows/tests.yml/badge.svg)

A Selenium + Python test automation framework for [SauceDemo](https://www.saucedemo.com),
built as a portfolio project while transitioning from manual QA (8 years) into
automation QA. It covers the full e-commerce flow — login, catalog, cart, and
checkout — with both positive and negative test cases, chosen deliberately
rather than padded for volume.

## Coverage

25 cases across 4 features. Full detail, priorities, and per-case rationale
are in [`Test_Coverage_Matrix.md`](Test_Coverage_Matrix.md).

| Feature | Cases | Highlights |
|---|---|---|
| Login | L1–L8 | Lockout vs. bad-credentials distinction, required-field validation, `performance_glitch_user` timing, a manually-found visual-overflow bug in the error banner (L8) |
| Inventory / Catalog | I1–I5 | All four sort orders verified by actual result order, plus `problem_user`'s broken sort caught on purpose (`xfail`, I5) |
| Cart | C1–C4 | Add/remove from both inventory and cart pages, badge count accuracy, persistence across navigation |
| Checkout | CO1–CO8 | Happy path through order confirmation, required-field validation, cancel-mid-checkout state preservation, order total calculation, PDF receipt download and content verification |

Two known-broken/known-slow users (`problem_user`, `performance_glitch_user`)
are tested on purpose, not skipped — see the matrix's "Coverage rationale"
section for why.

## Tech stack

- Python + Selenium WebDriver (Selenium 4, Selenium Manager — no manual
  driver management)
- pytest + pytest-html
- Page Object Model
- `pypdf` for verifying downloaded PDF receipt content
- GitHub Actions CI, matrixed across `ubuntu-latest` and `windows-latest`

## Running locally

```bash
pip install -r requirements.txt
```

```bash
pytest --browser_name chrome --html=reports/report.html
```

`--browser_name` also accepts `firefox`. Tests run headless by default.

## CI

Every push and pull request runs the full suite headless on GitHub Actions
across `ubuntu-latest` and `windows-latest` (`.github/workflows/tests.yml`).

## Design decisions

**Why Page Object Model.** Each page (`LoginPage`, `InventoryPage`,
`CartPage`, `ProductPage`, `CheckoutPage`) owns its own locators and
interactions; tests never call Selenium directly. When the site's markup
changes, the fix happens in one place instead of in every test that touches
that element.

**Why these specific negative cases.** Each negative case maps to a distinct
failure mode — auth rejection, field validation, state persistence, order
calculation — instead of being a variation on the same failure repeated with
different inputs. Depth over volume.

**Why `problem_user` and `performance_glitch_user` are included.** They
demonstrate testing against known-broken and known-slow states on purpose,
which is closer to real regression testing than only exercising the happy
path.

**What's out of scope for v1.** Cross-browser *parallel* execution beyond the
CI OS matrix, general visual-regression tooling (screenshot diffing, pixel
comparison), and accessibility testing. This is a stated boundary, not an
oversight — L8 is the one deliberate exception: a targeted regression test
for a specific layout bug found during manual exploration, not part of a
visual-regression suite. An accessibility observation on the login error
icon (WCAG 1.4.1, "use of color") was noted during that same exploration and
deferred to a future pass rather than folded into v1's scope.

**A CI-only flake worth documenting.** Headless Chrome on this site has a
quirk where native `.click()` and `send_keys()` calls can silently stop
registering whenever `document.hasFocus()` is `False` — most often right
after a same-page click or navigation, and more easily triggered on slower
CI runners than locally. Affected page-object methods force an element into
focus via JavaScript before interacting with it, and checkout field entry
additionally waits for the typed value to actually land in the DOM before
proceeding. It's the kind of intermittent, hard-to-reproduce-locally failure
that's common in real CI pipelines, not a code smell in the framework.
