import RPi.GPIO as GPIO
import time

# GPIO 핀 번호를 BCM 모드로 설정
GPIO.setmode(GPIO.BCM)

# 버튼 핀 번호 설정
green_button = 5
red_button = 6
yellow_button = 26

# 버튼 핀을 입력으로 설정하고 내부 풀다운 저항 활성화
GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 버튼 눌림을 감지하는 콜백 함수 정의
def green_pressed(channel):
    print("초록")

def red_pressed(channel):
    print("빨간")

def yellow_pressed(channel):
    print("노란")

# 이벤트 감지 설정 (버튼이 눌렸을 때)
GPIO.add_event_detect(green_button, GPIO.RISING, callback=green_pressed, bouncetime=200)
GPIO.add_event_detect(red_button, GPIO.RISING, callback=red_pressed, bouncetime=200)
GPIO.add_event_detect(yellow_button, GPIO.RISING, callback=yellow_pressed, bouncetime=200)

def green_pressed(channel):
    print(f"Green (GPIO {channel})")

def red_pressed(channel):
    print(f"Red (GPIO {channel})")

def yellow_pressed(channel):
    print(f"Yellow (GPIO {channel})")


try:
    print("버튼을 눌러보세요. 종료하려면 Ctrl+C 누르세요.")
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n프로그램 종료")

finally:
    GPIO.cleanup()
