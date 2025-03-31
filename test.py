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
    # 사용자 입력 받기 (분 단위)
    duration_minutes = float(input("회전할 시간(분)을 입력하세요: "))
    
    # 360도(1회전) = 512스텝, 60분 동안 360도 회전
    steps_per_rotation = 512  # 1회전 스텝 수
    total_time_seconds = 60 * 60  # 60분 = 3600초
    steps_per_second = steps_per_rotation / total_time_seconds  # 초당 스텝 수
    
    # 입력된 시간(분)을 초 단위로 변환
    duration_seconds = duration_minutes * 60
    total_steps = int(steps_per_second * duration_seconds)  # 목표 스텝 수
    
    # 속도 계산: 입력 시간 동안 total_steps를 수행하도록
    if total_steps > 0:
        speed = duration_seconds / total_steps  # 각 스텝당 시간(초)
    else:
        speed = 0.01  # 기본값
    
    print(f"목표 스텝 수: {total_steps} (최대 360도)")

    # 0도에서 목표 각도까지 회전
    print("목표 각도로 이동 중...")
    rotate_motor(total_steps, direction=1, speed=speed)
    
    # 잠시 대기
    time.sleep(1)
    
    # 다시 0도로 복귀
    print("0도로 복귀 중...")
    rotate_motor(total_steps, direction=-1, speed=speed)
    
except KeyboardInterrupt:
    print("\n프로그램 종료")
    GPIO.cleanup()
except ValueError:
    print("유효한 숫자를 입력해주세요")
    GPIO.cleanup()

finally:
    GPIO.cleanup()
