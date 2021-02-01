import pytesseract
import time

import settings, utils, scrape

# I didn't put my tesseract in my PATH properly, too lazy to fix :)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Runtimeeeee!
scrape.expandLists()

# Tests I want to save untill I am ready to use them
exit()

# Scroll 1 user item down
utils.drag((350, 450), (350, 450 - (settings.settings['itemheight'] +  settings.settings['dragbleed'])))

# Countdown and move spoofed GPS to coords
for i in range(3, 0, -1):
	print("{}...".format(i))
	time.sleep(1)

for coord in settings.coords:
	utils.setGeo(coord)
	time.sleep(1)
