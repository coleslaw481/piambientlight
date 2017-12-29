#!/usr/bin/evn python

import io
import time
import threading
import picamera
import os
import math
from PIL import Image
from PIL import ImageDraw

# Create a pool of image processors
done = False
pval = 'na'
lock = threading.Lock()
pool = []
pixel_values_changed = False
camera_res = (640, 384)

overlay_img = Image.new('RGB', camera_res)
BOX_COLOR = (0,255,0)
BOX_WIDTH = 5

draw = ImageDraw.Draw(overlay_img)

pixels = []
# generate top and bottom pixel array
x_step = int(camera_res[0] / 6)
for x in xrange(10, camera_res[0] + x_step, x_step):
    if x > camera_res[0]:
        x = camera_res[0]-10
    pixels.append((x, 10))
    pixels.append((x, camera_res[1] - 10))
    
# generate left and right pixels
for y in xrange(60, 350, 50):
    pixels.append((10, y))
    pixels.append((630, y))

pixels_values = [(0,0,0)]*len(pixels)

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
        global pixel_values_changed
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                img = None
                try:
                    self.stream.seek(0)
                    # Read the image and do some processing on it
                    img = Image.open(self.stream)
                    pval = ''
                    i = 0
                    # this is a flawed approach to only change overlay
                    # if pixel intensities increase by more then 10 per color
                    # cause we updated the pixels_values each time so
                    # if color change is gradual enough the overlay
                    # will never be updated. Should change code to update
                    # previous values only if threshold is reached, course 
                    # that means a double iteration across the pixels...
                    pixel_values_changed = False
                    for p in pixels:
                       mypix = img.getpixel(p)
                       for gg in xrange(0,3):  
                         if int(math.fabs(mypix[gg]-pixels_values[i][gg])) > 10:
                             pixel_values_changed = True
                             break
                       
                       pixels_values[i] = mypix
                       draw.rectangle([p,(p[0]+BOX_WIDTH,p[1]+BOX_WIDTH)],fill=mypix)
                       i += 1
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
    over_lay = None
    while not done:
        with lock:
            if pool:
                camera.annotate_text = pval
                
                if pixel_values_changed:
                    if over_lay is not None:
                        camera.remove_overlay(over_lay)
                    over_lay = camera.add_overlay(overlay_img.tostring(), size=camera_res)
                    over_lay.alpha = 128
                    over_lay.layer = 3
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
        camera.resolution = camera_res
        camera.framerate = 1
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
