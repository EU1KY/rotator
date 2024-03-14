# Building a ESP32 based antenna rotator controller

This is just a preliminary description.

Hardware required:
- ESP-WROOM-32 board
- AS5600 azimuth encoder board
- NEMA23 stepper motor with 8mm shaft (56mm/2.8A is suitable enough) 
- 6600 type stepper motor driver, or similar, that supports 1/8 substeps
- NMRV 030 worm gearbox 1:50, with a compatible 14mm single output shaft, and an input sleeve for 8mm NEMA23 shaft.

The code is working under Micropython environment flashed to the ESP32 board.

All configuration is in the config.py file. A custom azimuth map can be placed as a rotator's web gauge background, it can be created with the online tool at https://ns6t.net/azimuth/ , then properly cropped as a square bitmap and saved as a 400x400 pixels image file in static/azmap_s.jpg .

Rotator is controlled remotely with a web interface running on the Microdot web server, all the updates are pushed to browser with websockets. This is how the web interface is displayed in my browser:

![screenshot](https://github.com/EU1KY/rotator/assets/1841648/e5671847-bbd6-40ab-9ff1-d925bf39c139)

There is a FTP server that can be started by accessing /ftp, the web server stops working in this case. The updated python and HTML/CSS files can then be uploaded with a convenient FTP client.
