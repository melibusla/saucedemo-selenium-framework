import time

import pytest
from pypdf import PdfReader

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture()
def download_dir(driver, tmp_path, request):
    """Points Chrome's downloads at a fresh temp directory for this test.
    Chrome (headless included) blocks downloads unless explicitly allowed —
    Page.setDownloadBehavior is a Chrome DevTools Protocol command with no
    Firefox equivalent, so it's skipped there (test_generate_pdf_order skips
    itself on Firefox for the same reason)."""
    if request.config.getoption("browser_name") == "chrome":
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": str(tmp_path),
        })
    return tmp_path


def _wait_for_download(directory, timeout=10):
    """Polls `directory` until a fully-downloaded .pdf file appears.
    Downloads are asynchronous — the click that starts one returns
    immediately — and Chrome names an in-progress download with a
    .crdownload suffix until it's done, so we wait for a .pdf to show up
    AND for no .crdownload files to remain."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        entries = list(directory.iterdir())
        in_progress = [f for f in entries if f.suffix == ".crdownload"]
        pdf_files = [f for f in entries if f.suffix == ".pdf"]
        if pdf_files and not in_progress:
            return pdf_files
        time.sleep(0.2)
    raise TimeoutError(f"No completed .pdf download appeared in {directory} within {timeout}s")


def _extract_pdf_text(path):
    """Extracts and returns all text from a PDF file, one page's text after
    another, joined with newlines. This project's PDF is a single page, but
    joining all pages keeps this correct even if that ever changes."""
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() for page in reader.pages)


# CO1 — Complete checkout flow (happy path)
def test_complete_checkout_flow(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    item_total, tax, total = checkout_page.get_summary_totals()
    assert item_total + tax == total, "Order total calculation is incorrect"
    checkout_page.finish()
    assert checkout_page.is_order_complete(), "Order complete page did not load after finishing checkout"

# CO2 — Missing first name
def test_missing_first_name(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="", last_name="Doe", postal_code="12345")
    assert checkout_page.get_error_message() == "Error: First Name is required", "Expected error message for missing first name not displayed"


# CO3 — Missing last name
def test_missing_last_name(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="", postal_code="12345")
    assert checkout_page.get_error_message() == "Error: Last Name is required", "Expected error message for missing last name not displayed"


# CO4 — Missing postal code
def test_missing_postal_code(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="")
    assert checkout_page.get_error_message() == "Error: Postal Code is required", "Expected error message for missing postal code not displayed"


# CO5 — Cancel mid-checkout (cart state should be preserved)
def test_cancel_mid_checkout(driver, checkout_step_one):
    products = checkout_step_one
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=False)
    checkout_page.cancel()
    cart_page = CartPage(driver)
    assert sorted(cart_page.get_item_names()) == sorted(products), "Cart items not preserved after cancelling mid-checkout"


# CO6 — Order total calculation (item prices + tax == displayed total)
def test_order_total_calculation(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    item_total, tax, total = checkout_page.get_summary_totals()
    assert item_total + tax == total, "Order total calculation is incorrect"


# Bonus — cancelling from the overview step (after Continue) lands on the
# inventory page instead of the cart; cart contents should still be intact.
def test_cancel_order_after_calculation(driver, checkout_step_one):
    products = checkout_step_one
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    checkout_page.cancel()
    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()
    assert inventory_page.get_cart_count() == len(products)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    assert sorted(cart_page.get_item_names()) == sorted(products)


# CO7 — Generate PDF order on the confirmation page (triggers a file
# download), then use "Back Home" to return to the product catalog.
def test_generate_pdf_order(driver, request, checkout_step_one, download_dir):
    if request.config.getoption("browser_name") != "chrome":
        pytest.skip(
            "Page.setDownloadBehavior is a Chrome DevTools Protocol command; "
            "no Firefox equivalent is used here."
        )
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    checkout_page.finish()
    checkout_page.generate_pdf_order()

    pdf_files = _wait_for_download(download_dir)
    assert len(pdf_files) == 1, f"Expected exactly one PDF, found {pdf_files}"
    assert pdf_files[0].read_bytes().startswith(b"%PDF"), "Downloaded file is not a valid PDF"

    checkout_page.back_home()
    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded(), "Back Home did not return to the inventory page"


# CO8 — The PDF order receipt's content matches what was actually entered
# and displayed during checkout (shipping info, line items, totals) — not
# just that a PDF got downloaded (that's CO7).
def test_pdf_order_contents_match_checkout(driver, request, checkout_step_one, download_dir):
    if request.config.getoption("browser_name") != "chrome":
        pytest.skip(
            "Page.setDownloadBehavior is a Chrome DevTools Protocol command; "
            "no Firefox equivalent is used here."
        )
    first_name, last_name, postal_code = "John", "Doe", "12345"
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name=first_name, last_name=last_name, postal_code=postal_code, submit=True)

    # Read the expected values off the overview page (step two) BEFORE
    # finishing — once we move to checkout-complete.html these elements
    # are gone. Reading them from the page (instead of hardcoding prices
    # in the test) means the test still works if SauceDemo's catalog
    # prices ever change.
    line_items = checkout_page.get_line_items()
    item_total, tax, total = checkout_page.get_summary_totals()

    checkout_page.finish()
    checkout_page.generate_pdf_order()
    pdf_files = _wait_for_download(download_dir)
    pdf_text = _extract_pdf_text(pdf_files[0])

    assert f"{first_name} {last_name}" in pdf_text, "Shipping name missing or incorrect in PDF"
    assert postal_code in pdf_text, "Postal code missing from PDF"
    for name, price in line_items:
        assert f"{name} {price}" in pdf_text, f"Line item '{name} {price}' missing from PDF"
    assert f"Item total ${item_total:.2f}" in pdf_text, "Item total missing or incorrect in PDF"
    assert f"Tax ${tax:.2f}" in pdf_text, "Tax missing or incorrect in PDF"
    assert f"Total ${total:.2f}" in pdf_text, "Total missing or incorrect in PDF"
