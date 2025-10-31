
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the local index.html file
        await page.goto(f"file://{os.getcwd()}/index.html")

        # Check if QRCode is defined in the window scope
        is_qrcode_defined = await page.evaluate("typeof QRCode !== 'undefined'")

        if is_qrcode_defined:
            print("QRCode object is defined. The library is loaded correctly.")
        else:
            print("QRCode object is NOT defined. There is an issue with the library loading.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
