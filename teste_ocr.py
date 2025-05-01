import time
import easyocr
import cv2 as cv

reader = easyocr.Reader(['pt', 'en'], gpu=True)  # this needs to run only once to load the model into memory
image = cv.imread('media/drivers/teste_rodrigo.jpg')
print(image.shape)
# cv.imshow("image", image)
# time.sleep(10)
result = reader.readtext(image, detail=0)

print(result)
