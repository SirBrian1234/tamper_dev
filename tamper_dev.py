import time
import datetime
import math
import smtplib
from email.mime.text import MIMEText
import RPi.GPIO as GPIO
from L3GD20 import L3GD20
import Adafruit_LSM303

def send_email(text):
  send_email = False
  #send_email = True
  st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
  msg = MIMEText(text+"\nThis event was captured at: "+st)

  me = 'source.email@gmail.com'
  you = 'destination.email@gmail.com'

  msg['Subject'] = 'Tampering Device'
  msg['From'] = me
  msg['To'] = you

  if send_email:
    s = smtplib.SMTP_SSL('smtp.gmail.com:465')
    s.login('source.email@gmail.com','your_password')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
  
  #time.sleep(2)

# this script starts with the device itself
# in order to get it working each time you have to close the bag's zip trigger
# when the trigger is closed the device is going to send an email stating that 
# the bag is locked 

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lsm303 = Adafruit_LSM303.LSM303()

gyro = L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)
gyro.Set_PowerMode("Normal")
gyro.Set_FullScale_Value("250dps")
gyro.Set_AxisX_Enabled(True)
gyro.Set_AxisY_Enabled(True)
gyro.Set_AxisZ_Enabled(True)

delta_time = 0.2

while True:  
  while True:
    try:  
      print ('Waiting to engage lock')  
      GPIO.wait_for_edge(18, GPIO.FALLING)  
  
    except KeyboardInterrupt:  
      print('process stopped')
    
    #due to our HW - the alluminum foil, the plates are grinding over each other
    #this is the adjust time in order to let the plates settle down
    time.sleep(delta_time)
    input_state = GPIO.input(18)
    if input_state == False:
      break; 
  
  print('Lock engaged')      
  send_email('Your bag was locked!')
  
  gyro.Init()
  gyro.Calibrate()
  gyro_x = 0.0 
  gyro_y = 0.0
  gyro_z = 0.0
  
  accel, mag = lsm303.read()
  diff_accel_x, diff_accel_y, diff_accel_z = accel  
  Past_Previous_Delta_Sigma_Fxyz = 0.0
  Previous_Delta_Sigma_Fxyz = 0.0
  Current_Delta_Sigma_Fxyz = 0.0
  print"First data: {:7.2f} {:7.2f} {:7.2f}".format(diff_accel_x, diff_accel_y, diff_accel_z)

  while True:
    input_state = GPIO.input(18)
       
    if input_state == True:
      print('Lock disengaged')
      send_email('Your bag was un-locked!')
      break
      
    else:
      #accelerometer stuff
      accel, mag = lsm303.read()
      accel_x, accel_y, accel_z = accel
      
      diff_accel_x = accel_x - diff_accel_x
      diff_accel_y = accel_y - diff_accel_y
      diff_accel_z = accel_z - diff_accel_z
      
      Past_Previous_Delta_Sigma_Fxyz = Previous_Delta_Sigma_Fxyz
      Previous_Delta_Sigma_Fxyz = Current_Delta_Sigma_Fxyz
      
      Delta_Sigma_Fxy = math.sqrt(math.pow(diff_accel_x,2)+math.pow(diff_accel_y,2))
      Current_Delta_Sigma_Fxyz = math.sqrt(math.pow(Delta_Sigma_Fxy,2)+math.pow(diff_accel_z,2)) 
      #print"Curr Sigma xyz: {:7.2f} ".format(Current_Delta_Sigma_Fxyz)
            
      # now its time to detect the local maximum peaks!
      # for this task we will need three frames the present, the previous and the past previous
      # first we check if the new frame is grater than the past 
      # if yes there is yet room for an even bigger frame so we will save it
      # if the new frame is smaller than the previous then the previous might be a possible peak!
      # but only if the previous was bigger from the past_previous

      # one more thing... as good guys we have to inform the user about the
      # system's ambiguity meaning that the user has to receive not only the
      # logical interpretation of the data but also the actual data

      if Current_Delta_Sigma_Fxyz < Previous_Delta_Sigma_Fxyz:
        # this is a candidate local maximum as the previous value was bigger than the current
        if Previous_Delta_Sigma_Fxyz > Past_Previous_Delta_Sigma_Fxyz:
          # previous was definetely a peak!
          #print('local peak')
          if Previous_Delta_Sigma_Fxyz > 40:
            # Threshold noise and makse sure it's valid
            f_str = '\n\nThe force peak was measured to be\n {:7.2f} {:7.2f} {:7.2f}'.format(Past_Previous_Delta_Sigma_Fxyz, Previous_Delta_Sigma_Fxyz, Current_Delta_Sigma_Fxyz)
            if Previous_Delta_Sigma_Fxyz > 400:
              m_str = 'Your bag was kicked!'
            elif Previous_Delta_Sigma_Fxyz > 200:
              m_str = 'Your bag was pulled!'
            else:
              m_str = 'Your bag was slightly moved!'
            
            print(m_str)  
            send_email(m_str+f_str)
              
      diff_accel_x = accel_x
      diff_accel_y = accel_y
      diff_accel_z = accel_z	  	

      #gyroscope stuff
      dxyz = gyro.Get_CalOut_Value()
      # these ifs are simply noise thresholds 
      # you should change those according to your HW's behaviour
      if math.fabs(dxyz[0]*delta_time) > 1.20: 
        gyro_x += dxyz[0]*delta_time
      if math.fabs(dxyz[1]*delta_time) > 1.20:
        gyro_y += dxyz[1]*delta_time
      if math.fabs(dxyz[2]*delta_time) > 1.20:
        gyro_z += dxyz[2]*delta_time
	  		
      if math.fabs(gyro_x) > 40.0 or math.fabs(gyro_y) > 40.0 or math.fabs(gyro_z) > 40.0:
        g_data = '\n\nFrom the last point, gyroscope sensors were measured to be:\n{:7.2f} {:7.2f} {:7.2f}'.format(gyro_x, gyro_y, gyro_z)
        if gyro_x > 40.0:
          g_msg = 'Your bag was rotated anticlockwise!'
        elif gyro_x < -40.0:
          g_msg = 'Your bag was rotated clockwise!'
        elif gyro_y > 40:
          g_msg = 'Your bag was turned to its back!'
        elif gyro_y < -40.0:
          g_msg = 'Your bag was turned to its front!'
        elif gyro_z > 40.0:
          g_msg = 'Your bag was rotated sideways anticlockwise!'
        elif gyro_z < -40.0:
          g_msg = 'Your bag was rotated sideways clockwise!'
        
        print(g_msg)
        send_email(g_msg+g_data)
        gyro_x = 0
        gyro_y = 0
        gyro_z = 0
        
      time.sleep(delta_time)

