import RPi.GPIO as GPIO
import time

# 피에조 부저 핀
BUZZER_PIN = 13

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    while True:
        user_input = input("input: ").strip().lower()
        if user_input == 'r':
            print("Reset 감지됨: 부저 울림")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)  # 100ms 삑!
            GPIO.output(BUZZER_PIN, GPIO.LOW)

except KeyboardInterrupt:
    print("\n종료됨. GPIO 정리 중...")
finally:
    GPIO.cleanup()
