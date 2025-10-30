import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local file
        await page.goto(f'file://{file_path}')

        # Take a screenshot of the toolbar area
        await page.locator('#toolbar').screenshot(path='jules-scratch/verification/toolbar.png')
        await page.locator('#left-toolbar').screenshot(path='jules-scratch/verification/left_toolbar.png')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
