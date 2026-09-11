# Test Coverage Matrix — SauceDemo Automation

20 cases across 4 features. Positive and negative paths are balanced deliberately —
a portfolio built only on happy paths reads as tutorial-following, not test design.

---

## Login (7 cases)

| # | Scenario | Type | Priority | Notes |
|---|---|---|---|---|
| L1 | Valid login (`standard_user`) | Positive | High | Baseline — must pass before any other suite runs |
| L2 | Locked-out user (`locked_out_user`) | Negative | High | Verify the specific lockout error message, not just "login failed" |
| L3 | Empty username | Negative | Medium | Required-field validation |
| L4 | Empty password | Negative | Medium | Required-field validation |
| L5 | Both fields empty | Negative | Low | Edge case combining L3+L4 |
| L6 | Invalid username/password combo | Negative | High | Distinguish from L2 — wrong credentials vs. locked account is a different error path |
| L7 | `performance_glitch_user` login | Positive | Low | Not a functional bug, but worth documenting expected delay so it isn't mistaken for a failure in CI |

## Inventory / Catalog (5 cases)

| # | Scenario | Type | Priority | Notes |
|---|---|---|---|---|
| I1 | Sort by name A–Z | Positive | Medium | Verify actual order, not just that sort ran |
| I2 | Sort by name Z–A | Positive | Medium | |
| I3 | Sort by price low–high | Positive | High | Price sort is more failure-prone than name sort in this app — worth the higher priority |
| I4 | Sort by price high–low | Positive | Medium | |
| I5 | `problem_user` sort behavior | Negative | Medium | This user's sort is intentionally broken — the test should catch that it's broken, and documents *why* a known-bad user is included on purpose |

## Cart (4 cases)

| # | Scenario | Type | Priority | Notes |
|---|---|---|---|---|
| C1 | Add single item to cart | Positive | High | Cart badge count updates correctly |
| C2 | Add multiple items | Positive | High | Badge count reflects total, not just "1" |
| C3 | Remove item from cart | Positive | High | Both from inventory page and cart page, if UI allows both |
| C4 | Cart persists across navigation | Positive | Medium | Add item, navigate away, confirm it's still there — this is the kind of state-consistency bug from your LinkedIn mobile case, applied here |

## Checkout (4 cases)

| # | Scenario | Type | Priority | Notes |
|---|---|---|---|---|
| CO1 | Complete checkout flow (happy path) | Positive | High | End-to-end: cart → info → overview → confirmation |
| CO2 | Missing first name | Negative | High | Required-field validation blocks progression |
| CO3 | Missing last name | Negative | Medium | |
| CO4 | Missing postal code | Negative | Medium | |
| CO5 | Cancel mid-checkout | Negative | Medium | Confirm cart state is preserved, not silently cleared |
| CO6 | Order total calculation | Positive | High | Sum of item prices + tax matches displayed total — this is the case most likely to catch a real business-logic bug, not just a UI issue |

---

## Coverage rationale (for the README's "Design decisions" section)

- **Why these negative cases and not more:** each one maps to a distinct failure mode
  (auth rejection, required-field validation, state persistence, calculation logic)
  rather than multiple variations of the same failure. Depth was prioritized over
  volume.
- **Why `problem_user` and `performance_glitch_user` are included:** they're not just
  "extra" — they demonstrate testing against known-broken and known-slow states on
  purpose, which is closer to real regression testing than only testing the happy
  path.
- **What's out of scope for v1:** cross-browser execution, visual regression, and
  accessibility testing. Noted explicitly in the README as a "not yet" rather than
  an oversight — same principle used for the model-evaluation threshold question in
  interview prep: an honest scope boundary is stronger than pretending it's complete.
