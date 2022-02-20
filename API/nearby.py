import warnings
import asyncio
import os
import json

from datetime import datetime
from telethon import TelegramClient
from telethon import functions, types
from pathlib import Path

from utils import trilaterate, utils

# We don't do that here
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Read config
config = json.load(open("config.json"))

# Apply config
api_id = config['api']['api_id']
api_hash = config['api']['api_hash']
points = config['points']

# Storage
result = {}

# Preparations
if (config['settings']['profilepictures'] and os.path.exists(config['settings']['profilepicturespath'])):
	Path(config['settings']['profilepicturespath']).mkdir(parents=True, exist_ok=True)

# Setup client
client = TelegramClient("trilat", api_id, str(api_hash))
async def setup():
	print("Connecting to Telegram...")
	await client.start()
	print("Connected!")

async def find(lat, lon):
	print("=" * 15, " Polling @ {} {} ".format(lat, lon), "=" * 15)

	# Pull nearby people
	data = await client(functions.contacts.GetLocatedRequest(geo_point=types.InputGeoPoint(lat=lat, long=lon)))
	peers = data.updates[0].peers

	# Loop over all found entries
	for p in peers:
		# USER
		if hasattr(p.peer, "user_id"):
			id = p.peer.user_id
			prefix = "u"
			ent = await client.get_entity(id)
			name = "{} {}".format(str(ent.first_name or ''), str(ent.last_name or ''))
			enttype = "User"

		# GROUP
		elif hasattr(p.peer, "channel_id"):
			id = p.peer.channel_id
			prefix = "g"
			ent = await client.get_entity(id)
			name = ent.title
			enttype = "Group"
		
		name = name.strip()

		# Save profile picture
		if (config['settings']['profilepictures']):
			path = "{}{}_{}.jpg".format(config['settings']['profilepicturespath'], prefix, id)
			if os.path.exists(path) == False:
				await client.download_profile_photo(ent, file=path)
		
		# Record to result
		if id not in result:
			result[id] = {
				"name": name,
				"color": utils.usercolor(name),
				"type": enttype,
				"circles": [],
				"location": False
			}
		
		result[id]['circles'].append({
			"lat": lat,
			"lon": lon,
			"circle_radius": p.distance,
		})

		# Print & write data
		out = "[{}] [{}] {} -- Distance: {} meter(s)".format(id, prefix.upper(), name, p.distance)
		print(out)
	
	print("=" * 15, " FINISHED! ", "=" * 15)

# Run
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(setup())

# Run all points
for p in points:
	loop.run_until_complete(find(p[0], p[1]))

# Resolve locations
print("Starting resolver...")

# Loop over entities
for id in result.keys():
	ent = result[id]

	print("Locating {}...".format(ent['name']))

	# Collect data
	raw = []
	for c in ent['circles']:
		print("\t{}\t{}\t[{} m distance]".format(c['lat'], c['lon'], c['circle_radius']))
		raw.append((c['lat'], c['lon'], c['circle_radius']))

	# Execute trilateration
	loc = trilaterate.trilaterate_multi(raw)

	if loc == False:
		print("\tERROR: Could not resolve location.")
		result[id]['location'] = False
	else:
		print("\tEstimated location: {}".format(loc))
		result[id]['location'] = list(loc)

# Save to file
print("Saving to file...")
path = "data/{}.json".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f"))
outfile = open(path, 'wb')
outfile.write(json.dumps(result, indent=4).encode("UTF-8"))
outfile.write(b"\n")
outfile.close()
print("Saved to: {}".format(path))
