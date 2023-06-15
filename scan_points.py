import os
import ydlidar
import time
import sys
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import math

import RPi.GPIO as GPIO
from time import sleep
ydlidar.os_init();

f = open("a.txt", 'a')

servo_pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

pwm=GPIO.PWM(servo_pin, 50)
pwm.start(0)

fig = plt.figure()
fig.canvas.set_window_title('Human Detection Moniter')
lidar_polar = plt.subplot(projection = '3d')

ports = ydlidar.lidarPortList();
port = "/dev/ydlidar";
for key, value in ports.items():
	port = value;

laser = ydlidar.CYdLidar();
laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200) 
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
laser.setlidaropt(ydlidar.LidarPropSampleRate, 3)
laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
laser.setlidaropt(ydlidar.LidarPropMaxRange, 16.0)
laser.setlidaropt(ydlidar.LidarPropMinRange, 0.08)
laser.setlidaropt(ydlidar.LidarPropIntenstiy, False)
ret = laser.initialize();

scanning = True
x = []
y = []
z = []

angle_h_real = 9
angle_h = 30

if ret:
	ret = laser.turnOn();
	scan = ydlidar.LaserScan()
	while ret and ydlidar.os_isOk() :
		r = laser.doProcessSimple(scan);
		if r:
			
			for point in scan.points:
				seta   = math.radians((point.angle * 60))
				rang   = point.range
				seta_h = math.radians(angle_h)
				
				xdata = rang * math.cos(seta)
				ydata = rang * math.sin(seta)
				zdata = rang * math.tan(seta_h)
				
				if xdata < 0.5 and ydata < 0.5 and zdata < 0.5:
					x.append(xdata)

					# y.append(ydata)
					# if (rang * math.cos(seta)) > 0:
					# 	z.append(zdata)
					# else:
					# 	z.append(zdata * -1)

					if ydata > 0:
						y.append(ydata)
					else:
						y.append(ydata * -1)
					z.append(zdata)
					
			time.sleep(0.05);
			
		if angle_h_real < 6.1:
			break
		else: 
			pwm.ChangeDutyCycle(angle_h_real)
			sleep(0.07)
			angle_h_real -= 0.05
			angle_h -= 1
			
pwm.stop()

laser.turnOff();
laser.disconnecting();

f.write('\n\n\n')
f.write('xxx\n')
f.write(str([round(i,2) for i in x]))
f.write('yyy\n')
f.write(str([round(i,2) for i in y]))
f.write('zzz\n')
f.write(str([round(i,2) for i in z]))
f.write('\n\n\n')

f.close()
			
lidar_polar.scatter(x, y, z, marker=".")
plt.show()




