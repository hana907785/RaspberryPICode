import RPi.GPIO as GPIO
import time

# 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 시퀀스
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

steps_per_rotation = 4076
step_sleep_fast = 0.001  # 빠르게 갈 때 속도

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

try:
    duration_minutes = float(input("⏱ 몇 분 설정할까요? (예: 15): "))
    degrees_to_move = duration_minutes * 6
    steps_to_move = int((degrees_to_move / 360) * steps_per_rotation)

    print(f"➡ 빠르게 정방향 {degrees_to_move:.1f}도 이동 중... ({steps_to_move} 스텝)")
    motor_step_counter = 0

    # 빠르게 정방향
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep_fast)

    print("⏳ 타이머 시작! 천천히 복귀 중...")
    total_seconds = duration_minutes * 60
    delay_per_step = total_seconds / steps_to_move

    # ❗ 역방향 회전을 위해 counter 초기화
    # 역방향 순서로 동작시킬 때는 시퀀스 순서를 뒤집고 방향만 바꾸는 게 가장 직관적임
    # 또는, 인덱스를 새로 설정해도 됨
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8  # 역방향
        time.sleep(delay_per_step)

    print("✅ 복귀 완료!")

except KeyboardInterrupt:
    print("\n[사용자 종료]")
finally:
    cleanup()
