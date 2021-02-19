import sys
import os
import openpyxl
import json

sys.path.append('..')
from utils import trilaterate

# We assume all files are in a correct format
# No validation will happen here
def resolve(file, outfile = None):
	# Store combined information
	headers = None
	items = {}

	# Open XLSX file and select active sheet as main
	workbook = openpyxl.load_workbook(file)
	sheet = workbook.active

	# Loop over all rows
	for row in sheet.iter_rows(min_row=2):
		# Make into proper variables
		lat = row[0].value
		lon = row[1].value
		name = row[2].value
		color = row[3].value
		circle_radius = int(row[4].value.split(' ')[0])
		itemtype = row[5].value

		# Make user item if not exists yet
		if name not in items:
			items[name] = {
				"color": color,
				"type": itemtype,
				"circles": [],
				"location": False
			}
		
		# Append circle to user
		items[name]['circles'].append({
			"lat": lat,
			"lon": lon,
			"circle_radius": circle_radius
		})

	# Loop over everyone again and perform trilateration
	for key in items.keys():
		points = []
		for c in items[key]['circles']:
			points.append((c['lat'], c['lon'], c['circle_radius']))
		items[key]['location'] = trilaterate.trilaterate_multi(points)
	
	# Dump to file
	with open(outfile, 'w') as f:
		json.dump(items, f)

# Use as standalone
if __name__ == '__main__':
	# Get file from the commandline.
	# Remove the first arg, since that's the executable name
	args = sys.argv
	args.pop(0)

	# Need minimum of 2 files
	if (len(args) != 1):
		print("Please provide a combined XLSX file from the combiner.")
		exit(1)

	f = args[0]

	# Check extension
	for arg in sys.argv:
		ext = os.path.splitext(arg)[1].lower()
		if (ext != ".xlsx"):
			print("Please provide a combined XLSX file from the combiner.")
			exit(1)
	
	# Check if file exists
	if os.path.exists(f) == False or os.path.isfile(f) == False:
		print("Path is not a valid file: {}".format(f))
		exit(1)
	
	# Run
	resolve(f, "result.json")