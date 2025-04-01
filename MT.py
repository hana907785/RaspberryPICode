import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
IN1, IN2, IN3, IN4 = 23, 24, 25, 8
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
    # ⏱ 사용자 입력
    duration_minutes = float(input("Enter time in minutes (e.g., 40): "))
    total_degrees = duration_minutes * 6               # 1분 = 6도
    total_steps = int((total_degrees / 360) * 4096)    # 스텝 수 환산

    print(f"Rotating forward {total_degrees:.1f}° ({total_steps} steps)...")
    
    # 1️⃣ 빠르게 정방향 회전
    for _ in range(total_steps):
        step_forward(0.001)

    print("Now slowly returning over the full timer duration...")

    # 2️⃣ 입력한 시간 동안 서서히 역방향 복귀
    total_seconds = int(duration_minutes * 60)
    delay_between_steps = total_seconds / total_steps

    for _ in range(total_steps):
        step_backward(0)  # 실제 스텝은 바로 실행
        time.sleep(delay_between_steps)  # 간격을 조절해서 천천히 회전

    print("✅ Timer complete. Returned to starting point.")

except KeyboardInterrupt:
    print("\n[Interrupted by user]")
finally:
    GPIO.cleanup()
