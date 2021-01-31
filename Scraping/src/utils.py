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
	click(settings.locations['lat'])
	time.sleep(settings.settings['actionwait'])
	wipe()
	write(str(coords[0]))

	time.sleep(settings.settings['actionwait'])

	# Longitude
	click(settings.locations['lon'])
	time.sleep(settings.settings['actionwait'])
	wipe()
	write(str(coords[1]))

	time.sleep(settings.settings['actionwait'])

	# <Enter>
	pyautogui.press('enter')

	time.sleep(settings.settings['actionwait'])

	# Actually move GPS
	click(settings.locations['move'])
