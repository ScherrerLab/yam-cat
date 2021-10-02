from pyfirmata import Arduino, util
from time import sleep
import click

@click.command()
@click.option('--address', type=str)
@click.option('--pin', type=int)
def main(address, pin):
    print("Connecting")
    board = Arduino(address)
    board.digital[pin].write(0)

    framerate = 50

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

