from yamcat.core import Operator
from yamcat.utils import get_default_config
from yamcat.params import Params, CameraConfig

o = Operator()

cc1 = CameraConfig(
    guid='40120421',
    name='front',
    trigger_line=0,
    preview_position=(0, 0),
    preview_size=(1920/2, 1080/2)
)

cc2 = CameraConfig(
    guid='40120422',
    name='back',
    trigger_line=0,
    preview_position=(1920/2, 0),
    preview_size=(1920/2, 1080/2)
)

params = Params(
    arduino_address='/dev/ttyACM0',
    camera_configs=[cc1, cc2],
    duration=60,
    video_format='mp4v',
    framerate=60,
    width=2048,
    height=1536,
    destination_dir='/home/labuser/test-yamcat-mouse/bah',
)

o.connect_arduino(params.arduino_address)
o.arduino_trigger.set_fps(60) # 84 will give ~76-77 fps on average

print(o.camera_guids)

o.params = params
o.prime()

o.arduino_trigger.start()
