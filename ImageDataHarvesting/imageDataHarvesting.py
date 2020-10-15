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
    print(item_name,system_name,item_price)

    not_finished = True
    top_coordinates = [289, 388, 505, 616, 725, 0]
    bottom_offset_coordinates = [770, 660, 550, 440, 330, 0]
    i = 0
    while not_finished:
        is_an_item = check_is_item(grayscale_screenshot, top_coordinates[i], bottom_offset_coordinates[i])
        not_finished = is_an_item
        i += 1
    number_of_items = i - 1


def check_is_item(screenshot, top, bottom_offset):
    # top in item 4 = 615 or 616 need a check
    img_crop = crop_image(screenshot, left=1180, top=top, right_offset=670, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'check_is_item')
    text = text[:-3]
    return text == "Price"


def get_item_name(screenshot):
    img_crop = crop_image(screenshot, left=1170, top=250, right_offset=320, bottom_offset=790)
    # img_crop = crop_image(screenshot, left=1170, top=350, right_offset=320, bottom_offset=690)
    # img_crop = crop_image(screenshot, left=1165, top=255, right_offset=320, bottom_offset=791)
    # img_crop = crop_image(screenshot, left=1165, top=365, right_offset=320, bottom_offset=681)
    # img_crop = crop_image(screenshot, left=1165, top=455, right_offset=320, bottom_offset=571)
    # img_crop = crop_image(screenshot, left=1165, top=555, right_offset=320, bottom_offset=459)
    # img_crop = crop_image(screenshot, left=1165, top=655, right_offset=320, bottom_offset=349)
    text = extract_text(img_crop, 'item_name_temp')
    text = text[:-2]
    return text


def get_item_price(screenshot):
    # bottom in item 4 = 460 or 455 need a check
    img_crop = crop_image(screenshot, left=1741, top=250, right_offset=-20, bottom_offset=780)
    # img_crop = crop_image(screenshot, left=1741, top=350, right_offset=-20, bottom_offset=680)
    # img_crop = crop_image(screenshot, left=1741, top=485, right_offset=-20, bottom_offset=570)
    # img_crop = crop_image(screenshot, left=1741, top=560, right_offset=-20, bottom_offset=455)
    # img_crop = crop_image(screenshot, left=1741, top=660, right_offset=-20, bottom_offset=350)
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
