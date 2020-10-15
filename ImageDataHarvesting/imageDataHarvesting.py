import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dayzi\AppData\Local\Tesseract-OCR\tesseract.exe'


def main():
    screenshot_name = "Buying.png"
    grayscale_screenshot = Image.open(screenshot_name).convert('LA')
    # system_name = get_system_name(grayscale_screenshot)
    # item_name = get_item_name(grayscale_screenshot)
    # item_price = get_item_price(grayscale_screenshot)
    # print(item_name, system_name, item_price)

    top_coordinates_item = [255, 365, 455, 555, 655]
    bottom_offset_coordinates_item = [791, 681, 571, 459, 349]

    top_coordinates_price = [250, 350, 485, 560, 660]
    bottom_offset_coordinates_price = [780, 680, 570, 455, 350]

    not_finished = True
    top_coordinates_check = [289, 388, 505, 616, 725, 0]
    bottom_offset_coordinates_check = [770, 660, 550, 440, 330, 0]

    i = 0
    while not_finished:
        is_an_item = check_is_item(grayscale_screenshot, top_coordinates_check[i], bottom_offset_coordinates_check[i])
        not_finished = is_an_item
        i += 1
    number_of_items = i - 1

    a = 0
    while a < number_of_items:
        item_name = get_item_name(grayscale_screenshot, top_coordinates_item[a], bottom_offset_coordinates_item[a])
        system_name = get_system_name(grayscale_screenshot)
        item_price = get_item_price(grayscale_screenshot, top_coordinates_price[a], bottom_offset_coordinates_price[a])
        a += 1
        print(item_name, system_name, item_price)


def check_is_item(screenshot, top, bottom_offset):
    img_crop = crop_image(screenshot, left=1180, top=top, right_offset=670, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'check_is_item')
    text = text[:-3]
    return text == "Price"


def get_item_name(screenshot, top, bottom_offset):
    img_crop = crop_image(screenshot, left=1165, top=top, right_offset=320, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'item_name_temp')
    text = text[:-2]
    return text


def get_item_price(screenshot, top, bottom_offset):
    # bottom in item 4 = 460 or 455 need a check
    img_crop = crop_image(screenshot, left=1741, top=top, right_offset=-20, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'price_temp')
    text = text[:-2]
    try:
        text = int(text.replace(',', ''))
    except ValueError:
        img_crop = crop_image(screenshot, left=1750, top=250, right_offset=-20, bottom_offset=780)
        text = extract_text(img_crop, 'price_temp')
        text = int(text.replace(',', ''))
    return text


def get_system_name(screenshot):
    img_crop = crop_image(screenshot, left=150, top=930, right_offset=1100, bottom_offset=80)
    text = extract_text(img_crop, 'system_temp')
    text = text.split()
    text.remove('-')
    text.remove('System')
    ' '.join(text)
    text = f"{' '.join(text)}"
    return text


def crop_image(screenshot, left, top, right_offset, bottom_offset):
    width = screenshot.width
    height = screenshot.height
    right = width - right_offset
    bottom = height - bottom_offset
    img_crop = screenshot.crop((left, top, right, bottom))
    return img_crop


def extract_text(img_crop, file_name):
    img_crop.save('temp_files/' + file_name + '.png')
    img = cv2.imread('temp_files/' + file_name + '.png')
    text = pytesseract.image_to_string(img)
    return text


if __name__ == '__main__':
    main()
