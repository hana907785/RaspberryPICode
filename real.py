import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (BCM 모드)
IN1, IN2, IN3, IN4 = 23, 24, 25, 8  # 예시 핀번호
GPIO.setmode(GPIO.BCM)
for pin in (IN1, IN2, IN3, IN4):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# 하프스텝 시퀀스 정의 (8개의 코일 온오프 패턴)
halfstep_seq = [
    [1, 0, 0, 1],  # IN1,IN4 활성 (예시 패턴 시작)
    [1, 0, 0, 0], 
    [1, 1, 0, 0], 
    [0, 1, 0, 0], 
    [0, 1, 1, 0], 
    [0, 0, 1, 0], 
    [0, 0, 1, 1], 
    [0, 0, 0, 1]   # IN4 활성 (예시 패턴 끝)
]

def step_motor(sequence, delay):
    """시퀀스 리스트 하나(예: halfstep_seq)를 한 사이클 수행하여 모터를 한 스텝 회전"""
    for pattern in sequence:
        GPIO.output(IN1, pattern[0])
        GPIO.output(IN2, pattern[1])
        GPIO.output(IN3, pattern[2])
        GPIO.output(IN4, pattern[3])
        time.sleep(delay)

# 정방향 한 스텝 (halfstep_seq 순서대로)
def step_forward(delay=0.005):
    step_motor(halfstep_seq, delay)

# 역방향 한 스텝 (halfstep_seq를 역순으로)
def step_backward(delay=0.005):
    step_motor(reversed(halfstep_seq), delay)

# 예제: 정방향 512 스텝(약 45도) 회전 후 역방향 512 스텝 회전
for _ in range(512):
    step_forward(0.001)  # 빠르게 512스텝 정방향
for _ in range(512):
    step_backward(0.001)  # 빠르게 512스텝 역방향
