from yamcat.core import Operator
from yamcat.utils import get_default_config
from yamcat.params import Params, CameraConfig

o = Operator()

cc_left = CameraConfig(
    guid='40120421',
    name='left',
    trigger_line=0,
)

cc_right = CameraConfig(
    guid='40120422',
    name='right',
    trigger_line=0,
)

cc_front = CameraConfig(
    guid='40120423',
    name='front',
    trigger_line=0,
)

cc_back = CameraConfig(
    guid='40120424',
    name='back',
    trigger_line=0,
)

params = Params(
    arduino_address='/dev/ttyACM0',
    camera_configs=[cc_left],#[cc_right, cc_left, cc_front, cc_back],
    duration=60,
    video_format='raw',
    framerate=60,
    width=1920,
    height=1080,
    destination_dir='/home/labuser/adrien-hotplate/day1-mouse-1',
)

o.connect_arduino(params.arduino_address)
o.arduino_trigger.set_fps(60) # 84 will give ~76-77 fps on average

print(o.camera_guids)

o.params = params
o.prime()

o.arduino_trigger.start()
