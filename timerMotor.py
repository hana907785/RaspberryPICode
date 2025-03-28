import RPi.GPIO as GPIO
from time import sleep

servoPin = 12 #임시 핀번호
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 50)
servo.start(0)

SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

def setServoPos(degree):
    if degree > 180: degree = 180
    if degree < 0: degree = 0
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    print(f"→ 각도: {degree}도 (Duty: {duty:.2f})")
    servo.ChangeDutyCycle(duty)
    sleep(0.3)
    servo.ChangeDutyCycle(0)

try:
    user_minutes = int(input("Time: "))  # 예: 40
    total_angle = user_minutes * 6

    # 현재 위치 초기화
    current_angle = 0

    # 초기 설정: 지정 각도까지 이동
    if total_angle <= 180:
        setServoPos(total_angle)
        current_angle = total_angle
    else:
        # 1단계: 180도까지 회전
        setServoPos(180)
        sleep(1)

        # 2단계: 0도로 복귀
        setServoPos(0)
        sleep(1)

        # 3단계: 나머지 각도 회전
        remaining_angle = total_angle - 180
        setServoPos(remaining_angle)
        current_angle = 180 + remaining_angle  # 논리적 위치

    print("Timer Start")

    # 1분마다 6도씩 감소
    for minute in range(user_minutes):
        sleep(60)  # 실제 사용 시 60초 (테스트 땐 sleep(2) 등으로 바꿔도 됨)
        current_angle -= 6

        if current_angle >= 180:
            # 한 바퀴 이상일 경우 (나머지 각도만 계산해서 표현)
            setServoPos(180)
            sleep(1)
            setServoPos(0)
            sleep(1)
            setServoPos(current_angle - 180)
        else:
            setServoPos(current_angle)

    print("Finish!")

except KeyboardInterrupt:
    print("Stop")

finally:
    servo.stop()
    GPIO.cleanup()
