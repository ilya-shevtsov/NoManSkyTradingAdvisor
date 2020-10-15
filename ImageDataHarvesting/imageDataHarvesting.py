import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dayzi\AppData\Local\Tesseract-OCR\tesseract.exe'


def main():
    screenshot_name = "Buying.png"
    grayscale_screenshot = Image.open(screenshot_name).convert('LA')

    top_coordinates_item = [255, 365, 455, 555, 655]
    bottom_offset_coordinates_item = [790, 680, 570, 459, 350]

    top_coordinates_price = [250, 350, 485, 560, 680]
    bottom_offset_coordinates_price = [780, 675, 570, 460, 340]

    not_finished = True
    top_coordinates_check = [304, 414, 524, 634, 744, 0]
    bottom_offset_coordinates_check = [740, 635, 530, 425, 315, 0]

    item_index = 0
    while not_finished:
        is_an_item = check_is_item(
            grayscale_screenshot,
            top_coordinates_check[item_index],
            bottom_offset_coordinates_check[item_index],
            item_index
        )

        not_finished = is_an_item
        item_index += 1
    number_of_items = item_index - 1

    for a in range(number_of_items):
        system_name = get_system_name(grayscale_screenshot)
        item_name = get_item_name(grayscale_screenshot, top_coordinates_item[a], bottom_offset_coordinates_item[a])
        item_price = get_item_price(grayscale_screenshot, top_coordinates_price[a], bottom_offset_coordinates_price[a])
        print(item_name, system_name, item_price)


def check_is_item(screenshot, top, bottom_offset, item_index):
    img_crop = crop_image(screenshot, left=1180, top=top, right_offset=550, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'check_is_item' + str(item_index))
    text = text[:-3]
    return text == "Produced Locall"


def get_item_name(screenshot, top, bottom_offset):
    img_crop = crop_image(screenshot, left=1165, top=top, right_offset=320, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'item_name_temp')
    text = text[:-2]
    return text


def get_item_price(screenshot, top, bottom_offset):
    text = price_check(screenshot, 1620, top, bottom_offset)
    try:
        text = int(text)
    except ValueError:
        text = price_check(screenshot, 1600, top, bottom_offset)
        text = int(text)
    return text


def price_check(screenshot, left_coordinates, top, bottom_offset):
    img_crop = crop_image(screenshot, left=left_coordinates, top=top, right_offset=-20, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'price_temp')
    text = text[:-2]
    text = text.split()
    text = [x.replace(',', '') for x in text if x.replace(',', '').isnumeric()]
    ' '.join(text)
    text = f"{' '.join(text)}"
    return text


def get_system_name(screenshot):
    img_crop = crop_image(screenshot, left=150, top=930, right_offset=1100, bottom_offset=80)
    text = extract_text(img_crop, 'system_temp')
    text = text.split()
    text = [x for x in text if x not in ['-', 'System']]
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
