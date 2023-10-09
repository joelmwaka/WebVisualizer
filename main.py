import cv2
import time
from threading import Thread
from webvisualizer.webvisualizer import app, send_frame


def main():

    thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread.start()
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while True:

        _, frame = cap.read()
        send_frame(frame)

        if time.time() - start_time > 60:
            break
    
    cap.release()


if __name__ == "__main__":
    main()