import RPi.GPIO as GPIO
import time

# BCM 모드로 설정
GPIO.setmode(GPIO.BCM)

# 스텝모터 제어 핀 설정 (IN1 ~ IN4)
control_pins = [12, 16, 20, 21]

# 출력 핀으로 설정
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# 28BYJ-48의 하프스텝 시퀀스 (8단계)
halfstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

try:
    steps = 512  # 약 360도 회전 (하프스텝 기준)
    delay = 0.002  # 스텝 간 딜레이 (속도 조절 가능)

    print("스텝모터 회전 시작!")
    for i in range(steps):
        for step in halfstep_seq:
            for pin in range(4):
                GPIO.output(control_pins[pin], step[pin])
            time.sleep(delay)

    print("✅ 회전 완료!")

except KeyboardInterrupt:
    print("⛔ 사용자 중단")

finally:
    GPIO.cleanup()
