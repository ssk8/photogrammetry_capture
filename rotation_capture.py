#!/usr/bin/python3

import smbus
from picamera import PiCamera
from datetime import datetime
from os import mkdir
from time import sleep

i2c_bus = smbus.SMBus(1)

def send_i2c(n):
    i2c_bus.write_block_data(0x08, 0x00, list(divmod(n, 255)))


def step_enable(enable):
    DISABLE = 65279
    ENABLE = 65278
    send_i2c(enable*ENABLE or DISABLE)


def take_picture(cam):
    try:
        cam.capture(f'/home/pi/Pictures/{datetime.now().strftime("%y%m%d%H%M%S")}.jpg', format='jpeg')
    except FileNotFoundError:
        mkdir("/home/pi/Pictures")
        take_picture(cam)


def close(cam):
    step_enable(False)
    cam.close()
    print(f'\ngooodbye\n')


def main():
    send_i2c(0)
    step_enable(True)

    try:
        camera = PiCamera()
        camera.iso = 800
        sleep(2)
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        camera.resolution = (4056, 3040)
        for clicks in range(0, 3200, 80):
            send_i2c(clicks)
            sleep(3)
            take_picture(camera)
            sleep(3)
        close(camera)
    except KeyboardInterrupt:
        close(camera)


if __name__ == "__main__":
    main()
