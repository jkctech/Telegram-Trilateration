import numpy as np
import pyautogui
import time
import pytesseract
import re

from PIL import ImageGrab, Image
from textblob import TextBlob

import settings

# Function to return area from screen
def readscreen(bbox, name = "tmp/DEBUG_screen.png", correct = False, export = False):
	screen = ImageGrab.grab(bbox=bbox)
	img = screen.convert('L')
	if export:
		img.save(name)
	text = pytesseract.image_to_string(img)
	if correct:
		text = TextBlob(text).correct()
	return text

# Move mouse to location
def move(pos):
	pyautogui.moveTo(pos[0], pos[1])

# Click left mouse btn at position
def click(pos):
    pyautogui.click(pos[0], pos[1])

# Drag from point a to point b
def drag(a, b, seconds = 0):
	move(a)
	pyautogui.mouseDown()
	time.sleep(settings.settings['actionwait'])
	pyautogui.moveTo(b[0], b[1], seconds)
	pyautogui.mouseUp()

# Write a string emulating the keyboard
def write(text):
	pyautogui.write(text)

# Wipe a current field (CTRL + A | Del)
def wipe():
	pyautogui.keyDown('ctrl')
	pyautogui.press('a')
	pyautogui.keyUp('ctrl')
	time.sleep(settings.settings['actionwait'])
	pyautogui.press('delete')

# Execute a GPS move
def setGeo(coords):
	# Latitude
	click(settings.points['latlon'])
	time.sleep(settings.settings['actionwait'])
	wipe()
	write(str(coords[0]))

	time.sleep(settings.settings['actionwait'])

	# Longitude
	pyautogui.press('tab')
	time.sleep(settings.settings['actionwait'])
	wipe()
	write(str(coords[1]))

	time.sleep(settings.settings['actionwait'])

	# <Enter>
	pyautogui.press('enter')

	time.sleep(settings.settings['actionwait'])

	# Actually move GPS
	click(settings.points['move'])

def scroll(distance):
	# Move to center of clickable screen (Listport)
	x = settings.areas['listport'][0] + (settings.areas['listport'][2] - settings.areas['listport'][0]) / 2
	start = [x, 0]

	if distance < 0:
		# If below 0, we want to scroll DOWN
		start[1] = settings.areas['listport'][3] - 10
		end = (start[0], start[1] + distance - settings.settings['dragbleed'])
	elif distance > 0:
		# If above 0, we want to scroll UP
		start[1] = settings.areas['listport'][1] + 10
		end = (start[0], start[1] + distance + settings.settings['dragbleed'])
	else:
		return

	drag(tuple(start), end)

# Function to scroll 1 user entry further
# We do it the dirty way to make sure we never leave the screen by picking the center of the list area.
def scrollUsers(count):
	start = (
		settings.areas['initiallist'][0] + (settings.areas['initiallist'][2] - settings.areas['initiallist'][0]) / 2,
		settings.areas['initiallist'][1] + (settings.areas['initiallist'][3] - settings.areas['initiallist'][1]) / 2,
	)
	
	# Same coords but some pixels up of course (By decreasing the Y coord)
	end = (start[0], start[1] - (settings.settings['itemheight'] + settings.settings['dragbleed']))
	
	# Loop wanted amount of times
	for i in range(count):
		drag(start, end)

# Scroll for a certain pixel color to be on the top pixel of that area
def scrollForPixel(targetcolor, targetlocation, stepsize = 20, afterscroll = 0, safety = -1):
	step = 0
	offset = -1

	# Move just above middle bottom pixel of screen to start drag.
	start = (
		settings.areas['initiallist'][0] + (settings.areas['initiallist'][2] - settings.areas['initiallist'][0]) / 2,
		settings.areas['initiallist'][3] - 10,
	)
	move(start)

	# Mouse down
	pyautogui.mouseDown()

	# Loop only x times to prevent infinite loop
	while (step < safety or safety == -1):
		if (offset == -1):
			# Scroll by defined amount
			pyautogui.moveTo(start[0], start[1] - (step * stepsize))
		else:
			# If we found pixel in screengrab, move to that pixel
			pyautogui.moveTo(start[0], start[1] - ((step - 1) * stepsize) - offset - afterscroll)
			
			# Release mouse
			pyautogui.mouseUp()
			return True
		
		# Grab screen
		image = ImageGrab.grab(bbox=(
			targetlocation[0],
			targetlocation[1],
			targetlocation[0] + 1,
			targetlocation[1] + stepsize,
		))

		# Save for debugging
		#image.save("tmp/DEBUG_scroll_{}.png".format(step))
		
		# Find pixel in screengrab
		for y in range(0, stepsize):
			pixel = image.getpixel((0, y))
			if (pixel == targetcolor):
				offset = y
		
		# Increment stepper
		step += 1
	
	# Release mouse and close
	pyautogui.mouseUp()
	return False

def isdistance(input):
	res = re.match(r"\d+\.?\d*\s?k?m\s?away", input) != None
	if settings.settings['printdebug']:
		print("Checking if '{}' is a distance: [{}]".format(input, ("True" if res else "False")))
	return (res)

def getdistance(input):
	# Cleanup
	input = input.strip()

	# Only first part is important
	distance = input.split(' ')[0]

	# If we have a dot in the remainder, the data is in km, else in m
	if '.' in distance:
		tmp = distance.split('.')
		a = int(re.sub('[^0-9]','', tmp[0]))
		b = int(re.sub('[^0-9]','', tmp[1]))
		distance = (a * 1000) + (b * 10)
	else:
		distance = int(re.sub('[^0-9]','', distance))
	
	return (distance)
