#coding:utf8
from __future__ import print_function
import sys
import logging
import thread
import time
import json
from datetime import datetime
import argparse

import websocket


logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)],
                    level=logging.INFO,
                    format='%(asctime)-15s [%(levelname)s] %(filename)s/%(funcName)s | %(message)s')


def on_message(ws, message):
    logging.info('receive message:' + message)


def on_error(ws, error):
    logging.error('websocket error:' + error)


def on_close(ws):
    logging.warn('websocket close')


def on_open(ws):
    logging.info('websocket connect success')
    def run(*args):
        while 1:
            ws.send(get_heartbeat_msg())
            time.sleep(1)
    thread.start_new_thread(run, ())


def get_heartbeat_msg():
    return json.dumps({
        "type": "/lift/heartbeat/req",
        "id": "cefede8a-1872-467b-b9f4-1bcc1b77b714",
        "t": datetime.now().strftime('%Y%m%d%H%M%S'),
        "partner_id": "aaa",
        "lift_id": "31da2h",
        "sign": "a0da1e00-cdd1-11e8-90bc-6c96cfe06435",
        "data": {}
    })


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--websocket-url', type=str, default='ws://localhost:8080/connect')
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(args.websocket_url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
