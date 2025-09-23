#!/usr/bin/env python3
import subprocess
import json

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

    # icon = "🎜"
    text = meta['title']
    if meta['artist']:
        text += f" - {meta['artist']}"

    print(json.dumps({
        # "text": f"{icon} {text}",
        "text": f"{text}",
        "tooltip": f"{meta['title']}\n{meta['artist']}\n{meta['album']}",
        "class": "media"
    }))

if __name__ == "__main__":
    main()

