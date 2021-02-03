import numpy as np
import pyautogui
import time
import pytesseract

from PIL import ImageGrab, Image
from textblob import TextBlob

import settings

# Function to return area from screen
def readscreen(bbox, name = "tmp/tmp.png", correct = False):
	screen = ImageGrab.grab(bbox=settings.areas['initiallist'])
	img = screen.convert('L')
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
def drag(a, b, seconds = 1):
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
		drag(start, end, 0.2)

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
