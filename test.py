import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
StepPins = [12, 16, 20, 21]

for pin in StepPins: 
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

StepCounter = 0
StepCount = 4

Seq = [[0,0,0,1],
       [0,0,1,0],
       [0,1,0,0],
       [1,0,0,0]]

try:
    # 사용자 입력 받기 (분 단위)
    duration_minutes = float(input("회전할 시간(분)을 입력하세요: "))
    
    # 360도(512스텝)를 60분에 매핑
    steps_per_rotation = 512  # 360도에 해당하는 스텝 수
    reference_minutes = 60    # 기준 시간(60분)
    
    # 입력 시간에 비례한 스텝 수 계산 (60분 = 512스텝)
    total_steps = int(steps_per_rotation * (duration_minutes / reference_minutes))
    
    print(f"목표 스텝 수: {total_steps}")

    # 정방향 회전 (0도 -> 목표 각도)
    print("목표 각도로 이동 중...")
    for _ in range(total_steps):
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        
        StepCounter += 1
        if StepCounter == StepCount:
            StepCounter = 0
        if StepCounter < 0:
            StepCounter = StepCount
        
        time.sleep(0.01)  # 원본 속도 유지
    
    # 잠시 대기
    time.sleep(1)
    
    # 역방향 회전 (목표 각도 -> 0도)
    print("0도로 복귀 중...")
    for _ in range(total_steps):
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        
        StepCounter -= 1  # 역방향으로 이동
        if StepCounter == StepCount:
            StepCounter = 0
        if StepCounter < 0:
            StepCounter = StepCount - 1
        
        time.sleep(0.01)  # 원본 속도 유지

except KeyboardInterrupt:
    print("\n프로그램 종료")
    GPIO.cleanup()
except ValueError:
    print("유효한 숫자를 입력해주세요")
    GPIO.cleanup()

finally:
    GPIO.cleanup()
