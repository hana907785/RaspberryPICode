#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 정방향 시퀀스 (필요 시 반대로 정의 가능)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

steps_per_rotation = 4096  # 360도 회전 기준
step_sleep = 0.005         # 속도 조절

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
    # 사용자 입력 받기
    duration_minutes = float(input("Enter duration in minutes (1 min = 6 degrees): "))
    direction = input("Enter direction (f = forward, r = reverse): ").strip().lower()

    # 회전 각도 및 필요한 스텝 수 계산
    rotation_degrees = duration_minutes * 6
    total_steps = int((rotation_degrees / 360) * steps_per_rotation)

    # 방향에 따라 +1 또는 -1 설정
    if direction == 'f':
        step_direction = 1
    elif direction == 'r':
        step_direction = -1
    else:
        raise ValueError("Direction must be 'f' or 'r'.")

    print(f"Target angle: {rotation_degrees:.1f}°, Steps: {total_steps}")
    print("Rotating motor...")

    # 모터 회전 루프
    motor_step_counter = 0
    for _ in range(total_steps):
        # 현재 시퀀스 인덱스 계산
        seq_index = (motor_step_counter % 8) if step_direction == 1 else ((7 - motor_step_counter) % 8)
        seq = step_sequence[seq_index]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)

        motor_step_counter += step_direction
        time.sleep(step_sleep)

    print("Rotation complete!")

except KeyboardInterrupt:
    print("\n[Interrupted by user]")
    cleanup()
    exit(1)

except ValueError as ve:
    print(f"Input error: {ve}")
    cleanup()
    exit(1)

cleanup()
exit(0)
