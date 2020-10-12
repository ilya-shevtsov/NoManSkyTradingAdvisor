import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dayzi\AppData\Local\Tesseract-OCR\tesseract.exe'


def main():
    screenshot_name = "Buying.png"
    system_name = get_system_name(screenshot_name)
    item_name = get_item_name(screenshot_name)
    item_price = get_item_price(screenshot_name)
    print(item_name[:-2], system_name[:-2], item_price[:-2])


def get_system_name(screenshot_name):
    screenshot = Image.open(screenshot_name).convert('LA')
    width = screenshot.width
    height = screenshot.height
    left = 343
    top = 940
    right = width - 1100
    bottom = height - 81
    img_crop = screenshot.crop((left, top, right, bottom))
    img_crop.save('temp_files/System_temp.png')
    img = cv2.imread('temp_files/System_temp.png')
    text = pytesseract.image_to_string(img)
    return text


def get_item_name(screenshot_name):
    screenshot = Image.open(screenshot_name).convert('LA')
    img_crop = crop_image(screenshot, 1165, 250, 320, 793)
    img_crop.save('temp_files/Item_temp.png')
    img = cv2.imread('temp_files/Item_temp.png')
    text = pytesseract.image_to_string(img)
    return text


def get_item_price(screenshot_name):
    screenshot = Image.open(screenshot_name).convert('LA')
    width = screenshot.width
    height = screenshot.height
    left = 1750
    top = 250
    right = width - 0
    bottom = height - 780
    img_crop = screenshot.crop((left, top, right, bottom))
    img_crop.save('temp_files/Item_price_temp.png')
    img = cv2.imread('temp_files/Item_price_temp.png')
    text = pytesseract.image_to_string(img)
    return text


def crop_image(screenshot, left, top, right_offset, bottom_offset):
    width = screenshot.width
    height = screenshot.height
    right = width - right_offset
    bottom = height - bottom_offset
    img_crop = screenshot.crop((left, top, right, bottom))
    return img_crop


if __name__ == '__main__':
    main()
