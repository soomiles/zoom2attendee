import cv2
import pytesseract
from pathlib import Path
import datetime
import pandas as pd
from skimage.filters import threshold_otsu
from skimage.util import invert

import matplotlib.pyplot as plt

def main():
    dateTimeObj = datetime.datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d")
    
    pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'
    image_dir = Path('./images')
    image_paths = [path for path in image_dir.glob('*.png')]
    
    texts = ''
    for path in image_paths:
        image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        thresholded = (image > threshold_otsu(image)).astype('uint8') * 255
        texts += pytesseract.image_to_string(thresholded)
        texts += '\n'
    subtexts = texts.split('\n')
    
    ids = []
    for sub in subtexts:
        if (sub[:2] == '20' and len(sub) > 7):
            ids.append(sub[:8])
    ids = sorted(list(set(ids)))
    
    df = pd.DataFrame({'Attendee': ids})
    df.to_csv(f'./attendees/{timestampStr}.csv', index=False)

if __name__ == "__main__":
    main()