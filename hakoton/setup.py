from playwright.sync_api import sync_playwright
import time
import os
pe = os.path.abspath('./hakoton/Violentmonkey')
def run(playwright):
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir='./chromium',
        args=[
            f"--disable-extensions-except={pe}",
            f"--load-extension={pe}",
            "--allow-file-access-from-files"
        ],
        headless=False)
    page = browser.new_page()
    page.goto('https://greasyfork.org/en/scripts/492218-twitter-web-exporter')
    time.sleep(2)
    page.locator('a.install-link').click()
    newp = browser.wait_for_event('page')
    time.sleep(2)
    newp.locator('#confirm').click()
    time.sleep(2)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

