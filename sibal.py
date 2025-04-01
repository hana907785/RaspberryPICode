#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21

# 속도 설정
step_sleep = 0.01  # 스텝 간 시간 (작을수록 빠름)
steps_per_rotation = 4096  # 360도 회전 기준 스텝 수

# 하프스텝 시퀀스 (28BYJ-48 전용)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# 모든 핀 LOW로 시작
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

motor_pins = [in1, in2, in3, in4]

# GPIO 정리 함수
def cleanup():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.cleanup()

try:
    # 사용자 입력
    duration_minutes = float(input("Enter rotation time (minutes): "))
    total_steps = int(steps_per_rotation * (duration_minutes / 60))

    print(f"Calculated steps: {total_steps}")
    print(f"Expected rotation angle: {total_steps / steps_per_rotation * 360:.2f} degrees")

    # 🌀 정방향 회전
    print("Moving to target angle...")
    motor_step_counter = 0  # ⬅ 정방향 시작 전 초기화
    for i in range(total_steps):
        current_sequence = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, current_sequence):
            GPIO.output(pin, val)

        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)

        if (i + 1) % 512 == 0:
            print(f"Forward step: {i + 1}, Angle: {(i + 1) / steps_per_rotation * 360:.2f}°")

    time.sleep(1)

    # 🔁 역방향 회전
    print("Returning to 0 degrees...")
    motor_step_counter = 0  # ⬅ 역방향 시작 전 초기화
    for i in range(total_steps):
        current_sequence = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, current_sequence):
            GPIO.output(pin, val)

        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep)

        if (i + 1) % 512 == 0:
            print(f"Reverse step: {i + 1}, Remaining Angle: {(total_steps - (i + 1)) / steps_per_rotation * 360:.2f}°")

except KeyboardInterrupt:
    print("\n[Interrupted]")
    cleanup()
    exit(1)

except ValueError:
    print("⚠️ Please enter a valid number.")
    cleanup()
    exit(1)

# 마무리 정리
cleanup()
exit(0)
