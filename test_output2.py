#coding:utf8
from __future__ import print_function
import time
import argparse

import RPi.GPIO as GPIO


def process_signal(channel):
    print('Button pressed')
    GPIO.output(args.output_channel, GPIO.HIGH) # LED OFF
    time.sleep(args.delay_time/1000)
    GPIO.output(args.output_channel, GPIO.LOW)  # LED ON


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input-channel', type=int, default=11) # PIN 11/GPIO 0
    p.add_argument('--output-channel', type=int, default=18) # PIN 18/GPIO 5
    p.add_argument('--delay-time', type=int, default=500, help='delay time millisecond')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(args.input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(args.output_channel, GPIO.OUT, initial=GPIO.LOW)

    GPIO.add_event_detect(args.input_channel, GPIO.RISING, callback=process_signal, bouncetime=200)

    logging.info('waiting for input signal')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('keyboard interrupt')
    except:
        logging.info('error or exception occurred')
    finally:
        GPIO.cleanup()
