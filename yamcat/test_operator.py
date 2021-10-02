from yamcat.core import Operator
from yamcat.utils import get_default_config
from yamcat.params import Params, CameraConfig

o = Operator()

cc1 = CameraConfig(
    guid=o.camera_guids[0],
    name='c0',
    trigger_line=1,
)

cc2 = CameraConfig(
    guid=o.camera_guids[1],
    name='c1',
    trigger_line=1,
)

params = Params(
    arduino_address='/dev/ttyACM0',
    camera_configs=[cc1, cc2],
    duration=10,
    video_format='mp4v',
    framerate=50,
    width=1024,
    height=1024,
    parent_dir='/home/lab/test-yamcat',
    auto_create_subdirs=True,
    auto_create_subdirs_index=0,
    video_subdir='bah'
)

o.connect_arduino(params.arduino_address)
o.arduino_trigger.set_fps(50)

print(o.camera_guids)

o.params = params
o.prime()

o.arduino_trigger.start()