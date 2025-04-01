import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 하프스텝 시퀀스
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

GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

try:
    # 각도 및 시간 설정
    degrees_to_move = 30
    total_seconds = 5 * 60  # 5분 = 300초
    steps_per_degree = 4076 / 360
    total_steps = int(degrees_to_move * steps_per_degree)
    delay_per_step = total_seconds / total_steps  # 약 0.88초

    print(f"⏳ Slowly rotating {degrees_to_move}° over 5 minutes...")
    motor_step_counter = 0

    for _ in range(total_steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(delay_per_step)

    print("✅ Rotation complete.")

except KeyboardInterrupt:
    print("\n[Interrupted]")
finally:
    cleanup()
