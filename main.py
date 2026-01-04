import cv2
import numpy as np
import mss
from src.utils.read_config import config

class ScreenRecorder:
    def __init__(self, output_file, fps, monitor_index):
        self.output_file = output_file
        self.fps = fps
        self.monitor_index = monitor_index
        self.recording = False
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[self.monitor_index]
        print(f"Recording monitor {self.monitor_index}: {self.monitor}")

        self.create_video_writer()

    def create_video_writer(self):
        try:
            fourcc = cv2.VideoWriter_fourcc(*config.data.video.format)
            self.out = cv2.VideoWriter(
                self.output_file,
                fourcc,
                self.fps,
                (self.monitor["width"], self.monitor["height"])
            )
        except Exception as e:
            print(f"Error creating video writer for monitor {self.monitor_index}: {e}")

    def start_recording(self):
        print(f"Recording monitor {self.monitor_index}... Press Ctrl+C to stop")
        self.recording = True
        try:
            while self.recording:
                img = self.sct.grab(self.monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                self.out.write(frame)
        except KeyboardInterrupt:
            print(f"Stopped recording monitor {self.monitor_index} by user")
        finally:
            self.stop_recording()

    def stop_recording(self)-> None:
        try:
            if not self.recording:
                return
            
            self.recording = False
            self.out.release()
            print(f"Saved video to {self.output_file}")
        except Exception as e:
            print(f"Error stopping recorder for monitor {self.monitor_index}: {e}")


if __name__ == "__main__":

    recorders = []
    for i in range(1, len(mss.mss().monitors)):
        filename = f"screen_monitor_{i}.mp4"
        recorder = ScreenRecorder(output_file=filename, fps=config.data.fps, monitor_index=i)
        recorders.append(recorder)

    try:
        for recorder in recorders:
            recorder.start_recording()
    except KeyboardInterrupt:
        print("Stopped all recordings")
        for recorder in recorders:
            recorder.stop_recording()
    except Exception as e:
        print(f"An error occurred: {e}")
        for recorder in recorders:
            recorder.stop_recording()
