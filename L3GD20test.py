#!/usr/bin/python

from L3GD20 import L3GD20

import time

# Communication object
s = L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)

# Preconfiguration
s.Set_PowerMode("Normal")
s.Set_FullScale_Value("250dps")
s.Set_AxisX_Enabled(True)
s.Set_AxisY_Enabled(True)
s.Set_AxisZ_Enabled(True)

# Print current configuration
s.Init()
s.Calibrate()

# Calculate angle
dt = 0.2
gyro_x = 0
gyro_y = 0
gyro_z = 0
while True:
	time.sleep(dt)
	dxyz = s.Get_CalOut_Value()
	gyro_x += dxyz[0]*dt;
	gyro_y += dxyz[1]*dt;
	gyro_z += dxyz[2]*dt;
	print("{:7.2f} {:7.2f} {:7.2f}".format(gyro_x, gyro_y, gyro_z))


