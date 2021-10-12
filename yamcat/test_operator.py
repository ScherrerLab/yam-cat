from yamcat.core import Operator
from yamcat.utils import get_default_config
from yamcat.params import Params, CameraConfig

o = Operator()

cc1 = CameraConfig(
    guid='2676016BC31A',
    name='front',
    trigger_line=4,
    preview_position=(0, 0),
    preview_size=(1920/2, 1080/2)
)

cc2 = CameraConfig(
    guid='267601CA59E7',
    name='back',
    trigger_line=2,
    preview_position=(1920/2, 0),
    preview_size=(1920/2, 1080/2)
)

params = Params(
    arduino_address='/dev/ttyACM0',
    camera_configs=[cc1, cc2],
    duration=60,
    video_format='mp4v',
    framerate=76,
    width=1024,
    height=1024,
    parent_dir='/home/lab/test-yamcat-mouse',
    auto_create_subdirs=True,
    auto_create_subdirs_index=0,
    video_subdir='hot-3'
)

o.connect_arduino(params.arduino_address)
o.arduino_trigger.set_fps(80) # 84 will give ~76-77 fps on average

print(o.camera_guids)

o.params = params
o.prime()

o.arduino_trigger.start()
