import cv2
import numpy as np
import mss
from pynput import mouse
from src.utils.read_config import config

class ScreenRecorder:
    def __init__(self, output_file, fps, monitor_index):
        self.output_file = output_file
        self.fps = fps
        self.monitor_index = monitor_index
        self.recording = False

        self.mouse_listener()
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[self.monitor_index]
        print(f"Recording monitor {self.monitor_index}: {self.monitor}")

        self.create_video_writer()

    def mouse_listener(self):
        self.mouse_pressed = False
        self.listener = mouse.Listener(
            on_click=self.on_click
        )
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        self.mouse_pressed = pressed  

    def create_video_writer(self):
        try:
            fourcc = cv2.VideoWriter_fourcc(*config.data.video.format)
            self.out = cv2.VideoWriter(
                self.output_file,
                fourcc,
                self.fps,
                (self.monitor["width"], self.monitor["height"])
            )
            if not self.out.isOpened():
                raise RuntimeError("VideoWriter failed to open")
        except Exception as e:
            print(f"Error creating video writer for monitor {self.monitor_index}: {e}")
            self.out = None

    def start_recording(self):
        if self.out is None:
            print("Recorder not initialized")
            return

        print(f"Recording monitor {self.monitor_index}... Press Ctrl+C to stop")
        self.recording = True

        try:
            while self.recording:
                img = self.sct.grab(self.monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

                if frame is not None:
                    self.show_cursor(frame=frame)

                self.out.write(frame)

        except KeyboardInterrupt:
            print(f"Stopped recording monitor {self.monitor_index} by user")
        finally:
            self.stop_recording()

    def show_cursor(self,frame):
        x, y = mouse.Controller().position
        x_relative = int(x - self.monitor["left"])
        y_relative = int(y - self.monitor["top"])

        color = (0, 0, 100) if self.mouse_pressed else (0, 100, 0)
        radius = 15 if self.mouse_pressed else 10
        full_circle = -1
        cv2.circle(frame, (x_relative, y_relative), radius, color, full_circle)

    def stop_recording(self):
        if not self.recording or self.out is None:
            return
        self.recording = False
        self.out.release()
        print(f"Saved video to {self.output_file}")
        self.listener.stop()



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
