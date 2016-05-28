import transmissionrpc as trpc
import datetime
import json
import os.path
from logger import log

if not os.path.isfile("config.json"):
  log("ERROR", "config.json missing! Did you copy the template?")
  exit(1)

with open("config.json", "r") as f:
  config = json.load(f)

tc = trpc.Client(config["transmission"]["hostname"], port=config["transmission"]["port"])

for torrent in tc.get_torrents():
    if torrent.isFinished:
        log("INFO", 'Torrent "{!s}" is finished. Deleting...'.format(torrent.name))
        tc.remove_torrent(torrent.hashString, delete_data=True, timeout=300)
    elif (not torrent.isFinished) and torrent.status == 'stopped':
        log("INFO", 'Torrent "{!s}" is not finished and not seeding. Starting...'.format(torrent.name))
        tc.start_torrent(torrent.hashString, timeout=300)
    elif (not torrent.isFinished) and torrent.status == 'seeding':
        log("INFO", 'Torrent "{!s}" is seeding. Current ratio: {!s}'.format(torrent.name, torrent.uploadRatio))
    else:
        log("INFO", "Unknown status for torrent '" + str(torrent.name) + "'")
