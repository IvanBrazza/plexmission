import requests
import xml.etree.ElementTree as ET
import transmissionrpc as trpc
import json
import os.path
from logger import log

if not os.path.isfile("config.json"):
  log("ERROR", "config.json missing! Did you copy the template?")
  exit(1)

with open("config.json", "r") as f:
  config = json.load(f)

Plex_URL = 'https://{}:{!s}/status/sessions'.format(config["plex"]["hostname"], config["plex"]["port"])

tc = trpc.Client(config["transmission"]["hostname"], port=config["transmission"]["port"])
r = requests.get(Plex_URL, params={"X-Plex-Token": config["plex"]["token"]}, verify=False)
root = ET.fromstring(r.text.encode('utf-8'))

if int(root.attrib['size']) == 0:
    if tc.get_session().alt_speed_enabled:
        log("INFO", "No one is watching anything. Disabling speed restriction.")
        tc.set_session(alt_speed_enabled=False)
    else:
        log("INFO", "No one is watching anything. Speed restriction is already disabled.")
elif int(root.attrib['size']) > 0:
    if tc.get_session().alt_speed_enabled:
        log("INFO", str(root.attrib['size']) + " items are being watched. Speed restriction is already enabled.")
    else:
        log("INFO", str(root.attrib['size']) + " items are being watched. Enabling speed restriction.")
        tc.set_session(alt_speed_enabled=True)
