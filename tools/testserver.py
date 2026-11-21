#!/usr/bin/env python3
"""Lokale testserver die nooit iets laat cachen (je ziet altijd de nieuwste versie).

Gebruik:  python3 tools/testserver.py      → http://localhost:8765
"""
import http.server
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent.parent)


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


http.server.ThreadingHTTPServer(("0.0.0.0", 8765), NoCache).serve_forever()
