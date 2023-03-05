from PIL import Image

import pandas as pd
import requests
import shutil
import os

IMAGE_PATH = '../pdh/media/Images/'

def export_info():
    res = requests.get('http://0.0.0.0:8000/ofundus/')
    data = res.json()
    df = pd.DataFrame(data)
    images = df['image'].tolist()

    folder = 'output'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    for img in images:
        img = os.path.join(IMAGE_PATH, img.split('/')[-1])
        shutil.copy(src=img, dst=folder)

    csv_path = os.path.join(folder, 'received.csv')
    df.to_csv(csv_path)
