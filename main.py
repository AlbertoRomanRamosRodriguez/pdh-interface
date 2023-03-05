import RPi.GPIO as GPIO
import pandas as pd
import requests
import shutil
import time
import os

IMAGE_PATH = '../pdh-project/media/Images'
BUTTON_PIN = 16

def check_int(channel):
    print('interrupt')

def export_info(channel):
    try:
        print("Getting the server data from ofundus api")
        res = requests.get('http://0.0.0.0:8000/ofundus/')
    except Exception as e:
        print(e)
    else:
        print("Data received sucessfully")
        print("Parsing JSON")
        data = res.json()
        print("Data parsed sucessfully")
        df = pd.DataFrame(data)
        print("Getting image path list ")
        images = df['image'].tolist()
        print("Image path list obtained sucessfully")

        folder = 'output'
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        print(f"{folder} directory created sucessfully")

        for img in images:
            img = os.path.join(IMAGE_PATH, img.split('/')[-1])
            shutil.copy(src=img, dst=folder)
        print(f"Images exported sucessfully")
        
        csv_path = os.path.join(folder, 'received.csv')
        df.to_csv(csv_path)
        print(f"CSV file exported sucessfully")
        
def setup_interrupt(pin: int, c):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)
    GPIO.add_event_detect(
        pin,
        GPIO.RISING,
        callback = c,
        bouncetime=50)

if __name__ == '__main__':
    setup_interrupt(BUTTON_PIN, export_info)
    
    try:
        print('hello world')
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()