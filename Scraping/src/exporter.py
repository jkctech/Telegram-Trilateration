import xlsxwriter
import os
import random

def exportDistancesXLSX(raw, position, filename = "results/result.xlsx"):
	# Make sure folder exists
	try:
		os.makedirs(os.path.dirname(filename))
	except FileExistsError:
		pass

	xlsx = xlsxwriter.Workbook(filename)
	sheet = xlsx.add_worksheet()

	types = ["User", "Group"]

	# Headers
	sheet.write(0, 0, "latitude")
	sheet.write(0, 1, "longitude")
	sheet.write(0, 2, "name")
	sheet.write(0, 3, "color")
	sheet.write(0, 4, "circle_radius")
	sheet.write(0, 5, "type")

	# Loop over items
	for itemtype in range(len(raw)):
		for item in range(len(raw[itemtype])):
			name = raw[itemtype][item][0]
			distance = raw[itemtype][item][1]

			random.seed(name)

			color = random.randint(0, 16777215)
			color = '#' + str(hex(color))[2:]

			sheet.write(item + 1, 0, position[0])
			sheet.write(item + 1, 1, position[1])
			sheet.write(item + 1, 2, name)
			sheet.write(item + 1, 3, color)
			sheet.write(item + 1, 4, "{} m".format(distance))
			sheet.write(item + 1, 5, types[itemtype])

	xlsx.close()