import RPi.GPIO as GPIO
from time import sleep

servoPin = 18  # BCM GPIO 18번
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 50)  # 50Hz
servo.start(0)

SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

def setServoPos(degree):
    degree = max(0, min(180, degree))
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    print(f"서보 이동: {degree}도 (Duty: {duty:.2f})")
    servo.ChangeDutyCycle(duty)
    sleep(0.3)
    servo.ChangeDutyCycle(0)

def rotate_forward(from_angle, to_angle):
    """서보를 주어진 각도만큼 한 방향으로 회전"""
    setServoPos(0)       # 서보 시작 위치 초기화
    sleep(0.5)
    setServoPos(180)     # 1단계 회전
    sleep(1)
    setServoPos(0)       # 되감기
    sleep(0.5)
    setServoPos(to_angle)  # 나머지 회전
    sleep(1)

try:
    user_minutes = int(input("타이머 시간 (분): "))  # 예: 40
    total_logical_angle = user_minutes * 6  # 1분 = 6도

    print(f"총 논리 각도: {total_logical_angle}도")

    # 한 방향 회전처럼 보이게 제어
    if total_logical_angle <= 180:
        setServoPos(total_logical_angle)
    else:
        # 분할 회전
        rotate_forward(0, total_logical_angle - 180)

    # 감소 루프
    current_angle = total_logical_angle
    for minute in range(user_minutes):
        sleep(60)  # 실제는 60초
        current_angle -= 6
        print(f"{minute+1}분 경과 → 논리 각도: {current_angle}도")

        if current_angle <= 180:
            setServoPos(current_angle)
        else:
            rotate_forward(0, current_angle - 180)

    print("✅ 타이머 종료!")

except KeyboardInterrupt:
    print("중단됨")

finally:
    servo.stop()
    GPIO.cleanup()
