from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Obter o caminho absoluto para o arquivo index.html
        file_path = os.path.abspath('index.html')

        # Navegar para o arquivo local
        page.goto(f'file://{file_path}')

        # Esperar um pouco para a página carregar completamente
        page.wait_for_timeout(1000)

        # Tirar a captura de tela
        page.screenshot(path='jules-scratch/verification/verification.png')

        browser.close()

if __name__ == '__main__':
    run()
