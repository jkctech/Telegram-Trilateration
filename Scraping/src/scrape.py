import os
import re
import time

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

# Function to scrape all entries
def scrapeEntries():
	print("Starting scraper...")

	total = []
	cnt = 1

	while (True):
		# We will keep track of iterations
		print("Iteration {}...".format(cnt))

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
		data = data.splitlines()

		# Check to see if we are at the end
		if len(total) >= 2 and len(data) >= 2 and data[-1] == total[-1] and data[-2] == total[-2]:
			break
		
		# Append current list to total
		total += data

		if cnt == 3:
			break

		# Scroll x users down
		utils.scrollUsers(settings.settings['usersonscreen'])

		# Five a second to level out
		time.sleep(1)

		# Increase iteration counter
		cnt += 1

	# Complete!
	print("Scraping complete!")

	# Print
	print("===")
	for line in total:
		print(line)
	print("===")
	
	# Return result
	return total
