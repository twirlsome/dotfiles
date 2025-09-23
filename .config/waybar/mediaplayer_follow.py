#!/usr/bin/env python3
import subprocess
import json

def main():
    # playerctl follow prints lines like: title\x1fartist\x1falbum
    proc = subprocess.Popen(
        ["playerctl", "--follow", "metadata", "--format", "{{title}}||{{artist}}||{{album}}"],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue

        title, artist, album = (line.split("||") + ["", "", ""])[:3]

        text = title
        if artist:
            text += f" - {artist}"

        print(json.dumps({
            "text": text,
            "tooltip": f"{title}\n{artist}\n{album}",
            "class": "media"
        }), flush=True)

if __name__ == "__main__":
    main()

