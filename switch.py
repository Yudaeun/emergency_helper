import RPi.GPIO as GPIO
import sys
import adafruit_dht
import pymysql
import mysql.connector;
from datetime import datetime
import time
import board
import threading

conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="FOBO");
cur = conn.cursor(prepared=True);

button_pin = 21
button_pin2=20
count=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# 시간 상한선을 3초로 두고 3초가 지나면 해당 count-state 값으로 고정 후 count 초기화

dhtDevice = adafruit_dht.DHT11(board.D4)

max_time_end = time.time() + 3
state='reset'
check=0

def button_callback(channel):

    global count
    global max_time_end
    global state
    max_time_end = time.time() + 3
    count+=1
    # count 값에 따라 버튼 제어 가능하게 함
    print("Button pushed!",count)

    if count==1:
        #print("Time: {:.4f}sec".format((time.time() - max_time_end)))
        print("emergency")
        state="emergency"

    elif count==2:
        #print("Time: {:.4f}sec".format((time.time() - max_time_end)))
        print("delivery")
        state="delivery"

    elif count==3:
        print("consulting")
        state="consulting"
        count=0
        #print("Time: {:.4f}sec".format((time.time() - max_time_end)))

def button_callback2(channel):

    global count
    count=0
    cur_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO call_time(time,house_num,definition,state) VALUES(%s,%s,%s,%s)"
    Values = [
        (cur_time, 1, state, 'waiting')
    ];
    cur.executemany(query, Values);
    conn.commit();
    print("reset and commit!")

GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback, bouncetime=300)
GPIO.add_event_detect(button_pin2, GPIO.RISING, callback=button_callback2, bouncetime=300)
# Event 방식으로 핀의 Rising 신호를 감지하면 button_callback 함수를 실행
# 300ms 바운스타임을 설정하여 잘못된 신호를 방지

while True:

    try:

        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

        sql="insert into temptbl(time,house_num,temp,humidity) values(%s,%s,%s,%s);"
        cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'1',temperature_c,humidity))
        conn.commit();
    except RuntimeError as error:

        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(3.0)

while 1:
    time.sleep(0.1)
