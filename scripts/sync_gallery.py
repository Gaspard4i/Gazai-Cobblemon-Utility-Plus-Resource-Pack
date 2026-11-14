"""Replaces the gallery of the Modrinth project with the images of gallery/ (first one featured, order by file name).

usage: python scripts/sync_gallery.py   (needs MODRINTH_TOKEN and MODRINTH_PROJECT_ID)
"""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.modrinth.com/v2"
TOKEN = os.environ["MODRINTH_TOKEN"]
PROJECT = os.environ["MODRINTH_PROJECT_ID"]
DESCRIPTIONS = {
    "all-items": "Every retextured item.",
    "stat-candies": "The stat candies, one family per stat.",
    "whole-pokemon": "Items that change a whole Pokemon.",
    "identity": "Shiny, gender, Poke Ball and evolution stage.",
    "growth-and-riding": "Level, friendship and riding stats.",
    "alpha-and-fossils": "The Alpha Candy and the fossils.",
}


def call(method, path, data=None, content_type=None, query=None):
    url = API + path + ("?" + urllib.parse.urlencode(query) if query else "")
    headers = {"Authorization": TOKEN, "User-Agent": "resource-pack-gallery-sync"}
    if content_type:
        headers["Content-Type"] = content_type
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=headers)) as response:
            raw = response.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as error:
        raise SystemExit(f"{method} {path} failed: {error.code} {error.read().decode(errors='replace')}")


folder = os.path.join(ROOT, "gallery")
files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
for entry in call("GET", f"/project/{PROJECT}").get("gallery", []):
    call("DELETE", f"/project/{PROJECT}/gallery", query={"url": entry["url"]})
for order, name in enumerate(files):
    key = re.sub(r"^\d+-", "", name[:-4])
    query = {"ext": "png", "featured": str(order == 0).lower(), "title": key.replace("-", " ").capitalize(), "ordering": order}
    if key in DESCRIPTIONS:
        query["description"] = DESCRIPTIONS[key]
    with open(os.path.join(folder, name), "rb") as handle:
        call("POST", f"/project/{PROJECT}/gallery", handle.read(), "image/png", query)
    print("uploaded", name)
