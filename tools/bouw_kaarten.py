#!/usr/bin/env python3
"""Maakt cards.json uit videos.md (links + fragmenten) en titels.txt (jaartal + titel).

Gebruik:  python3 tools/bouw_kaarten.py
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "videos.md"
TITELS = ROOT / "titels.txt"
OUT = ROOT / "cards.json"

# Kaarten die niet ingesloten mogen worden: alleen een knop naar YouTube.
YOUTUBE_ONLY = {"sSvHPuOz_w0"}


def parse_time(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


def parse_videos():
    rows = {}
    for line in VIDEOS.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        cols = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        nr, link, _bron, frag = int(cols[0]), cols[1], cols[2], cols[3]
        start, end = 0, None
        m = re.match(r"(\d+:\d{2})\s*[–-]\s*(\d+:\d{2})", frag)
        if m:
            start, end = parse_time(m.group(1)), parse_time(m.group(2))
        rows[nr] = {"link": link, "start": start, "end": end}
    return rows


def parse_titels():
    rows = {}
    for line in TITELS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|", 2)]
        if len(parts) != 3:
            sys.exit(f"Kan deze regel in titels.txt niet lezen: {line!r}")
        nr, jaar, titel = parts
        titel = re.sub(r"^\?\?\s*", "", titel)
        rows[int(nr)] = {"year": int(jaar), "title": titel}
    return rows


def dumpert_media(item_id):
    url = f"https://api-live.dumpert.nl/mobile_api/json/info/{item_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    item = data["items"][0]
    variants = {v["version"]: v["uri"] for v in item["media"][0]["variants"]}
    return variants.get("720p") or variants.get("stream"), variants.get("still-large")


def main():
    videos, titels = parse_videos(), parse_titels()
    missing = sorted(set(videos) ^ set(titels))
    if missing:
        sys.exit(f"Nummers staan niet in beide bestanden: {missing}")

    cards = []
    for nr in sorted(videos):
        v, t = videos[nr], titels[nr]
        card = {"id": f"{nr:03d}", "year": t["year"], "title": t["title"],
                "start": v["start"], "end": v["end"]}
        link = v["link"]
        if "dumpert.nl" in link:
            item_id = link.rstrip("/").split("/")[-1]
            hls, poster = dumpert_media(item_id)
            card.update(source="dumpert", url=link, hls=hls)
        else:
            m = re.search(r"(?:v=|shorts/)([A-Za-z0-9_-]{11})", link)
            yt = m.group(1)
            card.update(source="youtube-only" if yt in YOUTUBE_ONLY else "youtube", youtube=yt)
            if "/shorts/" in link:
                card["vertical"] = True
        cards.append(card)

    OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(cards)} kaarten geschreven naar {OUT.name}")


if __name__ == "__main__":
    main()
