import RPi.GPIO as GPIO
import time

# GPIO pin configuration
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# Step sequence (based on original code)
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

steps_per_rotation = 4076  # Steps for 360 degrees
step_sleep = 0.002         # Step delay (adjusted for stability)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    """Reset all motor pins and cleanup GPIO."""
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def rotate_reverse_6_degrees():
    """Rotate 6 degrees in reverse (approx. 68 steps)."""
    steps_for_6_degrees = int((6 / 360) * steps_per_rotation)  # Approx. 68 steps
    motor_step_counter = 0
    for _ in range(steps_for_6_degrees):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8  # Reverse direction
        time.sleep(step_sleep)
    return steps_for_6_degrees

try:
    # Get user input
    duration_minutes = float(input("Enter duration in minutes (e.g., 30): "))
    total_degrees = duration_minutes * 6
    total_steps = int((total_degrees / 360) * steps_per_rotation)

    print(f"Starting reverse rotation: {duration_minutes:.0f} minutes, "
          f"{total_degrees:.1f} degrees, {total_steps} steps")

    # Rotate 6 degrees in reverse every minute
    for minute in range(int(duration_minutes)):
        print(f"[Minute {minute + 1}/{duration_minutes:.0f}] Rotating 6 degrees in reverse...")
        steps_moved = rotate_reverse_6_degrees()
        remaining_minutes = duration_minutes - (minute + 1)
        print(f"Completed! Remaining: {remaining_minutes:.0f} minutes, "
              f"Cumulative rotation: {(minute + 1) * 6:.1f} degrees")
        
        # Wait 1 minute unless it's the last rotation
        if minute < duration_minutes - 1:
            time.sleep(60)

    print("Rotation completed successfully!")

except KeyboardInterrupt:
    print("\n[Stopped by user]")
except ValueError as ve:
    print(f"Input error: {ve}")
finally:
    cleanup()
