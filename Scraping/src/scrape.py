import os
import re

import utils, settings

# Function to unfold the "Show More" list on the screen.
def expandLists():
	print("Searching for \"Show More\" entry in list...")

	# Read screen
	data = utils.readscreen(settings.areas['list'])

	# Print read data for debug
	if settings.settings['printdebug']:
		print("=== DATA ===")
		print(data)
		print("=== END DATA ===")

	# Remove empty lines
	data = os.linesep.join([s for s in data.splitlines() if s])

	# Split into list elements
	items = data.splitlines()

	# Method to find "show more" dynamically
	# pos = -1 
	# for i in range(len(items)):
	# 	# Matching it not very accurately since sometimes the OCR engine fucks up
	# 	# In the case tha a user is actually called "Show More (69)" this will break
	# 	if re.match(r"Show\s?More\s?\(.*\)", items[i]):
	# 		if settings.settings['printdebug']:
	# 			print("Found \"Show more\" at {}!".format(i))
	# 		pos = i
	# 		break

	# Click if needed
	# if pos != -1:

	# Find "show more" which should be the 6th item in the list
	# This means 5 items will preceed it, and thus should be at index 10
	if re.match(r"Show\s?More\s?\(.*\)", items[10]):
		print("Found \"Show More\" entry!")

		# Find coords to click
		# Ideally I should use bounding boxes of the text and stuff but for now, this will suffice
		x = int(settings.areas['list'][0] + 20)
		y = int(settings.areas['list'][1] + (5 * settings.settings['itemheight']) + (settings.settings['itemheight'] / 2))

		# Click
		utils.click((x, y))
		print("Clicked \"Show More\" at ({}, {})".format(x, y))
	else:
		print("Found nothing, proceeding...")\
