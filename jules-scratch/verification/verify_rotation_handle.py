
import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    """
    Navigates to the local index.html file, adds a text item,
    clicks it to ensure selection, presses 'Alt' to show the
    rotation handle, and takes a screenshot.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local file
        page.goto(f'file://{file_path}')

        # 1. Add a text item to have something to select
        add_text_button = page.locator('#btn-add-texto')
        add_text_button.click()

        # 2. Get the newly created text item and explicitly click it to select
        text_item = page.locator('.item-texto')
        expect(text_item).to_be_visible()
        text_item.click() # *** FIX: Ensure the item is selected ***

        # 3. Press and hold the 'Alt' key to trigger the handle's appearance
        page.keyboard.down('Alt')

        # 4. Verify that the rotation handle is now visible
        rotate_handle = text_item.locator('.rotate-handle')
        expect(rotate_handle).to_be_visible()

        # 5. Take a screenshot for visual verification
        screenshot_path = 'jules-scratch/verification/rotation_handle_verification.png'
        page.screenshot(path=screenshot_path)

        # Clean up by releasing the key
        page.keyboard.up('Alt')

        browser.close()
        print(f"Screenshot saved to {screenshot_path}")

if __name__ == "__main__":
    run_verification()
