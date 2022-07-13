# 1인 가구를 위한 비상 연락 호출 시스템


> **1인 가구의 안전을 위해 비상시에 연락을 호출할 수 있는 관리 할 수 있는 시스템**
> 
- 라즈베리파이4와 연결된 스위치와 온습도 센서에서 입력을 받으면 DB에 값이 저장됩니다.
- 저장된 값을 바탕으로 웹에서 DB 정보를 받아와 관리합니다.

## 🐻DB/라즈베리파이 코드/웹 개발(2022.04~2022.05)



> 21세기 이후, 독거노인 비율은 16%에서 19.5%까지 상승했습니다. 1인 가구의 비중 역시 5년간 27.2%에서 30.2%까지 상승했습니다. 하지만 한국은 빠른 경제발전으로 인해 경제 및 디지털 사각지대에 있는 독거노인 및 1인 가구의 사회보장제도가 아직 많이 부족합니다. 이에 따라, 응급상황 및 식료품 배달 혹은 상담이 필요한 경우를 위해 쉽고 간편하게 도움을 요청하고 담당자가 등록되어 있는 1인가구를 효율적으로 관리할 수 있는 시스템을 구현했습니다.
> 
> 
> 저는 DB 테이블을 설계하고 라즈베리파이에서 구동되는 코드를 작성 후, DB와 연결되어 있는 웹 코드를 작성했습니다. 
> 

