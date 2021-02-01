import numpy as np
import pyautogui
import time
import pytesseract

from PIL import ImageGrab, Image
from textblob import TextBlob

import settings

# Function to return area from screen
def readscreen(bbox, name = "tmp/tmp.png", correct = False):
	screen = ImageGrab.grab(bbox=settings.areas['list'])
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
	click(settings.locations['latlon'])
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
	click(settings.locations['move'])

# Function to scroll 1 user entry further
# We do it the dirty way to make sure we never leave the screen by picking the center of the list area.
def scrollUsers(count):
	start = (
		settings.areas['list'][0] + (settings.areas['list'][2] - settings.areas['list'][0]) / 2,
		settings.areas['list'][1] + (settings.areas['list'][3] - settings.areas['list'][1]) / 2,
	)
	
	# Same coords but some pixels up of course (By decreasing the Y coord)
	end = (start[0], start[1] -settings.settings['itemheight'] + settings.settings['dragbleed'])
	
	# Loop wanted amount of times
	for i in range(count):
		drag(start, end, 0.5)
