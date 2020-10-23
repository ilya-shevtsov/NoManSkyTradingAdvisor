import csv
import pandas as pd
import cv2
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def main():
    image_data_harvesting()


def image_data_harvesting():
    top_coordinates_item = [255, 355, 465, 575, 685, 795]
    bottom_offset_coordinates_item = [795, 685, 575, 465, 355, 245]
    top_coordinates_price = [250, 360, 470, 580, 690, 800]
    bottom_offset_coordinates_price = [780, 670, 560, 450, 340, 230]
    top_coordinates_check = [305, 415, 525, 635, 745, 855]
    bottom_offset_coordinates_check = [740, 630, 520, 410, 300, 190]
    for filename in os.listdir('un_converted_images'):
        if filename.endswith('jpg'):
            img = Image.open(os.path.join('un_converted_images', filename))
            new_img = img.convert('RGB')
            new_img.save(os.path.join('converted_images', filename.replace('jpg', 'png')))
            os.remove(os.path.join('un_converted_images', filename))
    for filename in os.listdir('converted_images'):
        screenshot_name = filename
        screenshot = Image.open(os.path.join('converted_images', screenshot_name))
        grayscale_screenshot = screenshot.convert('LA')
        screenshot_type = get_screenshot_type(grayscale_screenshot)
        if screenshot_type:
            item_check_list = checking_counting_item_selling(
                bottom_offset_coordinates_check,
                grayscale_screenshot, top_coordinates_check,
                screenshot_type
            )
        else:
            item_check_list = checking_counting_item_buying(
                bottom_offset_coordinates_check,
                grayscale_screenshot,
                top_coordinates_check,
                screenshot_type
            )

        for index, is_item in enumerate(item_check_list):
            if is_item:
                system_name = get_system_name(grayscale_screenshot, screenshot_type)
                item_name = get_item_name(
                    grayscale_screenshot,
                    top_coordinates_item[index],
                    bottom_offset_coordinates_item[index],
                    index,
                    screenshot_type
                )
                item_price = get_item_price(
                    grayscale_screenshot,
                    top_coordinates_price[index],
                    bottom_offset_coordinates_price[index],
                    index,
                    screenshot_type
                )
                if screenshot_type:
                    end_result = [item_name, system_name, 0, str(item_price)]
                else:
                    end_result = [item_name, system_name, str(item_price), 0]
                with open('harvested_data.csv', 'a') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(end_result)
    data = pd.read_csv('harvested_data.csv', encoding='cp1252')
    data.dropna(how='all')
    data.drop_duplicates(inplace=True)
    data.to_csv('harvested_data.csv', index=False)


def get_screenshot_type(screenshot):
    img_crop = screenshot.crop((1300, 190, screenshot.width - 320, screenshot.height - 850))
    img_crop.save('temp_files/screenshot_type.png')
    img = cv2.imread('temp_files/screenshot_type.png')
    text = pytesseract.image_to_string(img)
    text = text[:-3]
    return 'Sellable Item' in text


def checking_counting_item_buying(bottom_offset_coordinates_check, grayscale_screenshot, top_coordinates_check, screenshot_type):
    not_finished = True
    item_check_list = []
    item_index = 0
    while not_finished:
        checking_if_item = check_is_item(
            grayscale_screenshot,
            top_coordinates_check[item_index],
            bottom_offset_coordinates_check[item_index],
            item_index,
            screenshot_type
        )
        item_index += 1
        item_check_list.append(checking_if_item)
        if not checking_if_item:
            not_finished = False
    return item_check_list


def checking_counting_item_selling(bottom_offset_coordinates_check, grayscale_screenshot, top_coordinates_check, screenshot_type):
    item_check_list = []
    item_index = 0
    while item_index < 6:
        checking_if_item = check_is_item(
            grayscale_screenshot,
            top_coordinates_check[item_index],
            bottom_offset_coordinates_check[item_index],
            item_index,
            screenshot_type
        )
        item_index += 1
        item_check_list.append(checking_if_item)
    return item_check_list


