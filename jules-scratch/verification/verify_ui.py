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

        # Verify the new "Salvar" (Save) button is present
        save_button = page.locator('button[title="Salvar etiqueta"]')
        expect(save_button).to_be_visible()

        # Verify the new "Abrir" (Open) button is present
        open_button = page.locator('button[title="Abrir etiqueta"]')
        expect(open_button).to_be_visible()

        # Verify the shape tool icon is present using the corrected selector
        shape_tool = page.locator('#left-toolbar .select-wrapper .select-icon')
        expect(shape_tool).to_have_text('category')

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/proof.png")

        browser.close()

if __name__ == "__main__":
    run()
