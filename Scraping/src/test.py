import pytesseract
import time
import os

import settings, utils, scrape

# I didn't put my tesseract in my PATH properly, too lazy to fix :)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Runtimeeeee!
scrape.expandLists()
raw = scrape.scrapeEntries()

# Save raw if wanted
if settings.settings['savescrapes']:
	with open('tmp/scrape_{}.txt'.format(time.time() / 1000), 'a') as f:
		for line in raw:
			line = line.strip()
			if len(line) > 0:
				f.write("{}\n".format(line))

# Tests I want to save untill I am ready to use them
exit()

# Countdown and move spoofed GPS to coords
for i in range(3, 0, -1):
	print("{}...".format(i))
	time.sleep(1)

for coord in settings.coords:
	utils.setGeo(coord)
	time.sleep(1)
