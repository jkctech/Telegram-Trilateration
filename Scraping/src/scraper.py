import pytesseract
import time
import os
import pyautogui

from utils import settings, functions, scrape, exporter

import datetime

# Flags (And defaults)
f_export = "xlsx"

try:
	# Focus and maximize the NOX window
	# Somewhat buggy since NOX does not use native Windows forms
	if functions.focusnox() == False:
		print("Could not detect Nox... Aborting!")
		exit(1)
	time.sleep(1)
	functions.click(settings.points['focus'])

	# Confirm we are on the right screen
	print("Checking if we are on the \"Nearby\" screen...")
	if functions.confirmpixels(settings.pixelgroups['nearby']) == False:
		print("Not on correct screen inside Nox... Aborting!")
		exit(1)
	else:
		print("Seems OK, proceeding...")

	# Extract current coordinates
	print("Looking for current GPS coordinates...")
	coords = functions.getGPSCoords()
	if coords == False:
		print("Could not extract GPS location... Aborting!")
		exit(1)
	else:
		print("Found location: {}".format(coords))
		time.sleep(1)
	
	# Close GPS window
	functions.click(settings.points['close'])
	time.sleep(2)

	# I didn't put my tesseract in my PATH properly, too lazy to fix :)
	# If you one of those people as well, feel free to use this in from your config
	if len(settings.settings['tesseract']) > 0:
		pytesseract.pytesseract.tesseract_cmd = settings.settings['tesseract']

	# Align screen for start
	functions.firstalign()

	# See if we have to unfold user list (> 5 users) and settle out
	scrape.expandLists()
	time.sleep(1)

	# Runtimeeeee!
	raw = scrape.scrapeEntries()

	# Export
	# Should actually make this into a proper jumptable but whatever
	filename = "results/result_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

	# XLSX
	if f_export == "xlsx":
		filename += ".xlsx"
		exporter.exportDistancesXLSX(raw, coords, filename=filename)
	
	# JSON
	elif f_export == "json":
		filename += ".json"
		exporter.exportDistancesJSON(raw, coords, filename=filename)

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
	functions.setGeo(settings.coords[k])
	time.sleep(1)
