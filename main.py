import concurrent.futures
import RPi.GPIO as GPIO
import pandas as pd
import requests
import serial
import shutil
import time
import os

IMAGE_PATH = '../pdh-project/media/Images'
BUTTON_PIN = 16
LED_PIN = 21

def export_info():
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(3)
    
    def copy_image(img:str):
        img = os.path.join(IMAGE_PATH, img.split('/')[-1])
        shutil.copy(src=img, dst=folder)
        return img
    
    try:
        print("Getting the server data from ofundus api")
        res = requests.get('http://0.0.0.0:8000/ofundus/')
    except Exception as e:
        print(e)
    else:
        print("Data received sucessfully")
        data = res.json()
        df = pd.DataFrame(data)
        images = df['image'].tolist()

        folder = 'output'
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        print(f"{folder} directory created")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                results = [executor.submit(copy_image, img) for img in images]
                for f in concurrent.futures.as_completed(results):
                    print(f.result())
            except Exception as e:
                print("Error while copying the file")
                print(e)
            else:
                print(f"Images were successfully exported")
        
        csv_path = os.path.join(folder, 'received.csv')
        df.to_csv(csv_path)
        print(f"CSV file exported")
    
    GPIO.output(LED_PIN, GPIO.HIGH)
    
def export_interrupt(channel):
    export_info()

def setup_serial(direction="/dev/ttyUSB0", baud_rate=9600, timeout=1.0):
    sdata = serial.Serial(direction, baud_rate, timeout=timeout)
    time.sleep(2)
    
    sdata.reset_input_buffer()
    print('Serial device connected')
    
    return sdata

def check_serial(sdata, sleep_time = 0.1, character = 'e'):
    if sdata.in_waiting > 0:
        cmd = sdta.readline().decode('utf-8').rstrip()
        
        if cmd == character:
            export_info()

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down= GPIO.PUD_UP)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
def setup_interrupt(pin: int, c):
    GPIO.add_event_detect(
        pin,
        GPIO.RISING,
        callback = c,
        bouncetime=1000)

def toggle_led(t: float):
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(t)
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(t)

if __name__ == '__main__':
    
    use_serial = False
    
    try:
        sdata = setup_serial()
    except Exception as e:
        print(e)
        print("Serial Interface won't be used")
    else:
        use_serial = True
        
        
    setup_pins()
    setup_interrupt(BUTTON_PIN, export_interrupt)
    
    
    try:
        print('Program has started')
        while True:
            toggle_led(0.5)
            if use_serial:
                check_serial(sdata)
    except KeyboardInterrupt:
        GPIO.cleanup()