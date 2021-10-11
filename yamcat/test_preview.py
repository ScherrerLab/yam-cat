from yamcat.core import Writer, VideoDisplayQThread
import skvideo.io
from multiprocessing import Queue
from tqdm import tqdm
from time import sleep

input_file = '/home/kushal/Videos/sync_vids/left.mp4'

print("Reading file")
vid = skvideo.io.vread(input_file)

camera_name = 'emulate'
queue = Queue()
output_path = '/home/kushal/Videos/sync_vids/test_emulate_out.mp4'
fps = 50
fourcc = 'mp4v'
dims = (1024, 1024)

queue_preview = Queue()

print("Creating processes")
writer = Writer(
    camera_name=camera_name,
    queue=queue,
    output_path=output_path,
    fps=fps,
    fourcc=fourcc,
    dims=dims,
    preview=False,
    queue_preview=queue_preview
)

preview = VideoDisplayQThread(
    camera_name=camera_name,
    queue=queue_preview,
    position=(0, 0),
    size=(1024, 1024)
)

preview.start()

writer.start()
# timer = QtCore.QTimer()
# timer.timeout.connect(preview.update_frame)
# timer.start(0)

for frame in tqdm(vid, total=vid.shape[0]):
    queue.put(frame)
    sleep(0.01)

