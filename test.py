import RPi.GPIO as GPIO
import sys
import adafruit_dht
import pymysql
import mysql.connector;
from datetime import datetime
import time
import board
import threading

conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="FOBO")
cur = conn.cursor(prepared=True)

button_pin = 21
count=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 시간 상한선을 3초로 두고 3초가 지나면 해당 count-state 값으로 고정 후 count 초기화

dhtDevice = adafruit_dht.DHT11(board.D4)

max_time_end=time.time()+3

def maxtime():
    global max_time_end
    max_time_end=time.time()+3

threading.Timer(3.0,maxtime).start()

global pressed_button_time
pressed_button_time=None
global count1_time
count1_time=None
global count2_time
count2_time=None

def button_released(channel): #스위치 뗄때마다 시각 저장
    global pressed_button_time
    pressed_button_time=datetime.now()

def button_callback(channel):

    global count
    global max_time_end
    global count1_time
    global count2_time
    count+=1
    pressed_button_time=datetime.now()
    # count 값에 따라 버튼 제어 가능하게 함

    print("Button pushed!",count)
    if count==1 and count1_time==None: #처음 눌렀을 때만 emergency 나오도록 하기
        print("emergency")
        state="emergency"
        count1_time=datetime.now() #처음 눌렀을 때 시각 저장

        if time.time()>max_time_end:

            count=0

    #count가 2이거나 첫번째 눌렀을 때(정확하게는 첫번째 스위치 뗀 시각)와 두번째 눌렀을 때 시각 비교하여 count2_time이 None일때만 실행
    elif (count==2 or pressed_button_time>count1_time) and count2_time==None:
        print("delivery")
        state="delivery"
        count2_time=datetime.now()
        if time.time()>max_time_end:

            count=0

    elif count==3 or pressed_button_time>count2_time:#두번째 눌렀을 때와 세번째 눌렀을 때 시각 비교
        print("consulting")
        state="consulting"
        count=0

    if count==0 or (datetime.now()-count1_time).seconds>=3: #처음 눌렀을 때부터 3초 지났을 경우
        count=0
        count1_time=None #초기화
        count2_time=None
        cur_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO call_time(time,house_num,definition,state) VALUES(%s,%s,%s,%s)"
        Values = [
            (cur_time, 1, state, 'waiting')
        ]
        cur.executemany(query, Values)
        conn.commit()
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)


while 1:
    time.sleep(0.1)