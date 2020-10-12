import cv2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dayzi\AppData\Local\Tesseract-OCR\tesseract.exe'
img = Image.open('Buying.png').convert('LA')
width = img.width
height = img.height
img = cv2.imread('Buying.png')
text = pytesseract.image_to_string(img)
print(text)
