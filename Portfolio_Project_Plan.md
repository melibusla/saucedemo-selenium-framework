# Portfolio Automation Project — Plan

Working notes. September 2026. Target: public GitHub repo demonstrating automation
capability, built while transitioning from manual QA to automation.

**Repo:** https://github.com/melibusla/saucedemo-selenium-framework

---

## 1. Target site

**SauceDemo** (https://www.saucedemo.com) — chosen over "The Internet" because it's a
complete e-commerce flow (login → catalog → cart → checkout) rather than disconnected
feature demos. It also ships with users built for negative testing:

| User | Purpose |
|---|---|
| `standard_user` | Happy path baseline |
| `locked_out_user` | Account lockout scenario |
| `problem_user` | UI intentionally broken (images, sort) |
| `performance_glitch_user` | Simulated slowness |

---

## 2. Tech stack

- **Language:** Python
- **Automation library:** Selenium WebDriver (current course)
- **Test runner:** pytest — not unittest, because it's the industry standard and the
  same runner used with Playwright in Python. Business-logic test code carries over
  almost unchanged when migrating to Playwright later; only the driver calls change.
- **Design pattern:** Page Object Model — one file per page (`LoginPage`,
  `InventoryPage`, `CartPage`, `CheckoutPage`), tests kept separate from page logic.
- **CI:** GitHub Actions — a simple workflow (`.github/workflows/tests.yml`) that
  installs dependencies and runs `pytest` on every push. No need for anything more
  elaborate; the goal is proving the suite runs somewhere other than a local machine.

---

## 3. Repo structure (draft)

```
saucedemo-selenium-framework/
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── conftest.py          # fixtures: driver setup/teardown, base URL
├── requirements.txt
├── .github/
│   └── workflows/
│       └── tests.yml
└── README.md
```

---

## 4. README requirements

Written in English. Must include:

- What was tested and why — the coverage matrix (see companion file), not just a list
  of test names.
- How to run the suite locally.
- CI status badge.
- A short "Design decisions" section: why Page Object Model, why these specific
  negative cases and not others. This is what distinguishes the repo from a copied
  course exercise — it shows reasoning, not just execution.

---

## 5. Status

- [x] Finish Selenium + Python course (Rahul Shetty Academy) — done
- [x] Write test coverage matrix — see `Test_Coverage_Matrix.md`
- [x] Create new repo on GitHub — https://github.com/melibusla/saucedemo-selenium-framework (separate from `python-selenium-practice`, which stays as the course/practice repo)
- [x] Scaffold repo structure
- [ ] Implement Page Objects — `LoginPage` complete; `InventoryPage.is_loaded()`
      done (needed for login assertions), rest of Inventory/Cart/Checkout still
      stubs
- [ ] Implement test cases against the matrix — Login suite done (L1-L8, 10
      passing tests, incl. L8 bug found during manual exploration); Inventory,
      Cart, Checkout not started
- [ ] Set up GitHub Actions
- [ ] Write README
- [ ] Publish repo, link from CV and LinkedIn
- [ ] Later: migrate/extend with Playwright once that course is underway
