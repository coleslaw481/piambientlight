#!/usr/bin/evn python

import io
import time
import threading
import picamera
import os

from PIL import Image

# Create a pool of image processors
done = False
pval = 'na'
lock = threading.Lock()
pool = []

camera_res = (640, 360)

pixels = []
# generate top and bottom pixel array
for x in xrange(10, camera_res[0] - 10, int(camera_res[0] / 6)):
    pixels.append((x, 10))
    pixels.append((x, camera_res[1] - 10))

# generate left and right pixels
for y in xrange(60, 350, 50):
    pixels.append((10, y))
    pixels.append((630, y))


class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        global pval
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                img = None
                try:
                    self.stream.seek(0)
                    # Read the image and do some processing on it
                    img = Image.open(self.stream)
                    pval = ''
                    print '\n\n\n\n\n\n\n\n\n\n\n'
                    for p in pixels:
                        pval = str(p) + '=>' + str(img.getpixel(p))
                        print pval + ' '
                    if len(pval) > 255:
                        pval = pval[0:254]

                    # print('160x120 = ' + str(img.getpixel((160,120))) + '\n')
                    if os.path.isfile('exit'):
                        print('exit file detected\n')
                        done = True
                except Exception as e:
                    print('caught exception: ' + str(e) + '\n')
                    done = True
                finally:
                    if img is not None:
                        img.close()

                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)


def streams(camera):
    while not done:
        with lock:
            if pool:
                camera.annotate_text = pval
                processor = pool.pop()
            else:
                processor = None

        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)


with picamera.PiCamera() as camera:
    try:
        pool = [ImageProcessor() for i in range(4)]
        camera.resolution = (640, 360)
        camera.framerate = 30
        camera.start_preview()
        time.sleep(2)
        camera.capture_sequence(streams(camera), use_video_port=True)
    finally:
        camera.stop_preview()

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
