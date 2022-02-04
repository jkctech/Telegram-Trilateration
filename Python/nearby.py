import warnings
import asyncio
import configparser
import os

from telethon import TelegramClient
from telethon import functions, types
from pathlib import Path

# We don't do that here
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Read config
config = configparser.ConfigParser()
config.read("config.ini")

# Apply config
api_id = config['API']['api_id']
api_hash = config['API']['api_hash']

# Location
lat = 52.3794715
lon = 4.9000994

# Preparations
if (config['SETTINGS']['profilepictures'] and os.path.exists(config['SETTINGS']['profilepicturespath'])):
	Path(config['SETTINGS']['profilepicturespath']).mkdir(parents=True, exist_ok=True)

async def find():
	# Setup client
	client = TelegramClient("trilat", api_id, str(api_hash))
	await client.start()
	await client.get_me()
	
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
			name = "{} {}".format(ent.first_name, ent.last_name)

		# GROUP
		elif hasattr(p.peer, "channel_id"):
			id = p.peer.channel_id
			prefix = "g"
			ent = await client.get_entity(id)
			name = ent.title

		# Save profile picture
		if (config['SETTINGS']['profilepictures']):
			path = "{}{}_{}.jpg".format(config['SETTINGS']['profilepicturespath'], prefix, id)
			if os.path.exists(path) == False:
				await client.download_profile_photo(ent, file=path)

		# Print data
		print("[{}] [{}] {} -- Distance: {} meter(s)".format(id, prefix.upper(), name, p.distance))

# Run
loop = asyncio.get_event_loop()
tasks = [ loop.create_task(find()) ]
loop.run_until_complete(asyncio.wait(tasks))