> 🔗깃허브:  [https://github.com/Yudaeun/emergency_helper](https://github.com/Yudaeun/emergency_helper)
> 

 

## 🐻팀원



| 유다은 | 팀장, DB 구현, 웹개발 |
| --- | --- |
| 조현주 | 앱개발 |

## 개발환경



- Visual Studio Code
- RaspberryPi 4B
- Apache
- MySQL
- Android Studio

## 개발언어


- Python3
- PHP
- HTML
- CSS
- JavaScript
- JAVA

## 프로젝트 구조


<img width="940" alt="Untitled (3)" src="https://user-images.githubusercontent.com/54846663/178677310-5fa0ca56-0086-4672-a107-76065b18e624.png">



- 라즈베리파이에 DHT11(온습도 센서)와 Tact Switch 두 개를 연결해 온도 및 습도, 스위치 입력 값(리셋/호출)을 출력하고 DB 테이블에 행을 추가합니다.
- DB에서 받아온 값을 바탕으로 웹과 앱에서 각각 PHP와 JAVA를 이용해 정보를 나타내고 수정할 수 있습니다.

## DB

<img width="391" alt="Untitled (2)" src="https://user-images.githubusercontent.com/54846663/178677225-10b7939c-5bda-4559-afbf-37b23d5651cb.png">



- **manager:** 1인가구를 담당하는 요양보호사, 상담사 등의 담당자 정보를 저장하는 테이블
- **households:** 등록되어 있는 1인 가구의 정보를 저장하는 테이블
- **manager_house list**: 1인 가구와 담당자가 계약한 날을 저장하기 위한 테이블
- **call_time:** 라즈베리파이로부터 받아온 호출 정보를 저장하기 위한 테이블
- **temptbl:** 라즈베리파이로부터 받아온 온습도 정보를 저장하기 위한 테이블
- **delivery**: 라즈베리파이로부터 받아온 호출 정보 중에 배달 값을 저장하기 위한 테이블로, 트리거에 의해 배달 요청이 들어오면 자동으로 해당 값이 테이블에 추가된다.
    
    ```sql
    use FOBO;
    DROP TRIGGER IF EXISTS deli;
    DELIMITER $$
    	CREATE TRIGGER deli
    		AFTER INSERT 
    		ON FOBO.call_time 
            FOR EACH ROW
    	BEGIN
    		DECLARE statetemp VARCHAR(20);
            SET statetemp='waiting';
            IF new.definition='delivery' THEN BEGIN
    			INSERT INTO FOBO.delivery(house_num,state,time)
    				VALUES(new.house_num,statetemp,new.time);
    		END; END IF;
        END $$
    DELIMITER ;
    ```
    

## 라즈베리파이


```java
def button_callback(channel):
    global count
    global state
    count+=1
    # count 값에 따라 버튼 제어 가능하게 함
    print("Button pushed!",count)

    if count==1:
        print("emergency")
        state="emergency"

    elif count==2:
        ... 생략

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
```

- **button_callback():** 스위치 버튼1(호출 버튼)은 누르는 횟수에 따라 각각 다른 호출 정보를 저장합니다.
- **button_callback2():** 스위치 버튼2(리셋 버튼)는 스위치 버튼1(호출 버튼)을 통해 마지막으로 저장된 호출 정보(호출 시간, 호출값)를 DB로 쿼리에 담아 전송하고, 호출 정보를 리셋하는 역할을 합니다.
- 호출 버튼 1회 클릭 시: emergency 출력(응급 호출)
    
    호출 버튼 2회 클릭 시: delivery 출력(배달 요청)
    
    호출 버튼 3회 클릭 시: consulting 출력(상담 요청)
    

```java
while True:
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity))
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
```

- DHT11(온습도 센서)로부터 온도와 습도값을 3초마다 받아와 각각의 변수(temperature_c, humidity)에 저장하고 출력합니다.
- 저장한 온도와 습도를 현재 시각과 함께 DB로 쿼리를 보내주어 temptbl에 행을 추가합니다.
- 에러가 발생하면 에러 메시지를 출력합니다.

## WEB

<img width="508" alt="Untitled (1)" src="https://user-images.githubusercontent.com/54846663/178677065-5a17c913-22d7-4aab-9d62-57cb72b89221.png">


```php
...생략
$con = mysqli_connect("IP", "root", "1234", "FOBO");

	$sql = "SELECT * FROM call_time WHERE definition='emergency' and state='waiting'";
 
   $ret = mysqli_query($con, $sql);   
   echo "<thead><><th>일련번호</th><th>시간</th><th>1인가구번호</th></th><th>호출내용</th></th><th>상태</th><th>완료</th></tr></thead><tbody>";
 while($row = mysqli_fetch_array($ret)) {
  $jb_edit = '
  <form action="index_complete.php" method="POST">
    <input type="hidden" name="call_no" value="' . $row[ 'ct_num' ] . '">
    <input type="submit" value="Complete">
  </form>
';
	  echo "<tr><td>", $row['ct_num'], 
	  "</td><td>", $row['time'], 
	  "</td><td>", $row['house_num'],
      "</td><td>", $row['definition'],
	  "</td><td>", $row['state'],
    "</td><td>", $jb_edit,
... 생략
```

- DB에서 테이블 정보를 불러와 웹 브라우저 상에 나타냅니다.
- 위의 코드는 index.php 코드의 일부로, 웹사이트에 접속 시 가장 먼저 나타나는 페이지입니다. 해당 페이지에서 아직 처리되지 않은 응급호출 명단을 바로 확인할 수 있습니다.
- 행마다 나타나는 Complete버튼을 클릭하면, waiting(대기중)이었던 상태가 complete로 변경되어 해당 페이지에서 사라지게 됩니다.
- 배달 관리 페이지에서는 배달 요청이 들어온 목록에서 처리하고자 하는 건을 선택해 운송장 번호, 배달 물품 등의 정보를 수정할 수 있습니다.
- 온습도 관리 페이지에서는 현재 온도가 50도 이상인 가구의 정보만 나타냅니다. 집안 내부 온도에 이상이 생긴 경우만 빠르게 체크하기 위함입니다.

## 안드로이드



!<img width="726" alt="Untitled" src="https://user-images.githubusercontent.com/54846663/178676821-0afb03f0-39fe-4863-98c7-d99c24965baf.png">


- DB의 값을 가져와 응급 호출내역을 앱에서 보여줍니다.
- 비상연락망을 등록하고 확인할 수 있습니다.
- 현재 내 위치(GPS)를 바탕으로 가까운 병원과 약국의 위치를 확인할 수 있습니다.
