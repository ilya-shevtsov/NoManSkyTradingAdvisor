import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dayzi\AppData\Local\Tesseract-OCR\tesseract.exe'


def main():
    screenshot_name = "Buying.png"
    grayscale_screenshot = Image.open(screenshot_name).convert('LA')
    system_name = get_system_name(grayscale_screenshot)
    item_name = get_item_name(grayscale_screenshot)
    item_price = get_item_price(grayscale_screenshot)
    is_an_item = check_is_item(grayscale_screenshot)
    print(item_name, system_name, item_price)


# def count_items(screenshot):
#     number_of_items = 0
#     while check_is_item(screenshot):
#         number_of_items = +1
#     return number_of_items


def check_is_item(screenshot):
    # top in item 4 = 615 or 616 need a check
    # img_crop = crop_image(screenshot, left=1180, top=289, right_offset=670, bottom_offset=770)
    # img_crop = crop_image(screenshot, left=1180, top=388, right_offset=670, bottom_offset=660)
    # img_crop = crop_image(screenshot, left=1180, top=505, right_offset=670, bottom_offset=550)
    # img_crop = crop_image(screenshot, left=1180, top=616, right_offset=670, bottom_offset=440)
    img_crop = crop_image(screenshot, left=1180, top=725, right_offset=670, bottom_offset=330)
    img_crop.save('temp_files/check_is_item_temp.png')
    img = cv2.imread('temp_files/check_is_item_temp.png')
    text = pytesseract.image_to_string(img)
    text = text[:-3]
    return text == "Price"


def get_system_name(screenshot):
    if check_is_item(screenshot):
        img_crop = crop_image(screenshot, left=310, top=940, right_offset=1100, bottom_offset=81)
        img_crop.save('temp_files/System_temp.png')
        img = cv2.imread('temp_files/System_temp.png')
        text = pytesseract.image_to_string(img)
        text = text.lstrip("-")
        text = text.lstrip()
        text = text[:-2]
        return text


def get_item_name(screenshot):
    if check_is_item(screenshot):
        # img_crop = crop_image(screenshot, left=1165, top=255, right_offset=320, bottom_offset=791)
        # img_crop = crop_image(screenshot, left=1165, top=365, right_offset=320, bottom_offset=681)
        # img_crop = crop_image(screenshot, left=1165, top=455, right_offset=320, bottom_offset=571)
        # img_crop = crop_image(screenshot, left=1165, top=555, right_offset=320, bottom_offset=459)
        img_crop = crop_image(screenshot, left=1165, top=655, right_offset=320, bottom_offset=349)
        img_crop.save('temp_files/Item_temp.png')
        img = cv2.imread('temp_files/Item_temp.png')
        text = pytesseract.image_to_string(img)
        text = text[:-2]
        return text


def get_item_price(screenshot):
    if check_is_item(screenshot):
        # bottom in item 4 = 460 or 455 need a check
        # img_crop = crop_image(screenshot, left=1740, top=250, right_offset=-20, bottom_offset=780)
        # img_crop = crop_image(screenshot, left=1741, top=350, right_offset=-20, bottom_offset=680)
        # img_crop = crop_image(screenshot, left=1741, top=485, right_offset=-20, bottom_offset=570)
        # img_crop = crop_image(screenshot, left=1741, top=560, right_offset=-20, bottom_offset=455)
        img_crop = crop_image(screenshot, left=1741, top=660, right_offset=-20, bottom_offset=350)
        img_crop.save('temp_files/Item_price_temp.png')
        img = cv2.imread('temp_files/Item_price_temp.png')
        text = pytesseract.image_to_string(img)
        text = text[:-2]
        try:
            text = int(text.replace(',', ''))
            text = int(text)
        except ValueError:
            img_crop = crop_image(screenshot, left=1750, top=250, right_offset=-20, bottom_offset=780)
            img_crop.save('temp_files/Item_price_temp.png')
            img = cv2.imread('temp_files/Item_price_temp.png')
            text = pytesseract.image_to_string(img)
            text = int(text.replace(',', ''))
            text = int(text)
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
