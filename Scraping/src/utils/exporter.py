import xlsxwriter
import os
import random
import json
import time

def usercolor(name):
	# Seed the randomizer with the entry name
	# We use this to generate a Hex color for the displaying.
	# This way, every user always has the same color.
	random.seed(name)

	# Generate color
	color = random.randint(0, 16777215)
	color = '#' + str(hex(color))[2:]

	return color

# XLSX Exporter in https://www.gpsvisualizer.com/ format
def exportDistancesXLSX(raw, position, filename = "results/result.xlsx"):
	# Make sure folder exists
	try:
		os.makedirs(os.path.dirname(filename))
	except FileExistsError:
		pass

	# Create new file
	xlsx = xlsxwriter.Workbook(filename)
	sheet = xlsx.add_worksheet()

	# We have 2 types of entries
	types = ["User", "Group"]

	# Headers
	sheet.write(0, 0, "latitude")
	sheet.write(0, 1, "longitude")
	sheet.write(0, 2, "name")
	sheet.write(0, 3, "color")
	sheet.write(0, 4, "circle_radius")
	sheet.write(0, 5, "type")
	sheet.write(0, 6, "timestamp")

	timestamp = int(time.time())

	# Loop over items
	for itemtype in range(len(raw)):
		for item in range(len(raw[itemtype])):
			# Shorten
			name = raw[itemtype][item][0]
			distance = raw[itemtype][item][1]
			
			color = usercolor(name)

			sheet.write(item + 1, 0, position[0])
			sheet.write(item + 1, 1, position[1])
			sheet.write(item + 1, 2, name)
			sheet.write(item + 1, 3, color)
			sheet.write(item + 1, 4, "{} m".format(distance))
			sheet.write(item + 1, 5, types[itemtype])
			sheet.write(item + 1, 6, timestamp)

	xlsx.close()

# Export in proprietary JSON format
def exportDistancesJSON(raw, position, filename = "results/result.json"):
	# Make sure folder exists
	try:
		os.makedirs(os.path.dirname(filename))
	except FileExistsError:
		pass
	
	# Types
	types = ["users", "groups"]

	# Make dict
	result = {
		"latitude": position[0],
		"longitude": position[1],
		"timestamp": int(time.time()),
		"users": [],
		"groups": []
	}

	# Append all data to dict
	for i in range(len(types)):
		itemlist = raw[i]
		for item in itemlist:
			result[types[i]].append({
				"name": item[0],
				"distance": item[1],
				"color": usercolor(item[0]),
			})
	
	# Dump to file
	with open(filename, 'w') as outfile:
		json.dump(result, outfile)