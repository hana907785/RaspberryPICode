import RPi.GPIO as GPIO
import time

# GPIO pin setup
IN1, IN2, IN3, IN4 = 12, 16, 20, 21
MOTOR_PINS = [IN1, IN2, IN3, IN4]

GPIO.setmode(GPIO.BCM)
for pin in MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Half-step sequence (8 steps per cycle)
STEP_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

STEPS_PER_REV = 4096  # 360 degrees
STEP_DELAY = 0.002    # step speed

def step_motor(sequence, delay):
    for pattern in sequence:
        for pin, value in zip(MOTOR_PINS, pattern):
            GPIO.output(pin, value)
        time.sleep(delay)

def step_forward(n_steps):
    for _ in range(n_steps):
        step_motor(STEP_SEQUENCE, STEP_DELAY)

def step_backward(n_steps):
    for _ in range(n_steps):
        step_motor(reversed(STEP_SEQUENCE), STEP_DELAY)

def cleanup():
    for pin in MOTOR_PINS:
        GPIO.output(pin, 0)
    GPIO.cleanup()

try:
    # User input in minutes
    duration_min = int(input("Enter duration in minutes (1 min = 6 degrees): "))
    target_degrees = duration_min * 6
    total_steps = int((target_degrees / 360) * STEPS_PER_REV)

    print(f"Rotating forward by {target_degrees} degrees ({total_steps} steps)")
    step_forward(total_steps)

    print("\nStarting gradual return...")
    steps_per_minute = int((6 / 360) * STEPS_PER_REV)

    for i in range(duration_min):
        print(f"Restoring... {i + 1}/{duration_min} minutes")
        step_backward(steps_per_minute)
        time.sleep(60)  # wait 1 minute

    print("Return complete.")

except KeyboardInterrupt:
    print("\nInterrupted by user.")

finally:
    cleanup()
