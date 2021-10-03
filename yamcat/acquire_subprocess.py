import sys
from multiprocessing import Process, Queue
from pypylon import pylon
import logging
from datetime import datetime
import click
from yamcat.core import Writer
from pprint import pprint
from time import sleep


def exception_hook(exc_type, exc_value, traceback):
    logging.error("EXCEPTION ENCOUNTERED", exc_info=(exc_type, exc_value, traceback))


@click.command()
@click.option('--device-guid', type=str)
@click.option('--camera-name', type=str)
@click.option('--fps', type=int)
@click.option('--duration', type=int)
@click.option('--trigger-line', type=int)
@click.option('--video-output-path', type=str)
@click.option('--fourcc', type=str)
@click.option('--dims', type=str)
def main(
        device_guid,
        camera_name,
        fps,
        duration,
        trigger_line,
        video_output_path,
        fourcc,
        dims
):
    pprint(locals())
    log_level = 'DEBUG'
    log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)s \n %(message)s "
    log_file = f'/home/lab/{datetime.now().strftime("acquire_%Y-%m-%d_%H.%M.%S-%f")}.ycl'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=log_file,
        filemode='w'
    )

    sys.excepthook = exception_hook

    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    # console.setFormatter(log_format)

    logger = logging.getLogger()

    # root_logger.addHandler(console)
    logger.addHandler(
        logging.StreamHandler(sys.stdout)
    )
    logger.addHandler(
        logging.StreamHandler(sys.stderr)
    )
    
    queue = Queue()

    dims = tuple(map(int, dims.split(',')))

    writer = Writer(
        camera_name=camera_name,
        queue=queue,
        output_path=video_output_path,
        fps=fps,
        fourcc=fourcc,
        dims=dims
    )
    writer.start()

    logger.info(f'Connecting to camera: {camera_name}')

    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()

    try:
        guids = [dev.GetDeviceGUID() for dev in devices]
    except ValueError:
        raise KeyError("Device GUID not found in connected devices")

    dev_ix = guids.index(device_guid)
    device = devices[dev_ix]

    # TODO: Have a way to choose the camera!!!
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(device))
    camera.Open()

    camera.Width.SetValue(dims[0])
    camera.Height.SetValue(dims[1])

    # number of frames to grab
    nframes_grab = fps * duration

    camera.MaxNumBuffer = 100

    camera.TriggerSelector.SetValue('FrameStart')
    camera.TriggerMode.SetValue('On')

    trigger_source = f'Line{trigger_line}'
    logging.info(trigger_source)
    camera.TriggerSource.SetValue(trigger_source)

    camera.TriggerActivation.SetValue('RisingEdge')

    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    logger.info(f'Camera ready: {camera_name}')

    camera.StartGrabbingMax(nframes_grab)
    logger.info("Grabbing started")

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(50000, pylon.TimeoutHandling_ThrowException)

        if not grabResult.GrabSucceeded():
            logger.info(f"{camera_name}: Couldn't grab frame\n{grabResult.ErrorDescription()}")
            return

        #logger.info("Getting image")
        image = converter.Convert(grabResult)
        frame = image.GetArray()

        queue.put(frame)

    queue.put(None)

    camera.Close()

    while writer.is_alive():
        print("Waiting for writer to finish...")
        sleep(1)
    

if __name__ == '__main__':
    main()
