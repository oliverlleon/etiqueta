from playwright.sync_api import sync_playwright, expect
import os
import re

def get_transform_values(transform_string):
    """Helper function to parse translate and rotate values from a CSS transform string."""
    translate_match = re.search(r'translate\(([^,]+)px, ([^,]+)px\)', transform_string)
    rotate_match = re.search(r'rotate\((.+)deg\)', transform_string)

    x = float(translate_match.group(1)) if translate_match else 0
    y = float(translate_match.group(2)) if translate_match else 0
    angle = float(rotate_match.group(1)) if rotate_match else 0

    return x, y, angle

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Capture and print console messages
        page.on("console", lambda msg: print(f"Browser Console: {msg.text()}"))

        file_path = os.path.abspath('index.html')
        page.goto(f'file://{file_path}')

        # 1. Add a text item
        page.locator('#btn-add-texto').click()
        item = page.locator('.item-arrastavel.item-texto')
        expect(item).to_be_visible()

        page.wait_for_timeout(500)

        # 2. Drag the item to a new position (using relative move)
        start_box = item.bounding_box()
        item.hover()
        page.mouse.down()
        page.mouse.move(start_box['x'] + 150, start_box['y'] + 150)
        page.mouse.up()

        transform1 = item.evaluate('el => el.style.transform')
        x1, y1, angle1 = get_transform_values(transform1)
        assert x1 > 10 and y1 > 10, f"Item did not drag correctly. Final position: ({x1}, {y1})"

        # 3. Rotate the item
        print("\n--- Starting First Rotation ---")
        item.hover()
        page.keyboard.down('Alt')
        page.mouse.down()
        page.mouse.move(start_box['x'] + 250, start_box['y'] + 250)
        page.mouse.up()
        page.keyboard.up('Alt')
        print("--- Finished First Rotation ---\n")

        transform2 = item.evaluate('el => el.style.transform')
        x2, y2, angle2 = get_transform_values(transform2)
        assert angle2 != angle1, "Item did not rotate on the first attempt."
        assert abs(x2 - x1) < 1 and abs(y2 - y1) < 1, "Item position changed during rotation."

        # 4. Rotate the item a second time
        print("\n--- Starting Second Rotation ---")
        item.hover()
        page.keyboard.down('Alt')
        page.mouse.down()
        page.mouse.move(start_box['x'] + 150, start_box['y'] + 250)
        page.mouse.up()
        page.keyboard.up('Alt')
        print("--- Finished Second Rotation ---\n")

        transform3 = item.evaluate('el => el.style.transform')
        x3, y3, angle3 = get_transform_values(transform3)
        assert angle3 != angle2, "Item did not rotate on the second attempt."

        # 5. Drag the item again to confirm movement is restored
        drag_again_box = item.bounding_box()
        item.hover()
        page.mouse.down()
        page.mouse.move(drag_again_box['x'] + 50, drag_again_box['y'] + 50)
        page.mouse.up()

        transform4 = item.evaluate('el => el.style.transform')
        x4, y4, angle4 = get_transform_values(transform4)
        assert x4 != x3 or y4 != y3, "Item did not resume dragging after rotation."
        assert abs(angle4 - angle3) < 1, "Item rotated when it should have dragged."

        # 6. Take final screenshot
        page.screenshot(path="jules-scratch/verification/rotation_final_proof.png")

        browser.close()
        print("Verification successful: Drag -> Rotate -> Rotate -> Drag sequence works correctly.")

if __name__ == "__main__":
    run()
