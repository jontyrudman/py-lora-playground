#!/usr/bin/env python3
"""RAK811 P2P demo.

Send counter messages at random interval and listen the rest of the time.

Start this script on 2 or more nodes an observe the packets flowing.

Copyright 2019 Philippe Vanhaesendonck

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0

Changes made by Jonathan Rudman. Compare with original repository:
https://github.com/AmedeeBulle/pyrak811
"""

from random import randint
from sys import exit
from time import time
import logging
import logging.handlers

from rak811 import Mode, Rak811

# Send packet every P2P_BASE + (0..P2P_RANDOM) seconds
P2P_BASE = 30
P2P_RANDOM = 60

# Magic key to recognize our messages
P2P_MAGIC = b'\xca\xfe'


def get_logger():
    logger = logging.getLogger("logs")
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logFilePath = "log"
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=logFilePath, when='midnight', backupCount=30)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = get_logger()

def main():
    logger.debug('Starting a new session using magic string {} (hex).'.format(P2P_MAGIC.hex()))
    logger.info('Entering send/receive loop.')
    loop()
    logger.info('All done')


def receive(lora):
    # Calculate next message send timestamp
    next_send = time() + P2P_BASE + randint(0, P2P_RANDOM)
    # Set module in receive mode
    lora.rxc()
    # Loop until we reach the next send time
    # Don't enter loop for small wait times (<1 1 sec.)
    while (time() + 1) < next_send:
        wait_time = next_send - time()
        logger.info('Waiting on message for {:0.0f} seconds'.format(wait_time))
        # Note that you don't have to listen actively for capturing message
        # Once in receive mode, the library will capure all messages sent.
        lora.rx_get(wait_time)
        while lora.nb_downlinks > 0:
            message = lora.get_downlink()
            data = message['data']
            if data[:len(P2P_MAGIC)] == P2P_MAGIC:
                logger.info(
                    'Received message: {}'.format(
                        int.from_bytes(data[len(P2P_MAGIC):],
                                       byteorder='big')
                    )
                )
                logger.debug('RSSI: {}, SNR: {}'.format(message['rssi'],
                                                 message['snr']))
            else:
                logger.info('Foreign message received: {} (bytes)'.format(data))
    # Exit receive mode
    lora.rx_stop()


def send(lora, counter):
    logger.info('Sending message {}'.format(counter))
    hex_bytes = P2P_MAGIC + bytes.fromhex('{:08x}'.format(counter))
    lora.txc(hex_bytes)


def loop():
    counter = 0
    with Rak811() as lora:
        while True:
            receive(lora)
            counter += 1
            send(lora, counter)

if __name__ == '__main__':
    main()
