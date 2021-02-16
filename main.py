import config
import logging, sys
import queue
from arduino import Arduino
from keyboard import KeyMonitor
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

config.run = True

arduino_q = queue.Queue(maxsize=0)
arduino_thread = Arduino(args = (arduino_q), baudrate = config.serial_baudrate, port = config.serial_port)

keyboard_q = queue.Queue(maxsize=0)
keyboard_thread = KeyMonitor(args = (keyboard_q))

arduino_thread.start()
keyboard_thread.start()

now = time.time()

while True:
    if time.time() - now > config.length:
        config.run = False
        time.sleep(1)
        logging.debug("Experiment is over, closing threads. Press Enter to exit.")
        sys.exit(1)
    if (keyboard_q.qsize() > 0):
        input_str = keyboard_q.get()
        if (input_str == "q"):
            config.run = False
            time.sleep(1)
            logging.debug("Experiment is over, closing threads. Press Enter to exit.")
            sys.exit(1)
        elif (input_str == "a"):
            logging.info(arduino_q.get())
        else:
            logging.debug("Unknown keyboard entry.")