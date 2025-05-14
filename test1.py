import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 시퀀스 (정방향 기준)
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

steps_per_rotation = 4076
step_sleep_fast = 0.001
step_sleep_reverse = 0.001  # 역방향 속도

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def move_motor(steps, direction, step_delay):
    global motor_step_counter
    for _ in range(steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        if direction == "forward":
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction == "backward":
            motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_delay)

try:
    duration_minutes = int(input("⏱ 몇 분 설정할까요? (예: 10): "))
    total_degrees = duration_minutes * 6
    total_steps = int((total_degrees / 360) * steps_per_rotation)
    steps_per_minute = total_steps // duration_minutes

    print(f"➡ 정방향 {total_degrees}도 이동 중 ({total_steps} 스텝)")
    motor_step_counter = 0
    move_motor(total_steps, direction="forward", step_delay=step_sleep_fast)

    print("⏳ 타이머 시작! 1분마다 6도씩 역방향 복귀 중...")
    for i in range(duration_minutes):
        time.sleep(60)  # 1분 대기
        print(f"⬅ {i+1}분 경과: 역방향 {6 * (i+1)}도 복귀 중...")
        move_motor(steps_per_minute, direction="backward", step_delay=step_sleep_reverse)

    print("✅ 전체 복귀 완료!")

except KeyboardInterrupt:
    print("\n[사용자 종료]")
finally:
    cleanup()
