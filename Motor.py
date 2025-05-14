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

steps_per_rotation = 4076         # 360도 기준
step_sleep = 0.001                # 속도 조절 (빠른 회전)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

try:
    duration_minutes = float(input("input time : "))
    degrees_to_move = duration_minutes * 6
    steps_to_move = int((degrees_to_move / 360) * steps_per_rotation)

    print(f"➡ 정방향 {degrees_to_move:.1f}도 회전 중 ({steps_to_move} 스텝)")
    motor_step_counter = 0

    # 정방향 회전
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep)

    time.sleep(1)  # 잠깐 멈춤

    print("reverse...")
    for _ in range(steps_to_move):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)

    print("complete!")

except KeyboardInterrupt:
    print("\n[사용자 종료]")
finally:
    cleanup()
