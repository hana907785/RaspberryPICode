import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 시퀀스 (이미 잘 작동했던 방향 기준)
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

steps_per_rotation = 4076  # 360도 회전 기준
step_sleep = 0.001

GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

try:
    # ✅ 15도에 해당하는 스텝 수 계산
    degrees_to_move = 15
    steps_to_move = int((degrees_to_move / 360) * steps_per_rotation)
    print(f"Moving {degrees_to_move}° → {steps_to_move} steps")

    motor_step_counter = 0

    # ⏩ 정방향 15도
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep)

    time.sleep(1)

    # ⏪ 역방향 15도
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)

    print("✅ Done. Moved 15° forward and back.")

except KeyboardInterrupt:
    print("\n[Interrupted]")
finally:
    cleanup()
