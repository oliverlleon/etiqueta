import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        file_path = os.path.abspath('index.html')
        await page.goto(f'file://{file_path}')

        # Add a QR code which will be selected by default
        await page.locator('#btn-add-qrcode').click()
        await page.locator('#modal-input-field').fill('proof')
        await page.locator('#modal-input-submit').click()

        # Press the 'Alt' key to activate rotation mode
        await page.keyboard.down('Alt')

        # Move mouse over the item to show the cursor change (the cursor itself won't be in the screenshot)
        await page.locator('.item-qrcode').hover()

        # Take a screenshot of the whole page
        await page.screenshot(path='jules-scratch/verification/proof.png')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
