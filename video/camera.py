import json
import os

from tqdm import tqdm
import time
import cv2

from common.consts import AVI_FILE_NAME, RECORDS_PATH
from common.log import debug
from common.process_sync import should_stop


class StandardVideoRecorder:
    def __init__(self):
        self._video_timestamps_file_path = None
        self._cap = None
        self._out = None
        self._ret = False
        self._frame = None
        self._frames = []
        self._timestamps = []
        self._output_file_path = None
        print(RECORDS_PATH)
        os.makedirs(RECORDS_PATH, exist_ok=True)
        self._output_file_path = os.path.join(RECORDS_PATH, AVI_FILE_NAME)

    def stop(self):
        for f in tqdm(self._frames, f'Saving video {self._output_file_path}'):
            self._out.write(f)
        self._cap.release()
        self._out.release()
        cv2.destroyAllWindows()

        json.dump(
            self._timestamps,
            open(self._video_timestamps_file_path, 'w')
        )

    def start(self):
        self._video_timestamps_file_path = os.path.join(RECORDS_PATH, 'video_timestamps.json')

        self._frames = []

        # cap = cv2.VideoCapture(1)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH , 320) # you should chose a value that the camera supports
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT , 240) # you should chose a value that the camera supports

        if not cap.isOpened():
            print("sad face")
        else:
            print("using 0")

        self._ret, self._frame = cap.read()
        print(self._ret, self._frame)
        # h, w = self._frame.shape[:2]
        h, w = (240, 320)

        fps = cap.get(cv2.CAP_PROP_FPS) // 3
        print(fps)
        self._cap = cap

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self._out = cv2.VideoWriter(self._output_file_path, fourcc, fps, (w, h))
        print(self._output_file_path)
        # self._out = cv2.VideoWriter(self._output_file_path, fourcc, 20.0, (int(cap.get(3)),int(cap.get(4))))


    def run(self):
        debug('Recording video')
        try:
            while True:
                if not self._ret:
                    debug('No more frames')
                    return True
                self._frames.append(self._frame)
                self._timestamps.append(time.time())
                self._ret, self._frame = self._cap.read()
                if should_stop():
                    raise KeyboardInterrupt()
        except KeyboardInterrupt:
            debug('Quitting video recording')


def video_capture():
    r = StandardVideoRecorder()
    r.start()
    r.run()
    r.stop()
