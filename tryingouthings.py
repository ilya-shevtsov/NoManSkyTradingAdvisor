import cv2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dayzi\AppData\Local\Tesseract-OCR\tesseract.exe'


img = cv2.imread('price_temp4.png',cv2.IMREAD_GRAYSCALE)
img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imwrite('processed.png',img)
