import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)
StepPins = [12, 16, 20, 21]

# 핀 설정
for pin in StepPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# 스텝 시퀀스 정의
StepCount = 4
Seq = [[0,0,0,1],
       [0,0,1,0],
       [0,1,0,0],
       [1,0,0,0]]

def rotate_motor(steps, direction=1, speed=0.01):
    """모터를 지정된 스텝 수만큼 회전"""
    StepCounter = 0
    total_steps = abs(steps)
    
    for _ in range(total_steps):
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
                
        StepCounter += direction
        if StepCounter >= StepCount:
            StepCounter = 0
        if StepCounter < 0:
            StepCounter = StepCount - 1
            
        time.sleep(speed)

try:
    # 사용자 입력 받기
    duration = float(input("회전할 시간(초)을 입력하세요: "))
    
    # 60도가 85스텝이라고 가정 (360도 = 512스텝 기준, 60도 = 512/6 ≈ 85)
    steps_for_60_degrees = 85
    # 시간당 스텝 수 계산 (duration 동안 60도 회전)
    steps_per_second = steps_for_60_degrees / duration if duration > 0 else 85
    total_steps = int(steps_per_second * duration)
    
    print(f"목표 스텝 수: {total_steps} (최대 60도)")

    # 0도에서 60도까지 회전
    print("60도로 이동 중...")
    rotate_motor(total_steps, direction=1, speed=0.01)
    
    # 잠시 대기
    time.sleep(1)
    
    # 다시 0도로 복귀
    print("0도로 복귀 중...")
    rotate_motor(total_steps, direction=-1, speed=0.01)
    
except KeyboardInterrupt:
    print("\n프로그램 종료")
    GPIO.cleanup()
except ValueError:
    print("유효한 숫자를 입력해주세요")
    GPIO.cleanup()

finally:
    GPIO.cleanup()
