import asyncio
from playwright.sync_api import sync_playwright, Page, expect
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the index.html file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Assuming the script is in jules-scratch/verification, so we go up two levels
        base_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
        file_path = f"file://{os.path.join(base_dir, 'index.html')}"

        page.goto(file_path)

        # Add three text items to trigger the multi-selection state
        add_text_button = page.locator("#btn-add-texto")
        add_text_button.click()
        add_text_button.click()
        add_text_button.click()

        # Select all three items using Shift + Click
        items = page.locator(".item-arrastavel")
        items.nth(0).click()
        items.nth(1).click(modifiers=["Shift"])
        items.nth(2).click(modifiers=["Shift"])

        # Wait for the alignment and layering toolbars to be visible
        alignment_toolbar = page.locator("#alignment-toolbar")
        layering_toolbar = page.locator("#layering-toolbar")

        expect(alignment_toolbar).to_be_visible()
        expect(layering_toolbar).to_be_visible()

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

run_verification()