def check_is_item(screenshot, top, bottom_offset, item_index, screenshot_type):
    img_crop = crop_image('check_is_item' + str(item_index), screenshot, left=1180, top=top, right_offset=550, bottom_offset=bottom_offset)
    if screenshot_type:
        text = extract_text_checking_item(img_crop, 'check_is_item' + str(item_index), screenshot_type)
    else:
        text = extract_text(img_crop, 'check_is_item' + str(item_index), screenshot_type)
    text = text[:-3]
    if screenshot_type:
        return 'Economy' in text
    else:
        return text == 'Produced Locall' in text


def get_item_name(screenshot, top, bottom_offset, item_index, screenshot_type):
    img_crop = crop_image('item_name_temp' + str(item_index), screenshot, left=1165, top=top, right_offset=340, bottom_offset=bottom_offset)
    text = extract_text(img_crop, 'item_name_temp' + str(item_index), screenshot_type)
    text = text[:-2]
    return text


def get_item_price(screenshot, top, bottom_offset, item_index, screenshot_type):
    left_coordinates = [1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660]
    item_price = 0
    for coordinate in left_coordinates:
        try:
            text = read_price(
                screenshot,
                left_coordinate=coordinate,
                top=top,
                bottom_offset=bottom_offset,
                item_index=item_index,
                screenshot_type=screenshot_type
            )
            item_price = int(text)
        except ValueError:
            continue
        break
    return item_price


def read_price(screenshot, left_coordinate, top, bottom_offset, item_index, screenshot_type):
    img_crop = crop_image('price_temp' + str(item_index), screenshot, left=left_coordinate, top=top, right_offset=0, bottom_offset=bottom_offset)
    if screenshot_type:
        text = extract_text_selling(img_crop, 'price_temp' + str(item_index), screenshot_type)
    else:
        text = extract_text(img_crop, 'price_temp' + str(item_index), screenshot_type)
    text = text[:-2]
    text = text.split()
    text = [x.replace(',', '') for x in text if x.replace(',', '').isnumeric()]
    ' '.join(text)
    text = f"{' '.join(text)}"
    return text


def get_system_name(screenshot, screenshot_type):
    img_crop = crop_image('system_temp', screenshot, left=150, top=930, right_offset=1100, bottom_offset=80)
    text = extract_text_system_name(img_crop, 'system_temp', screenshot_type)
    text = text.split()
    text = [x for x in text if x not in ['-', 'System']]
    ' '.join(text)
    text = f"{' '.join(text)}"
    return text


def crop_image(file_name, screenshot, left, top, right_offset, bottom_offset):
    width = screenshot.width
    height = screenshot.height
    right = width - right_offset
    bottom = height - bottom_offset
    img_crop = screenshot.crop((left, top, right, bottom))
    img_crop.save('temp_files/' + file_name + '.png')
    return img_crop


def extract_text_selling(img_crop, file_name, screenshot_type):
    img = cv2.imread('temp_files/' + file_name + '.png')
    img = cv2.threshold(img, 45, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite('temp_files/' + file_name + '.png', img)
    text = pytesseract.image_to_string(img)
    return text


def extract_text_system_name(img_crop, file_name, screenshot_type):
    img = cv2.imread('temp_files/' + file_name + '.png')
    img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite('temp_files/' + file_name + '.png', img)
    text = pytesseract.image_to_string(img)
    return text


def extract_text_checking_item(img_crop, file_name, screenshot_type):
    img = cv2.imread('temp_files/' + file_name + '.png')
    img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite('temp_files/' + file_name + '.png', img)
    text = pytesseract.image_to_string(img)
    return text


def extract_text(img_crop, file_name, screenshot_type):
    img = cv2.imread('temp_files/' + file_name + '.png')
    text = pytesseract.image_to_string(img)
    return text


if __name__ == '__main__':
    main()
