#!/usr/bin/env python3
import gi
gi.require_version("Playerctl", "2.0")
from gi.repository import Playerctl, GLib
import signal
import sys
import json
import time
import logging
import argparse
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    logger.info("Received signal to stop, exiting")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.exit(0)

class PlayerManager:
    def __init__(self, selected_player=None, excluded_players: Optional[List[str]] = None):
        self.manager = Playerctl.PlayerManager()
        self.loop = GLib.MainLoop()
        self.manager.connect("name-appeared", self.on_player_appeared)
        self.manager.connect("player-vanished", self.on_player_vanished)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        self.selected_player = selected_player
        self.excluded_players = excluded_players if excluded_players else []

        self.player_activity: Dict[str, float] = {}
        self.player_last_status: Dict[str, str] = {}
        self.current_displayed_player: Optional[str] = None
        self._last_output: Optional[dict] = None

        self.priority_order = ["youtube-music", "spotify", "qutebrowser",
                               "firefox", "chromium", "mpv", "brave"]

        self.init_existing_players()

    def init_existing_players(self):
        for name in self.manager.props.player_names:
            if name in self.excluded_players:
                continue
            if self.selected_player and name != self.selected_player:
                continue
            self.init_player(name)

    def run(self):
        self.loop.run()

    def init_player(self, name: str):
        logger.debug(f"Initializing player: {name}")
        player = Playerctl.Player.new_from_name(name)
        player.connect("playback-status", self.on_playback_status_changed)
        player.connect("metadata", self.on_metadata_changed)
        self.manager.manage_player(player)

        self.update_player_activity(name)
        try:
            self.player_last_status[name] = player.props.status
        except Exception:
            self.player_last_status[name] = "Unknown"

        # Force initial metadata handling
        self.on_metadata_changed(player, player.props.metadata)

    def update_player_activity(self, player_name: str):
        self.player_activity[player_name] = time.time()

    def get_players(self):
        valid_players = []
        try:
            for p in self.manager.props.players:
                try:
                    _ = p.props.player_name
                    _ = p.props.status
                    valid_players.append(p)
                except Exception:
                    continue
        except Exception:
            pass
        return valid_players

    def get_most_important_player(self):
        players = self.get_players()
        if not players:
            return None

        def player_sort_key(player):
            name = player.props.player_name
            ts = self.player_activity.get(name, 0)
            status = getattr(player.props, "status", "")
            try:
                prio_idx = self.priority_order.index(name)
            except ValueError:
                prio_idx = len(self.priority_order)
            return (prio_idx, 0 if status == "Playing" else 1, -ts)

        players.sort(key=player_sort_key)
        return players[0]

    def write_output(self, text: str, player):
        if player is None or not text.strip():
            output = {"text": "", "class": "nothing"}
            self.current_displayed_player = None
        else:
            output = {
                "text": text,
                "class": "custom-" + player.props.player_name,
                "alt": player.props.player_name,
            }
            self.current_displayed_player = player.props.player_name

        # Deduplication check
        if self._last_output == output:
            return
        self._last_output = output

        sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def clear_output(self):
        self.write_output("", None)

    def show_top_player(self):
        top = self.get_most_important_player()
        if top is None:
            self.clear_output()
            return

        self.update_player_activity(top.props.player_name)
        self.on_metadata_changed(top, top.props.metadata)

    def on_playback_status_changed(self, player, status, *_):
        name = player.props.player_name
        self.player_last_status[name] = status
        self.update_player_activity(name)
        self.show_top_player()

    def on_metadata_changed(self, player, metadata, *_):
        try:
            name = player.props.player_name
            self.update_player_activity(name)

            top = self.get_most_important_player()
            if top is None or player.props.player_name != top.props.player_name:
                return

            artist = player.get_artist() or ""
            title = player.get_title() or ""

            # If only title is available, print it but allow update later
            if artist and title:
                track_info = f"{artist} - {title}"
            elif title:
                track_info = title
            elif artist:
                track_info = artist
            else:
                self.clear_output()
                return

            track_info = " " + track_info + " "
            self.write_output(track_info, player)
        except Exception as e:
            logger.exception(f"Metadata handling error: {e}")
            self.show_top_player()

    def on_player_appeared(self, _, name: str):
        if name in self.excluded_players:
            return
        if self.selected_player and name != self.selected_player:
            return
        self.init_player(name)
        self.show_top_player()

    def on_player_vanished(self, _, player):
        try:
            name = getattr(player, 'props', None) and player.props.player_name or str(player)
            self.player_activity.pop(name, None)
            self.player_last_status.pop(name, None)
            if self.current_displayed_player == name:
                self.current_displayed_player = None
        except Exception:
            pass
        self.show_top_player()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-x", "--exclude", help="Comma-separated excluded players")
    parser.add_argument("--player", help="Listen to only a specific player")
    parser.add_argument("--enable-logging", action="store_true")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.enable_logging:
        logfile = "media-player.log"
        logging.basicConfig(filename=logfile, level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s: %(message)s")
    logger.setLevel(max(10, 30 - (args.verbose or 0)*10))

    excluded = args.exclude.split(",") if args.exclude else []
    manager = PlayerManager(selected_player=args.player, excluded_players=excluded)
    manager.run()

if __name__ == "__main__":
    main()

