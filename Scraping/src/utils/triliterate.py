import math
import numpy
import itertools

# Function for triliteration
# This function is based (Or copied technically) on this post:
# - https://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-longitude-points-and-3-distances/415
# HOWEVER: It seems this function can generate different outputs based on the order of input variables...
# We "solve" this issue down below in a dirty way because I don't understand math that well
def triliterate(raw):
	# Earth's radius (In km) at sea level
	earthR = 6371

	# Parse our raw list into variables to make more readable
	LatA = raw[0][0]
	LonA = raw[0][1]
	DistA = raw[0][2] / 1000

	LatB = raw[1][0]
	LonB = raw[1][1]
	DistB = raw[1][2] / 1000

	LatC = raw[2][0]
	LonC = raw[2][1]
	DistC = raw[2][2] / 1000

	# Convert lat, lon coords to positions
	xA = earthR *(math.cos(math.radians(LatA)) * math.cos(math.radians(LonA)))
	yA = earthR *(math.cos(math.radians(LatA)) * math.sin(math.radians(LonA)))
	zA = earthR *(math.sin(math.radians(LatA)))

	xB = earthR *(math.cos(math.radians(LatB)) * math.cos(math.radians(LonB)))
	yB = earthR *(math.cos(math.radians(LatB)) * math.sin(math.radians(LonB)))
	zB = earthR *(math.sin(math.radians(LatB)))

	xC = earthR *(math.cos(math.radians(LatC)) * math.cos(math.radians(LonC)))
	yC = earthR *(math.cos(math.radians(LatC)) * math.sin(math.radians(LonC)))
	zC = earthR *(math.sin(math.radians(LatC)))

	P1 = numpy.array([xA, yA, zA])
	P2 = numpy.array([xB, yB, zB])
	P3 = numpy.array([xC, yC, zC])

	# Transform to get circle 1 at origin
	# Transform to get circle 2 on x axis
	# (This is the part my math knowledge ends)
	ex = (P2 - P1) / (numpy.linalg.norm(P2 - P1))
	i = numpy.dot(ex, P3 - P1)
	ey = (P3 - P1 - i * ex) / (numpy.linalg.norm(P3 - P1 - i * ex))
	ez = numpy.cross(ex, ey)
	d = numpy.linalg.norm(P2 - P1)
	j = numpy.dot(ey, P3 - P1)

	# Convert above to xyz
	x = (pow(DistA, 2) - pow(DistB, 2) + pow(d, 2)) / (2 * d)
	y = ((pow(DistA, 2) - pow(DistC, 2) + pow(i, 2) + pow(j, 2)) / (2  *j)) - ((i / j) * x)
	z = numpy.sqrt(abs(pow(DistA, 2) - pow(x, 2) - pow(y, 2))) # Fixed negative sqrt calculations by using abs()

	# triPt is an array with ECEF x,y,z of trilateration point
	triPt = P1 + x * ex + y * ey + z * ez

	# Convert back to lat / lon
	lat = math.degrees(math.asin(triPt[2] / earthR))
	lon = math.degrees(math.atan2(triPt[1], triPt[0]))

	return (lat, lon)

# This is... Dirty...
# We generate ALL POSSIBLE ways of ordering our input coordinates...
# We store the calculated lat / lon values and later get the avarages
# This actually solves the above mentioned problem.
def triliterate_correct(raw):
	# We will store calculated values here
	lats = []
	lons = []

	# Loop over ALL COMBINATIONS of these coords....
	for item in itertools.permutations(raw):
		res = triliterate(item)
		lats.append(res[0])
		lons.append(res[1])

	# Calculate the avarages...
	lat = sum(lats) / len(lats)
	lon = sum(lons) / len(lons)

	return (lat, lon)

# Example
if __name__ == '__main__':
	# Coordinates and distances in meters
	raw = [
		(52.907848, 4.684513, 6420),
		(52.94083, 4.7577238, 1430),
		(52.894424, 4.8364009, 8780)
	]

	print("Inputs:")

	for i in raw:
		print("{}\t{}\t[{} m distance]".format(i[0], i[1], i[2]))

	# Execute triliteration
	res = triliterate_correct(raw)

	# Print, but with rounding to 7th digit.
	print("\nResult:")
	print((round(res[0], 7), round(res[1], 7)))
