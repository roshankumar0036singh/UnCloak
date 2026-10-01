from playwright.sync_api import sync_playwright


def record_har(url: str, output_path: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_har_path=output_path)
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        # Wait a bit for async XHRs to settle
        page.wait_for_timeout(2000)
        context.close()
        browser.close()
    return output_path
