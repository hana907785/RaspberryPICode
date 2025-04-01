#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 하나의 정방향 시퀀스만 사용 (현재 하드웨어 기준에서 역방향으로 동작함)
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

    # 방향에 따라 step_direction 설정 (❗정방향은 -1, 역방향은 +1)
    if direction == 'f':
        step_direction = -1  # 실제 정방향 회전
    elif direction == 'r':
        step_direction = 1   # 실제 역방향 회전
    else:
        raise ValueError("Direction must be 'f' or 'r'.")

    print(f"Target angle: {rotation_degrees:.1f}°, Steps: {total_steps}")
    print("Rotating motor...")

    # 모터 회전 루프
    motor_step_counter = 0
    for _ in range(total_steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)

        motor_step_counter = (motor_step_counter + step_direction) % 8
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
