import os
import re
import easyocr
import cv2 as cv
from django.conf import settings


class DocumentOCR:

    def __init__(self) -> None:
        filename = cv.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_classifier = cv.CascadeClassifier(filename)
        self.reader = easyocr.Reader(lang_list=['pt', 'en'])
        self.destination_image_path = os.path.join(settings.MEDIA_ROOT, "drivers/validate/drivers/")

    def extract_data_document(self, document_path: str):
        image = cv.imread(document_path)
        text = " ".join(self.reader.readtext(image, detail=0))
        cpf_match = re.search(r'\b(\d{3}\.?\d{3}\.?\d{3}-?\d{2})\b', text)
        phone_match = re.search(r'\b(\(?\d{2}\)?\s*\d{4,5}-?\d{4})\b', text)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        name = lines[0] if lines else ''
        result = {
            'name': name,
            'cpf': cpf_match.group(1).replace('.', '').replace('-', '') if cpf_match else '',
            'phone': phone_match.group(1) if phone_match else '',
        }
        return result

    def extract_image(self, document_path: str):
        os.makedirs(os.path.dirname(self.destination_image_path), exist_ok=True)

        image = cv.imread(document_path)
        image_name = document_path.split("/")[-1]
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(
            gray_image,
            1.1,
            5,
            minSize=(40, 40),
        )

        image_to_validate = os.path.join(self.destination_image_path, image_name)

        for x, y, w, h in faces:
            image = image[y : y + h, x : x + w]
            cv.imwrite(image_to_validate, image)

        return image_to_validate
