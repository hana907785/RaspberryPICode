#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 하프스텝 시퀀스
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# 설정
steps_per_rotation = 4096  # 360도 한 바퀴
step_sleep = 0.005         # 속도 조절 (필요 시 조정)

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
    # 사용자 입력
    duration_minutes = float(input("⏱ 회전 분 수 입력 (예: 15분 → 90도 회전): "))

    # ⬅ 입력된 분당 6도 계산
    rotation_degrees = duration_minutes * 6
    total_steps = int((rotation_degrees / 360) * steps_per_rotation)

    print(f"👉 회전할 각도: {rotation_degrees:.1f}°, 필요한 스텝 수: {total_steps}")

    # ⏩ 정방향 회전
    print("정방향 회전 시작...")
    motor_step_counter = 0
    for i in range(total_steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)

    time.sleep(1)

    # ⏪ 역방향 복귀
    print("역방향 복귀 중...")
    motor_step_counter = 0
    for i in range(total_steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1 + 8) % 8
        time.sleep(step_sleep)

    print("✅ 완료!")

except KeyboardInterrupt:
    print("\n[중단됨]")
    cleanup()
    exit(1)

except ValueError:
    print("⚠️ 유효한 숫자를 입력하세요.")
    cleanup()
    exit(1)

cleanup()
exit(0)
