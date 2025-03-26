import RPi.GPIO as GPIO
import time

# 버튼 핀 정의
RED_BUTTON = 5
YELLOW_BUTTON = 6
BLUE_BUTTON = 26

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_BUTTON, GPIO.IN)
GPIO.setup(YELLOW_BUTTON, GPIO.IN)
GPIO.setup(BLUE_BUTTON, GPIO.IN)

print("버튼 입력 대기 중... (Ctrl+C로 종료)")

try:
    while True:
        if GPIO.input(RED_BUTTON) == GPIO.HIGH:
            print("Red Button Pressed")
            while GPIO.input(RED_BUTTON) == GPIO.HIGH:
                time.sleep(0.01)  # 버튼에서 손 뗄 때까지 대기

        if GPIO.input(YELLOW_BUTTON) == GPIO.HIGH:
            print("Yellow Button Pressed")
            while GPIO.input(YELLOW_BUTTON) == GPIO.HIGH:
                time.sleep(0.01)

        if GPIO.input(BLUE_BUTTON) == GPIO.HIGH:
            print("Blue Button Pressed")
            while GPIO.input(BLUE_BUTTON) == GPIO.HIGH:
                time.sleep(0.01)

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n종료됨. GPIO 정리 중...")
finally:
    GPIO.cleanup()
