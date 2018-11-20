#coding:utf8
from __future__ import print_function
import time
import argparse

import RPi.GPIO as GPIO


def process(input_channel, output_channel, timeout):
    print('Waiting for button pressed for LED-OFF')
    GPIO.wait_for_edge(input_channel, GPIO.RISING)
    print('Button pressed')

    GPIO.output(output_channel, GPIO.HIGH) # LED OFF

    print('Waiting for button pressed for LED-ON')
    channel = GPIO.wait_for_edge(input_channel, GPIO.RISING, timeout=timeout*1000)
    if not channel:
        print('Timeout, auto on')
    else:
        print('Receive signal')
    GPIO.output(output_channel, GPIO.LOW)  # LED ON


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input-channel', type=int, default=11) # PIN 11/GPIO 0
    p.add_argument('--output-channel', type=int, default=18) # PIN 18/GPIO 5
    p.add_argument('--timeout', type=int, default=10, help='timeout seconds')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(args.input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(args.output_channel, GPIO.OUT, initial=GPIO.LOW)

    try:
        while True:
            process(args.input_channel, args.output_channel, args.timeout)
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
