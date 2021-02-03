import pytesseract
import time
import os

import settings, utils, scrape

# I didn't put my tesseract in my PATH properly, too lazy to fix :)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# See if we have to unfold user list (> 5 users)
scrape.expandLists()

# Align screen to the first user item
print("Aligning for first user...")
scrolled = utils.scrollForPixel(
	settings.colors['line'],
	(
		settings.areas['screen'][2],
		settings.areas['screen'][1] + settings.settings['topbar'] + 2
	),
	afterscroll=5,
	safety=50
)
if scrolled:
	print("Aligned!")
else:
	print("Could not find alignment, aborting.")
	exit(1)

# Tests I want to save untill I am ready to use them
exit()

# Runtimeeeee!
raw = scrape.scrapeEntries()

# Save raw if wanted
if settings.settings['savescrapes']:
	with open('tmp/scrape_{}.txt'.format(int(time.time())), 'a') as f:
		for line in raw:
			line = line.strip()
			if len(line) > 0:
				f.write("{}\n".format(line))

# Countdown and move spoofed GPS to coords
for i in range(3, 0, -1):
	print("{}...".format(i))
	time.sleep(1)

for coord in settings.coords:
	utils.setGeo(coord)
	time.sleep(1)
