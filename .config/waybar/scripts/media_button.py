#!/usr/bin/env python3
import gi, json, sys, time
gi.require_version("Playerctl", "2.0")
from gi.repository import Playerctl, GLib

action = sys.argv[1] if len(sys.argv) > 1 else "?"

icon_map = {
    "prev": "󰒮",
    "next": "󰒭"
}

manager = Playerctl.PlayerManager()

# Track activity times and last statuses
player_activity = {}
player_status = {}

def pick_player():
    """Choose the most relevant player: Playing > Paused > others, sorted by recency."""
    players = manager.props.players
    if not players:
        return None
    now = time.time()
    choices = []
    for p in players:
        try:
            status = p.props.status
            ts = player_activity.get(p.props.player_name, 0)
            choices.append((p, status, ts))
        except:
            continue

    # Prioritize Playing, then Paused, then others. Sort by recency.
    playing = sorted([c for c in choices if c[1] == "Playing"], key=lambda x: x[2], reverse=True)
    paused = sorted([c for c in choices if c[1] == "Paused"], key=lambda x: x[2], reverse=True)
    others = sorted([c for c in choices if c[1] not in ("Playing", "Paused")], key=lambda x: x[2], reverse=True)

    if playing: return playing[0][0]
    if paused: return paused[0][0]
    if others: return others[0][0]
    return None

def print_button():
    player = pick_player()
    if player is None:
        output = {"text": "", "class": "nothing"}
    else:
        status = player.props.status
        if status in ("Playing", "Paused"):
            output = {"text": icon_map.get(action, "?"), "class": "media"}
        else:
            output = {"text": "", "class": "nothing"}
    print(json.dumps(output), flush=True)

def on_metadata(player, metadata, _=None):
    player_activity[player.props.player_name] = time.time()
    player_status[player.props.player_name] = player.props.status
    print_button()

def on_status(player, status, _=None):
    player_activity[player.props.player_name] = time.time()
    player_status[player.props.player_name] = status
    print_button()

def on_player_appeared(manager, name):
    player = Playerctl.Player.new_from_name(name)
    player.connect("metadata", on_metadata)
    player.connect("playback-status", on_status)
    manager.manage_player(player)
    # initialize state
    player_activity[player.props.player_name] = time.time()
    player_status[player.props.player_name] = player.props.status
    print_button()

manager.connect("name-appeared", on_player_appeared)

# Initialize existing players
for name in manager.props.player_names:
    on_player_appeared(manager, name)

loop = GLib.MainLoop()
loop.run()

