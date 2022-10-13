import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = \
'C:/Program Files (x86)/Tesseract-OCR/tesseract'
image = cv2.imread('car.JPG')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny_edge = cv2.Canny(gray_image, 100, 200)
(contours, new) = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
    if len(approx) == 4:
        contour_with_license_plate = approx
        (x, y, w, h) = cv2.boundingRect(contour)
        license_plate = image[y:y + h, x:x + w]
        break
(thresh, license_plate) = cv2.threshold(license_plate, 127, 255,
        cv2.THRESH_BINARY)

text = pytesseract.image_to_string(license_plate)
plate = cv2.blur(license_plate, ksize=(40, 40))
image[y:y + h, x:x + w] = plate

print ('BLURRED License Plate:', text)
cv2.imshow('Original Plate', license_plate)
cv2.imshow('Blurred Plate', image)
cv2.waitKey(0)