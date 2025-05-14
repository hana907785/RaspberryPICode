import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 하프 스텝 시퀀스
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

steps_per_rotation = 4096            # 360도 회전 기준
step_sleep = 0.001                   # 빠른 회전 속도

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def step_motor(steps, forward=True, delay=0.001):
    idx = 0
    for _ in range(steps):
        for pin, val in zip(motor_pins, step_sequence[idx]):
            GPIO.output(pin, val)
        idx = (idx - 1) % 8 if forward else (idx + 1) % 8
        time.sleep(delay)

try:
    duration_minutes = float(input("⏱ 몇 분 설정할까요? (예: 10): "))
    degrees_to_move = duration_minutes * 6
    total_steps = int((degrees_to_move / 360) * steps_per_rotation)

    # ✅ 정방향 즉시 회전
    print(f"➡ 정방향 {degrees_to_move:.1f}도 회전 중 ({total_steps} 스텝)")
    step_motor(total_steps, forward=True, delay=step_sleep)

    # ✅ 역방향 복귀: 1분마다 6도씩 천천히 복귀
    print("⬅ 역방향 천천히 복귀 중...")

    for minute in range(int(duration_minutes)):
        print(f"  🔄 {minute+1}분 경과 - 6도 복귀")
        step_motor(int((6 / 360) * steps_per_rotation), forward=False, delay=0.003)
        time.sleep(60)  # 1분 대기

    print("✅ 복귀 완료!")

except KeyboardInterrupt:
    print("\n[사용자 종료]")
finally:
    cleanup()
