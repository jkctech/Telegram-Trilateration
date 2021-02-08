# Area defenitions
areas = {}

# Bounding box of the NOX touchscreen.
# Some libraries in this project don't like multi-monitor setups,
# so please leave the main window at your primary screen.
areas['screen'] = (545, 32, 1093, 1007)

# The "You are here" text in the GPS window (RELATIVE)
areas['gpsreadback'] = (8, 584, 356, 619) 


# Pixelgroups
# Used to confirm correct screens
# Contains arrays of pixel points and RGB colors
pixelgroups = {}

pixelgroups['nearby'] = [
	[(818, 108), (102, 169, 224)], # Blue in the GPS icon
	[(818, 126), (102, 169, 224)], # Blue in the GPS icon
	[(818, 138), (255, 255, 255)], # White in the GPS icon
]


# (Clickable) screen points
# If marked as relative, you should probably not touch them.
points = {}
points['focus'] = (1400, 400) # Point to click to make sure we have focus on NOX
points['center'] = (825, 500) # Point to have mouse on screen
points['gpswindow'] = (494, 190) # Top left pixel of where the GPS window is located (ABSOLUTE)
points['latlon'] = (462, 96) # Location of the 'Lat' field in the NOX GPS Window (RELATIVE)
points['move'] = (568, 602) # Location of the 'Move Here' button (RELATIVE)
points['close'] = (682, 16) # Location of the close button (RELATIVE)


# Location coordinates for triliteration
coords = {
	"a": (52.929502, 4.8012571),
	"b": (52.965476, 4.7217422),
	"c": (52.929502, 4.7217422),
	"d": (52.965476, 4.8012571),
	"e": (52.940832, 4.7577242)
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

# Tesseract executable location.
# Replace by "" if you with to use your PATH default.
settings['tesseract'] = ""

# Prints some more info on the screen
settings['printdebug'] = False

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
settings['usersonscreen'] = 14

# If you have a higher resolution than your native resolution, the scrolling might drift.
# To counter this, we re-align after a page
settings['fixscrolldrift'] = True


# Calculations done using the settings themselves
# === You should probably not edit anything beyond this point! ===

# List area on the screen
# Basically same as areas['screen'] but added the topbar and no images on the left
areas['listport'] = (
	areas['screen'][0] + 67,
	areas['screen'][1] + settings['topbar'],
	areas['screen'][2],
	areas['screen'][3],
)

# Convert relative position of GPS window points
areas['gpsreadback'] = (
	areas['gpsreadback'][0] + points['gpswindow'][0],
	areas['gpsreadback'][1] + points['gpswindow'][1],
	areas['gpsreadback'][2] + points['gpswindow'][0],
	areas['gpsreadback'][3] + points['gpswindow'][1],
)
points['latlon'] = (
	points['latlon'][0] + points['gpswindow'][0],
	points['latlon'][1] + points['gpswindow'][1],
)
points['move'] = (
	points['move'][0] + points['gpswindow'][0],
	points['move'][1] + points['gpswindow'][1],
)
