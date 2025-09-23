#!/usr/bin/env python3
import subprocess
import json
import sys

def list_players():
    try:
        output = subprocess.check_output(['playerctl', '-l'], text=True).strip().split('\n')
        return output
    except subprocess.CalledProcessError:
        return []

def metadata(player):
    try:
        output = subprocess.check_output(
            ['playerctl', '-p', player, 'metadata', '--format', '{{title}}||{{artist}}||{{album}}'],
            text=True
        ).strip()
        title, artist, album = (output.split('||') + ['', '', ''])[:3]
        return {
            'title': title,
            'artist': artist,
            'album': album
        }
    except subprocess.CalledProcessError:
        return None

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    action = sys.argv[1]
    icon_map = {
        'prev': '󰒮',
        'next': '󰒭'
    }

    players = list_players()
    ytp_player = next((p for p in players if p.startswith('mps-youtube')), None)
    player = ytp_player if ytp_player else (players[0] if players else None)

    if not player:
        print(json.dumps({"text": "", "class": "nothing"}))
        return

    meta = metadata(player)
    if not meta or not meta['title']:
        print(json.dumps({"text": "", "class": "nothing"}))
        return

    print(json.dumps({
        "text": icon_map.get(action, "?"),
        "class": "media"
    }))

if __name__ == "__main__":
    main()

