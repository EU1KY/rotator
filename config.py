class RotatorConfig:
    WIFI_SSID = 'Your_WiFi_SSID'
    WIFI_PASSWD = 'Your_WiFi_password'
    AZ_CORRECTION = -6
    PWM_PIN = 4
    DIR_PIN = 16
    EN_PIN = 17
    DIRCW = 0         #Clockwise rotation polarity value
    DIRCCW = 1        #Counter-clockwise rotation polarity value
    ROTENABLE = 0     #Rotation enable polarity value
    ROTDISABLE = 1    #Rotation disable polarity value
    FREQ_LO  = 500
    FREQ_MID = 1000
    FREQ_HI = 2000
    ROT_THRESHOLD_HI = 15
    ROT_THRESHOLD_LO = 7
    I2C_SCL_PIN = 22
    I2C_SDA_PIN = 21
