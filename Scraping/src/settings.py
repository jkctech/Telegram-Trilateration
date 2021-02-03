# Area defenitions
areas = {}
areas['screen'] = (545, 32, 1093, 1007)
areas['initiallist'] = (612, 387, 1093, 1007)


# Clickable screen points
points = {}
points['latlon'] = (1050, 105) # Location of the 'Lat' field in the NOX GPS Window
points['move'] = (1160, 600) # Location of the 'Move Here' button


# Location coordinates for scanning
coords = {
	(52.929502, 4.8012571),
	(52.965476, 4.7217422),
	(52.929502, 4.7217422),
	(52.965476, 4.8012571),
	(52.940832, 4.7577242)
}


# Color codes (RGB) for certain pixels.
# Used for alignment of the screen.
colors = {}

# Division line between users
colors['line'] = (236, 236, 236)

# Background color
colors['background'] = (240, 240, 240)

# Just for reference
colors['white'] = (255, 255, 255)

# Blue text Telegram uses
colors['text'] = (30, 136, 211)


# Settings
settings = {}

# Prints some more info on the screen
settings['printdebug'] = False

# Save raw scrapes in txt files
settings['savescrapes'] = True

# Amount of seconds to wait between certain mouse / keyboard events
settings['actionwait'] = 0.15

# Height of a single element in the Telegram overview
settings['itemheight'] = 65

# Amount of pixels mouse needs to move before NOX sees it as a "drag"
settings['dragbleed'] = 8

# Size of the android navbar + the topbar inside Telegram. (24 + 57)
settings['topbar'] = 81

# Amount of users who are COMPLETELY visible on screen at a single time
# (While unfolded and scrolled to the very top)
settings['usersonscreen'] = 9


# Calculations done using the settings themselves

# Viewport area on the screen
# Basically same as areas['screen'] but added the topbar
areas['viewport'] = (
	areas['screen'][0],
	areas['screen'][1] + settings['topbar'],
	areas['screen'][2],
	areas['screen'][3],
)
