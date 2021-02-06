import pytesseract
import time
import os
import pyautogui

import settings, utils, scrape

try:
	# Focus and maximize the NOX window
	# Somewhat buggy since NOX does not use native Windows forms
	utils.focusnox()
	time.sleep(1)
	utils.click(settings.points['focus'])

	# Confirm we are on the right screen
	print("Checking if we are on the \"Nearby\" screen...")
	if utils.confirmpixels(settings.pixelgroups['nearby']) == False:
		print("Not on correct screen inside Nox... Aborting!")
		exit(1)
	else:
		print("Seems OK, proceeding...")

	# I didn't put my tesseract in my PATH properly, too lazy to fix :)
	# If you one of those people as well, feel free to use this in from your config
	if len(settings.settings['tesseract']) > 0:
		pytesseract.pytesseract.tesseract_cmd = settings.settings['tesseract']

	# Align screen for start
	utils.firstalign()

	# See if we have to unfold user list (> 5 users) and settle out
	scrape.expandLists()
	time.sleep(1)

	# Runtimeeeee!
	raw = scrape.scrapeEntries()

	# Save raw if wanted
	if settings.settings['savescrapes']:
		with open('tmp/scrape_{}.txt'.format(int(time.time())), 'a') as f:
			for line in raw:
				f.write("{}\n".format(line))

# Using the PyAutoGUI failsafe
except pyautogui.FailSafeException:
	print("FAILSAFE TRIGGERED, ABORTING!")
	exit(2)

# Using the PyAutoGUI failsafe
except KeyboardInterrupt:
	print("User interrupt, aborting!")
	exit(1)

# Tests I want to save untill I am ready to use them
exit()

# Countdown and move spoofed GPS to coords
for i in range(3, 0, -1):
	print("{}...".format(i))
	time.sleep(1)

for k in settings.coords.keys():
	utils.setGeo(settings.coords[k])
	time.sleep(1)