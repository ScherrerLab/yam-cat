from pyfirmata import Arduino, util
from time import sleep

print("Connecting")
board = Arduino('/dev/ttyACM1')
board.digital[9].write(0)

framerate = 50

# divide by two for high and low signal outputs
delay = (1 / framerate) / 2

HIGH = 1
LOW = 0

print("Starting trigger")
while True:
    board.digital[9].write(HIGH)
    sleep(delay)
    board.digital[9].write(LOW)
    sleep(delay)

