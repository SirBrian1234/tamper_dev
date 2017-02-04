# Simple demo of of the LSM303 accelerometer & magnetometer library.
# Will print the accelerometer & magnetometer X, Y, Z axis values every half
# second.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the LSM303 module.
import Adafruit_LSM303

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

print('Printing accelerometer & magnetometer X, Y, Z axis values, press Ctrl-C to quit...')

# Read the X, Y, Z axis acceleration values and print them.
accel, mag = lsm303.read()
diff_accel_x, diff_accel_y, diff_accel_z = accel

while True:
    # Read the X, Y, Z axis acceleration values and print them.
    accel, mag = lsm303.read()
    
    # Grab the X, Y, Z components from the reading and print them out.
    accel_x, accel_y, accel_z = accel
    
    diff_accel_x = diff_accel_x - accel_x
    diff_accel_y = diff_accel_y - accel_y
    diff_accel_z = diff_accel_z - accel_z		

    mag_x, mag_z, mag_y = mag
    #print('Accel X={0}, Accel Y={1}, Accel Z={2}, Mag X={3}, Mag Y={4}, Mag Z={5}'.format(
    #      accel_x, accel_y, accel_z, mag_x, mag_y, mag_z))

    #print('delta Accel X={0}, Accel Y={1}, Accel Z={2}'.format(diff_accel_x, diff_accel_y, diff_accel_z))

    
    #print('delta Accel Z={0}'.format(diff_accel_z))
    

    if (diff_accel_x or diff_accel_y or diff_accel_z) > 10:
    	print('Apisteuto kounithike!!!')


    diff_accel_x = accel_x
    diff_accel_y = accel_y
    diff_accel_z = accel_z	    

    # Wait half a second and repeat.
    time.sleep(0.5)
    
