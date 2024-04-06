# Building a ESP32 based antenna rotator controller

This is just a preliminary description.

Hardware required:
- ESP-WROOM-32 Devkit board. If the device will be mounted in a metallic enclosure, ESP32-WROOM-32U Devkit is recommended with
external WiFi antenna and U.FL pigtail.
- AS5600 azimuth encoder board
- NEMA23 stepper motor with 8mm shaft (56mm/2.8A is suitable, lightweight and compact) 
- 6600 type stepper motor driver, or similar, that supports 1/8 substeps
- NMRV 030 worm gearbox 1:50, with a compatible 14mm single output shaft, and an input sleeve for 8mm NEMA23 shaft.

The code is working under Micropython environment flashed to the ESP32 board.

All configuration is in the config.py file. A custom azimuth map can be placed as a rotator's web gauge background, it can be
created with the online tool at https://ns6t.net/azimuth/ , then properly cropped as a square bitmap and saved as a 400x400 pixels image file in static/azmap_s.jpg .

Alternatively, use the included azmap_gen/azmap_gen.py Python script to generate azimuthal map file for your QTH locator. It looks much better.

The only wiring to the rotator is just a power supply (14 Volts 1A max is enough), it then connects to the preconfigured WiFi
network and appears as a web server in your LAN.

Rotator is controlled remotely with a web interface running on ESP32 under the Microdot web server. The interface uses websockets
for live updates and command submissions. This is how the web interface is displayed in my browser:

![screenshot](https://github.com/EU1KY/rotator/assets/1841648/e5671847-bbd6-40ab-9ff1-d925bf39c139)

There is a FTP server that runs in the background. The updated python and HTML/CSS files can then be uploaded with a convenient FTP client,
even with Windows Explorer. Thus, on-the-air code updating is possible. The device automatically resets after FTP client disconnection
to apply changes. But be careful: if your files have critical bugs, the device can be bricked and you will need to put the antenna down
to connect to the device directly for recovery. Be especially careful when updating the boot.py and config.py files. 

My current working prototype:

![prototype_1](https://github.com/EU1KY/rotator/assets/1841648/d35414da-c701-420c-ae66-c1df03fdd736)
![prototype_2](https://github.com/EU1KY/rotator/assets/1841648/a3a52a5f-4010-4889-8b40-02e133d503e9)
![prototype_3](https://github.com/EU1KY/rotator/assets/1841648/304d80ba-6bec-44a8-8fd8-6762de2d77b1)

Здесь черновик подробной инструкции, что и как делать, пока только на русском: https://github.com/EU1KY/rotator/wiki
