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
    "all-items": "The 38 items of Cobblemon Utility+ 1.8.0 with the names and sprites of this pack.",
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


SUMMARY = "New names and sprites for the items of Cobblemon Utility+ (Mystery, Moldy, Rotten and more)."
with open(os.path.join(ROOT, "DESCRIPTION.md"), encoding="utf-8") as handle:
    call("PATCH", f"/project/{PROJECT}", json.dumps({"description": SUMMARY, "body": handle.read()}).encode(), "application/json")
print("description updated")

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
