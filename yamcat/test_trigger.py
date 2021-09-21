from pyfirmata import Arduino, util
from time import sleep

board = Arduino('/dev/ttyACM0')
board.digital[9].write(0)

framerate = 60

# divide by two for high and low signal outputs
delay = (1 / framerate) / 2

HIGH = 1
LOW = 0

while True:
    board.digital[9].write(HIGH)
    sleep(delay)
    board.digital[9].write(LOW)
    sleep(delay)

