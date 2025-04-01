import RPi.GPIO as GPIO
import time

# 핀 설정 (너가 쓰던 순서 그대로)
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 정확히 작동하던 시퀀스
step_sequence = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

# ✅ 여기서 사용하는 기준 스텝 수는 실제로 잘 돌아가던 값: 4076
steps_per_rotation = 4076
step_sleep_fast = 0.001  # 빠른 초기 회전
step_sleep_slow = 0      # 느린 복귀 (간격은 time.sleep으로 조절)

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
    duration_minutes = float(input("Enter duration in minutes (1 min = 6 degrees): "))
    rotation_degrees = duration_minutes * 6
    steps_to_move = int((rotation_degrees / 360) * steps_per_rotation)

    print(f"Target angle: {rotation_degrees:.1f}°, Steps: {steps_to_move}")
    print("▶ Fast rotating to target angle...")

    # ⏩ 빠르게 정방향 회전 (작동했던 방향)
    motor_step_counter = 0
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep_fast)

    # ⏳ 복귀 시작
    print("⏳ Returning slowly over time...")

    total_seconds = duration_minutes * 60
    delay_between_steps = total_seconds / steps_to_move

    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(delay_between_steps)

    print("✅ Done! Back to 0°")

except KeyboardInterrupt:
    print("\n[Interrupted]")
finally:
    cleanup()
