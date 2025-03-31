import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
StepPins = [12, 16, 20, 21]

for pin in StepPins: 
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

StepCounter = 0
StepCount = 8  # 8스텝 시퀀스로 변경

# 반/반상 구동 시퀀스 (28BYJ-48 기준)
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]

try:
    # 사용자 입력 받기 (분 단위)
    duration_minutes = float(input("회전할 시간(분)을 입력하세요: "))
    
    # 360도 = 2048스텝 (28BYJ-48 기준)
    steps_per_rotation = 2048  # 360도에 해당하는 스텝 수
    reference_minutes = 60     # 기준 시간(60분)
    
    # 입력값에 비례한 스텝 수 계산
    total_steps = int(steps_per_rotation * (duration_minutes / reference_minutes))
    
    print(f"계산된 스텝 수: {total_steps}")
    print(f"예상 회전 각도: {total_steps / steps_per_rotation * 360:.2f}도")

    # 정방향 회전 (0도 -> 목표 각도)
    print("목표 각도로 이동 중...")
    for step in range(total_steps):
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
            StepCounter = StepCount - 1
        
        # 속도 조정: 초반 느리게, 점차 정상 속도
        sleep_time = 0.02 if step < 100 else 0.01  # 처음 100스텝은 느리게
        time.sleep(sleep_time)
        
        if (step + 1) % 512 == 0:
            print(f"현재 스텝: {step + 1}, 예상 각도: {(step + 1) / steps_per_rotation * 360:.2f}도")

    # 잠시 대기
    time.sleep(1)
    
    # 역방향 회전 (목표 각도 -> 0도)
    print("0도로 복귀 중...")
    for step in range(total_steps):
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
        
        sleep_time = 0.02 if step < 100 else 0.01  # 처음 100스텝은 느리게
        time.sleep(sleep_time)
        
        if (step + 1) % 512 == 0:
            print(f"복귀 중 스텝: {step + 1}, 예상 각도: {(total_steps - (step + 1)) / steps_per_rotation * 360:.2f}도")

except KeyboardInterrupt:
    print("\n프로그램 종료")
    GPIO.cleanup()
except ValueError:
    print("유효한 숫자를 입력해주세요")
    GPIO.cleanup()

finally:
    GPIO.cleanup()
