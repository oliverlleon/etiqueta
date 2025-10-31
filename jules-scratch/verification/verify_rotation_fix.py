from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Construct the absolute file path for index.html
        file_path = os.path.abspath('index.html')

        # Go to the local index.html file
        page.goto(f'file://{file_path}')

        # Add a text item to rotate
        page.locator('#btn-add-texto').click()

        # Select the newly added text item
        item_to_rotate = page.locator('.item-arrastavel.item-texto')
        expect(item_to_rotate).to_be_visible()

        # Get the initial transform value
        initial_transform = item_to_rotate.evaluate('element => element.style.transform')

        # Simulate holding the 'Alt' key and rotating
        item_to_rotate.hover()
        page.keyboard.down('Alt')
        page.mouse.down()
        page.mouse.move(200, 200) # Move the mouse to a new position to cause rotation
        page.mouse.up()
        page.keyboard.up('Alt')

        # Get the final transform value
        final_transform = item_to_rotate.evaluate('element => element.style.transform')

        # Assert that the transform has changed (i.e., rotation occurred)
        assert initial_transform != final_transform, "The item did not rotate."

        # Take a screenshot to visually confirm the rotation
        page.screenshot(path="jules-scratch/verification/rotation_fix_proof.png")

        browser.close()

if __name__ == "__main__":
    run()
