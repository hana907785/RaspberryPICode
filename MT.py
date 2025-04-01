import RPi.GPIO as GPIO
import time

# 핀 설정
IN1, IN2, IN3, IN4 = 12, 16, 20, 21
GPIO.setmode(GPIO.BCM)
for pin in (IN1, IN2, IN3, IN4):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# 하프스텝 시퀀스
halfstep_seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0], 
    [1, 1, 0, 0], 
    [0, 1, 0, 0], 
    [0, 1, 1, 0], 
    [0, 0, 1, 0], 
    [0, 0, 1, 1], 
    [0, 0, 0, 1]
]

def step_motor(sequence, delay):
    for pattern in sequence:
        GPIO.output(IN1, pattern[0])
        GPIO.output(IN2, pattern[1])
        GPIO.output(IN3, pattern[2])
        GPIO.output(IN4, pattern[3])
        time.sleep(delay)

def step_forward(delay=0.005):
    step_motor(halfstep_seq, delay)

def step_backward(delay=0.005):
    step_motor(reversed(halfstep_seq), delay)

try:
    duration_minutes = float(input("Enter time in minutes (e.g., 15): "))

    degrees_to_rotate = duration_minutes * 6           # 1분 = 6도
    steps_per_revolution = 2038                        # 정확한 360도 스텝 수
    steps_to_move = int((degrees_to_rotate / 360) * steps_per_revolution)

    print(f"▶ Fast rotate {degrees_to_rotate:.1f}° → {steps_to_move} steps")
    for _ in range(steps_to_move):
        step_forward(0.001)

    print("⏳ Starting slow reverse timer...")
    total_seconds = duration_minutes * 60
    delay_between_steps = total_seconds / steps_to_move

    for _ in range(steps_to_move):
        step_backward(0)
        time.sleep(delay_between_steps)

    print("✅ Done! Returned to 0°")

except KeyboardInterrupt:
    print("\n[Interrupted]")
finally:
    GPIO.cleanup()
