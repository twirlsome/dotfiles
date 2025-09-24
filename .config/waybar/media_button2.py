#!/usr/bin/env python3
import gi, json, sys
gi.require_version("Playerctl", "2.0")
from gi.repository import Playerctl, GLib

action = sys.argv[1] if len(sys.argv) > 1 else "?"

icon_map = {
    "prev": "󰒮",
    "next": "󰒭"
}

def print_button(player):
    status = player.props.status
    if status in ("Playing", "Paused"):
        print(json.dumps({
            "text": icon_map.get(action, "?"),
            "class": "media"
        }), flush=True)
    else:
        print(json.dumps({
            "text": "",
            "class": "nothing"
        }), flush=True)

def on_metadata(player, metadata, _=None):
    print_button(player)

def on_status(player, status, _=None):
    print_button(player)

def on_player_appeared(manager, name):
    player = Playerctl.Player.new_from_name(name)
    player.connect("metadata", on_metadata)
    player.connect("playback-status", on_status)
    manager.manage_player(player)
    # Force initial state print on appearance
    print_button(player)

manager = Playerctl.PlayerManager()
manager.connect("name-appeared", on_player_appeared)

# Initialize already running players
for name in manager.props.player_names:
    on_player_appeared(manager, name)

loop = GLib.MainLoop()
loop.run()

