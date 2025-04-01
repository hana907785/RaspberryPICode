import RPi.GPIO as GPIO
import time

# GPIO pin setup
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# Half-step sequence (forward)
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

steps_per_rotation = 4076  # One full rotation = 360 degrees
step_sleep_fast = 0.001    # Delay for fast rotation

# GPIO initialization
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

try:
    duration_minutes = float(input("Enter timer duration in minutes (e.g., 15): "))
    degrees_to_move = duration_minutes * 6
    steps_to_move = int((degrees_to_move / 360) * steps_per_rotation)

    print(f"➡ Rotating forward {degrees_to_move:.1f}° ({steps_to_move} steps)")
    motor_step_counter = 0

    # Fast forward rotation
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep_fast)

    print("⏳ Timer running... slowly returning")
    total_seconds = duration_minutes * 60
    delay_per_step = total_seconds / steps_to_move

    # Slow backward rotation
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(delay_per_step)

    print("✅ Returned to starting position.")

except KeyboardInterrupt:
    print("\n[Interrupted by user]")
finally:
    cleanup()
