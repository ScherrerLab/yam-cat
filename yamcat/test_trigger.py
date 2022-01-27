from pyfirmata import Arduino, util
from time import sleep
import click


"""
Usage:

python test_trigger --address /dev/ttyACM0 --pin 9 --fps 50
"""

@click.command()
@click.option('--address', type=str)
@click.option('--pin', type=int)
@click.option('--fps', type=float)
def main(address, pin, fps):
    print("Connecting")
    board = Arduino(address)
    board.digital[pin].write(0)

    framerate = fps

    # divide by two for high and low signal outputs
    delay = (1 / framerate) / 2

    HIGH = 1
    LOW = 0

    print("Starting trigger")
    while True:
        board.digital[pin].write(HIGH)
        sleep(delay)
        board.digital[pin].write(LOW)
        sleep(delay)

if __name__ == '__main__':
    main()

