from PIL import ImageGrab
import time

start = time.time()
image = ImageGrab.grab(bbox=(0,0,100,100))

for y in range(0, 100):
	for x in range(0, 100):
		print(image.getpixel((x, y)))

print(time.time() - start)