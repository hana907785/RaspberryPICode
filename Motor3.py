import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 8스텝 시퀀스
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

steps_per_rotation = 4076  # 360도 기준
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def move_motor(steps, direction=1, delay=0.001):
    counter = 0
    for _ in range(steps):
        seq = step_sequence[counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        counter = (counter + direction) % 8
        time.sleep(delay)

try:
    # 입력: 몇 분 설정?
    duration_minutes = float(input("⏱ 몇 분 설정할까요? (예: 10): "))
    degrees = duration_minutes * 6
    total_steps = int((degrees / 360) * steps_per_rotation)
    steps_per_minute = int((6 / 360) * steps_per_rotation)  # 1분 = 6도 = 약 67스텝

    print(f"➡ 즉시 정방향 {degrees:.1f}도 ({total_steps}스텝) 회전")
    move_motor(total_steps, direction=-1, delay=0.001)

    print(f"⬅ 천천히 역방향 복귀 시작 (1분마다 {steps_per_minute}스텝, 총 {int(duration_minutes)}회)")
    for i in range(int(duration_minutes)):
        move_motor(steps_per_minute, direction=1, delay=0.005)
        print(f"⏪ {i+1}분 경과: {((i+1)*6)}도 복귀됨")
        time.sleep(60)

    print("✅ 복귀 완료!")

except KeyboardInterrupt:
    print("\n[사용자 중단]")
finally:
    cleanup()
