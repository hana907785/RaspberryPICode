import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1, in2, in3, in4 = 12, 16, 20, 21
motor_pins = [in1, in2, in3, in4]

# 스텝 시퀀스
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

steps_per_rotation = 4076  # 360도
step_sleep = 0.001         # 빠른 회전 속도

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def rotate(steps, direction=1, delay=step_sleep):
    """ 모터를 주어진 스텝만큼 회전 (direction: 1=정방향, -1=역방향) """
    index = 0
    for _ in range(steps):
        seq = step_sequence[index]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        index = (index + direction) % 8
        time.sleep(delay)

try:
    duration_minutes = float(input("⏱ 몇 분 설정할까요? (예: 10): "))
    degrees = duration_minutes * 6
    steps_to_move = int((degrees / 360) * steps_per_rotation)

    print(f"➡ 정방향 {degrees:.1f}도 회전 중... ({steps_to_move} 스텝)")
    rotate(steps_to_move, direction=1)

    print("⏳ 실시간 복귀 중...")
    total_seconds = int(duration_minutes * 60)
    steps_remaining = steps_to_move
    current_step_index = 0

    for _ in range(total_seconds):
        steps_this_second = steps_to_move / total_seconds
        steps_this_second = int(round(steps_this_second))

        for _ in range(steps_this_second):
            seq = step_sequence[current_step_index]
            for pin, val in zip(motor_pins, seq):
                GPIO.output(pin, val)
            current_step_index = (current_step_index - 1) % 8  # 역방향
            time.sleep(0.01)  # 부드럽게

        time.sleep(1 - 0.01 * steps_this_second)  # 나머지 시간 대기

    print("✅ 복귀 완료!")

except KeyboardInterrupt:
    print("\n[사용자 종료]")

finally:
    cleanup()
