import pytesseract
import time

import utils, settings

# I didn't put my tesseract in my PATH properly, too lazy to fix :)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


print(utils.readscreen(settings.areas['list']))


exit()
# Countdown
for i in range(3, 0, -1):
	print("{}...".format(i))
	time.sleep(1)

# Move to locations
for coord in settings.coords:
	utils.setGeo(coord)
	time.sleep(1)
