import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 시퀀스 (정방향 기준)
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

steps_per_rotation = 4076         # 360도 기준
step_sleep_fast = 0.001           # 빠른 회전 (정방향)
step_sleep_slow = None            # 나중에 계산됨

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def move_motor(steps, direction=1, delay=0.001):
    motor_step_counter = 0
    for _ in range(steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + direction) % 8
        time.sleep(delay)

try:
    duration_minutes = float(input("⏱ 몇 분 설정할까요? (예: 10): "))
    degrees_to_move = duration_minutes * 6
    steps_to_move = int((degrees_to_move / 360) * steps_per_rotation)

    print(f"➡ 정방향 {degrees_to_move:.1f}도 회전 중 ({steps_to_move} 스텝)")
    move_motor(steps_to_move, direction=-1, delay=step_sleep_fast)  # 정방향

    # 복귀: 천천히 역방향으로 1분에 6도씩
    steps_per_6_degrees = int((6 / 360) * steps_per_rotation)
    delay_per_step = 60 / steps_per_6_degrees  # 1분(60초) 동안 6도 복귀

    print(f"⬅ {duration_minutes:.0f}분에 걸쳐 천천히 복귀 중...")
    for _ in range(steps_to_move):
        seq = step_sequence[0]  # 초기화 필요
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        move_motor(1, direction=1, delay=delay_per_step)  # 역방향 (slow)

    print("✅ 복귀 완료!")

except KeyboardInterrupt:
    print("\n[사용자 종료]")
finally:
    cleanup()
