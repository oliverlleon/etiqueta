
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the local index.html file
        await page.goto(f"file://{os.getcwd()}/index.html")

        # Click the "Add QR Code" button
        await page.click("#btn-add-qrcode")

        # Wait for the modal to appear
        await page.wait_for_selector("#modal-input", state="visible")

        # Fill in the input field
        await page.fill("#modal-input-field", "https://www.google.com")

        # Click the "Generate" button
        await page.click("#modal-input-submit")

        # Wait for the QR code to be generated
        await page.wait_for_selector(".item-qrcode svg")

        # Take a screenshot
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
