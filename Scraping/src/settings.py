# Area defenitions
areas = {}
areas['list'] = (70, 393, 550, 975)

# Screen Location definitions
locations = {}
locations['latlon'] = (1050, 105) # Location of the 'Lat' field in the NOX GPS Window
locations['move'] = (1160, 600) # Location of the 'Move Here' button

# Location coordinates for scanning
coords = {
	(52.929502, 4.8012571),
	(52.965476, 4.7217422),
	(52.929502, 4.7217422),
	(52.965476, 4.8012571),
	(52.940832, 4.7577242)
}

# Settings
settings = {}

# Prints some more info on the screen
settings['printdebug'] = False

# Amount of seconds to wait between certain mouse / keyboard events
settings['actionwait'] = 0.15

# Height of a single element in the Telegram overview
settings['itemheight'] = 66

# Top-left pixel of the dividing line of the first item in the overview list.
settings['firstpixel'] = (74, 393)

# Amount of pixels mouse needs to move before NOX sees it as a "drag"
settings['dragbleed'] = 7

# Amount of users we should attempt to scroll if we detected more users.
settings['scrollusers'] = 5

# Amount of users who are COMPLETELY visible on screen at a single time
# (While unfolded and scrolled to the very top)
settings['usersonscreen'] = 9
