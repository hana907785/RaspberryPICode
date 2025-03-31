import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
control_pins = [12, 16, 20, 21]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# 정확한 하프스텝 시퀀스
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

delay = 0.005  # 5ms: 느리지만 확실히 움직임

print("모터 회전 테스트 시작!")
try:
    for i in range(512):  # 약 360도 회전
        for step in halfstep_seq:
            for pin in range(4):
                GPIO.output(control_pins[pin], step[pin])
            time.sleep(delay)
    print("✅ 회전 완료!")

except KeyboardInterrupt:
    print("중지됨")

finally:
    GPIO.cleanup()
