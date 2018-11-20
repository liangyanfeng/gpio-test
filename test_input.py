#coding:utf8
from __future__ import print_function
import sys
import logging
import argparse
import time

import RPi.GPIO as GPIO


logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)],
                    level=logging.INFO,
                    format='%(asctime)-15s [%(levelname)s] %(filename)s/%(funcName)s | %(message)s')


def process_signal(channel):
    logging.info('receive signal %d' % GPIO.input(channel)) 


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input-channel', type=int, default=11) # pin 11/GPIO 0
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(args.input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(args.input_channel, GPIO.BOTH, callback=process_signal, bouncetime=200)

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
