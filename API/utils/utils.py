import random

def usercolor(name):
	# Seed the randomizer with the entry name
	# We use this to generate a Hex color for the displaying.
	# This way, every user always has the same color.
	random.seed(name)

	# Generate color
	color = random.randint(0, 16777215)
	color = '#' + str(hex(color))[2:]

	return color