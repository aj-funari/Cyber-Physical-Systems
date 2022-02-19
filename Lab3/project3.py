from AlphaBot2 import AlphaBot2
from TRSensors import TRSensor
from PIDclass import pidclass
import time

PID = pidclass()
TR = TRSensor()
Ab = AlphaBot2()

Ab.stop()
print("Line follow Example")
time.sleep(0.5)
for i in range(0,100):
	if(i<25 or i>= 75):
		Ab.right()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	else:
		Ab.left()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	TR.calibrate()
Ab.stop()
Ab.forward()

maximum = 80
integral = 0
last_proportional = 0
count = 0

start_time = time.perf_counter()
while True: 
	timestamp = time.perf_counter()
	position,Sensors = TR.readLine()  # black line reads value close to 1000
	if(Sensors[0] >800 and Sensors[1] >800 and Sensors[2] >800 and Sensors[3] >800 and Sensors[4] >800):
		Ab.setPWMA(0)
		Ab.setPWMB(0)
		loop_time = (time.perf_counter() - start_time)
		print(loop_time)
		exit(1)
	else:
		# The "proportional" term should be 0 when we are on the line.
		error = position - 2000 
		
		# Compute the derivative (change) and integral (sum) of the position.
		derivative = error - last_proportional
		integral += error
		
		# Remember the last position.
		last_proportional = error

		pterm = error*.04
		iterm = integral*1/10000
		dterm = derivative*6
		# iterm = 0
		# dterm = 0

		# output = pterm 
		# output = pterm + dterm
		output = pterm + iterm + dterm 

		if (output > maximum):
			output = maximum
		if (output < - maximum):
			output = - maximum
		# print(position,output)
		if (output < 0):
			left = maximum + output
			right = maximum
			Ab.setPWMA(left)
			Ab.setPWMB(right)
		else:
			left = maximum
			right = maximum - output
			Ab.setPWMA(left)
			Ab.setPWMB(right)
		
		runtime = (time.perf_counter() - timestamp)  # duration of control loop
		target = 0.006  # 200Hz 
		x = target - runtime  # sleep time -> difference between target and runtime
		time.sleep(x)  # sleep for difference
		total_time = (time.perf_counter() - timestamp)  # should be within +/- 2% of target time 
		dev = PID.freq(target, total_time)  # computation to find if time is withint +/- 2%


		if count % 20 == 0:
			PID.loginfo(timestamp, dev, error, pterm, iterm, dterm, left, right)
			#print("Info Logged!")
		count += 1