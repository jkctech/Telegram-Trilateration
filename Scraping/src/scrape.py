import os
import re
import time
import datetime

import utils, settings

# Function to unfold the "Show More" list on the screen.
def expandLists():
	print("Searching for \"Show More\" entry in list...")

	# Read screen
	data = utils.readscreen(settings.areas['listport'], export=True)

	# Remove empty lines
	data = os.linesep.join([s for s in data.splitlines() if s])

	# Split into list elements
	items = data.splitlines()

	# Print read data for debug
	if settings.settings['printdebug']:
		print("=== DATA ===")
		print(items)
		print("=== END DATA ===")

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
		x = int(settings.areas['listport'][0] + 20)
		y = int(settings.areas['listport'][1] + (5 * settings.settings['itemheight']) + (settings.settings['itemheight'] / 2))

		# Click
		utils.click((x, y))
		print("Clicked \"Show More\" at ({}, {})".format(x, y))
	else:
		print("Found nothing, proceeding...")\

# Function to scrape all entries
def scrapeEntries():
	# Start and note time
	starttime = time.time()
	print("Starting scraper at [{}] ({} Per page)".format(datetime.datetime.now().strftime("%H:%M:%S"), settings.settings['usersonscreen']))
	print("Indexing users...")

	total = [[], []]
	index = 0
	cnt = 1
	stop = False

	while (True):
		# We will keep track of pages
		print("Page {}...".format(cnt))

		# Read screen
		data = utils.readscreen(settings.areas['listport'], "tmp/tmp_{}.png".format(cnt))

		# Remove empty lines
		data = os.linesep.join([s for s in data.splitlines() if s])

		# Split into list elements
		data = data.splitlines()

		# Print read data for debug
		if settings.settings['printdebug']:
			print("=== DATA ===")
			print(data)
			print("=== END DATA ===")

		# Append users to total
		i = 0
		while i < len(data):
			# Check if we found group marker
			if (index == 0 and data[i] == "Create a Local Group"):
				index = 1
				i += 1
				continue

			# We have a valid combination
			if i + 1 < len(data) and utils.isdistance(data[i]) == False and utils.isdistance(data[i + 1]) == True:
				# Debugging
				if settings.settings['printdebug']:
					print("Found {} @ {}".format(data[i], data[i + 1]))
				
				# Tuple to add to the list
				tup = (data[i], utils.getdistance(data[i + 1]))

				# Append to correct group and stop if we have a double
				if (index == 0 and tup not in total[0]) or (index == 1 and tup not in total[0] and tup not in total[1]):
					total[index].append(tup)
				else:
					# Mark that we want to stop after this page
					stop = True
				
				# We used both the name and distance so count up by 2
				i += 2
			else:
				# We skipped, so just go to the next item
				i += 1
		
		# If we detected a double, stop the loop
		if stop:
			break

		# Scroll x users down
		utils.scrollUsers(settings.settings['usersonscreen'])

		# Fix scroll drifting
		if settings.settings['fixscrolldrift']:
			utils.scroll(settings.settings['itemheight'] / 2)
			print("Compensating for drift...")
			scrolled = utils.scrollForPixel(
				settings.colors['line'],
				(
					settings.areas['screen'][2],
					settings.areas['screen'][1] + settings.settings['topbar'] + 2
				),
				afterscroll=5,
				safety=5
			)
			if scrolled:
				print("Aligned!")
			else:
				print("Could not find alignment, assuming ending.")

		# Give a second to level out
		time.sleep(1)

		# Increase iteration counter
		cnt += 1

	# Complete!
	print("Scraping complete!")

	# Stats
	print("Time elapsed: {}".format(str(datetime.timedelta(seconds=int(time.time() - starttime)))))
	print("Found entries: {}".format(len(total[0]) + len(total[1])))

	# Print
	print("===")
	print("Users: ({})".format(len(total[0])))
	for line in total[0]:
		print(line)
	print("\nGroups: ({})".format(len(total[1])))
	for line in total[1]:
		print(line)
	print("===")
	
	# Return result
	return total
