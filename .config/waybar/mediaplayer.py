#!/usr/bin/env python3
import gi
gi.require_version("Playerctl", "2.0")
from gi.repository import Playerctl, GLib
from gi.repository.Playerctl import Player
import argparse
import logging
import sys
import signal
import json
import os
import time
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    logger.info("Received signal to stop, exiting")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.exit(0)


class PlayerManager:
    def __init__(self, selected_player=None, excluded_player=[]):
        self.manager = Playerctl.PlayerManager()
        self.loop = GLib.MainLoop()
        # connect to player appearance / disappearance
        self.manager.connect("name-appeared", lambda *args: self.on_player_appeared(*args))
        self.manager.connect("player-vanished", lambda *args: self.on_player_vanished(*args))

        # install signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        self.selected_player = selected_player
        self.excluded_player = excluded_player.split(',') if excluded_player else []
        
        # Track the last displayed player to avoid unnecessary updates
        self.current_displayed_player = None
        
        # Track player activity timestamps to prioritize most recent
        self.player_activity: Dict[str, float] = {}
        
        # Track last known status to detect changes
        self.player_last_status: Dict[str, str] = {}

        self.init_players()

    def update_player_activity(self, player_name: str):
        """Update the activity timestamp for a player"""
        self.player_activity[player_name] = time.time()
        logger.debug(f"Updated activity for {player_name}: {self.player_activity[player_name]}")

    def init_players(self):
        # Initialize currently-known players
        for name in self.manager.props.player_names:
            if name in self.excluded_player:
                continue
            if self.selected_player is not None and self.selected_player != name:
                logger.debug(f"{name} is not the filtered player, skipping it")
                continue
            self.init_player(name)

    def run(self):
        logger.info("Starting main loop")
        self.loop.run()

    def init_player(self, name: str):
        logger.info(f"Initialize new player: {name}")
        player = Playerctl.Player.new_from_name(name)
        player.connect("playback-status", self.on_playback_status_changed, None)
        player.connect("metadata", self.on_metadata_changed, None)
        self.manager.manage_player(player)
        
        # Initialize activity tracking
        self.update_player_activity(player.props.player_name)
        
        # Initialize status tracking
        try:
            self.player_last_status[player.props.player_name] = player.props.status
        except:
            self.player_last_status[player.props.player_name] = "Unknown"
        
        # force initial metadata handling (may emit nothing if no metadata)
        self.on_metadata_changed(player, player.props.metadata)

    def get_players(self) -> List[Player]:
        """Get list of valid, accessible players"""
        players = []
        try:
            for player in self.manager.props.players:
                try:
                    _ = player.props.player_name
                    _ = player.props.status
                    players.append(player)
                except Exception as e:
                    logger.debug(f"Player is no longer valid: {e}")
                    continue
        except Exception as e:
            logger.debug(f"Error getting players: {e}")
        return players

    def write_output(self, text: str, player):
        """
        Writes JSON to stdout. If `player` is None or `text` is empty,
        emit the `nothing` class so CSS can collapse the widget.
        """
        logger.debug(f"Writing output: text={text!r}, player={getattr(player, 'props', None)}")
        if player is None or not text or not text.strip():
            output = {
                "text": "",
                "class": "nothing"
            }
            self.current_displayed_player = None
        else:
            output = {
                "text": text,
                "class": "custom-" + player.props.player_name,
                "alt": player.props.player_name
            }
            self.current_displayed_player = player.props.player_name
        sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def clear_output(self):
        self.write_output("", None)

    def on_playback_status_changed(self, player, status, _=None):
        player_name = player.props.player_name
        logger.debug(f"Playback status changed for player {player_name}: {status}")
        
        old_status = self.player_last_status.get(player_name, "Unknown")
        self.player_last_status[player_name] = status
        
        if status == "Playing" or (old_status in ["Stopped", "Unknown"] and status == "Paused"):
            self.update_player_activity(player_name)
            logger.debug(f"Player {player_name} became more active: {old_status} -> {status}")
        
        self.show_most_important_player()

    def get_most_recent_active_player(self) -> Optional[Player]:
        players = self.get_players()
        if not players:
            return None
        
        playing_players, paused_players, other_players = [], [], []
        for player in players:
            try:
                status = player.props.status
                player_name = player.props.player_name
                ts = self.player_activity.get(player_name, 0)
                if status == "Playing":
                    playing_players.append((player, ts))
                elif status == "Paused":
                    paused_players.append((player, ts))
                else:
                    other_players.append((player, ts))
            except Exception as e:
                logger.debug(f"Error checking player status: {e}")
                continue
        
        playing_players.sort(key=lambda x: x[1], reverse=True)
        paused_players.sort(key=lambda x: x[1], reverse=True)
        other_players.sort(key=lambda x: x[1], reverse=True)
        
        if playing_players:
            return playing_players[0][0]
        elif paused_players:
            return paused_players[0][0]
        elif other_players:
            return other_players[0][0]
        return None

    def is_player_playing(self, player) -> bool:
        try:
            return player.props.status == "Playing"
        except:
            return False

    def is_player_paused(self, player) -> bool:
        try:
            return player.props.status == "Paused"
        except:
            return False

    def show_most_important_player(self):
        current_player = self.get_most_recent_active_player()
        if current_player is not None:
            try:
                self.on_metadata_changed(current_player, current_player.props.metadata)
            except Exception as e:
                logger.debug(f"Error accessing metadata: {e}")
                self.clear_output()
        else:
            self.clear_output()

    def on_metadata_changed(self, player, metadata, _=None):
        try:
            player_name = player.props.player_name
            self.update_player_activity(player_name)
            
            current_active = self.get_most_recent_active_player()
            if current_active is None:
                self.clear_output()
                return
            if current_active.props.player_name != player_name:
                return

            artist = player.get_artist() or ""
            title = player.get_title() or ""

            artist = artist.replace("&", "&amp;")
            title = title.replace("&", "&amp;")

            track_info = ""
            if player_name == "spotify" and isinstance(metadata, dict) and "mpris:trackid" in metadata.keys() and ":ad:" in player.props.metadata.get("mpris:trackid", ""):
                track_info = "Advertisement"
            elif artist and title:
                track_info = f"{artist} - {title}"
            elif title:
                track_info = title
            elif artist:
                track_info = artist
            else:
                self.clear_output()
                return

            track_info = " " + track_info
            self.write_output(track_info, player)
            
        except Exception as e:
            logger.exception(f"Exception in on_metadata_changed: {e}")
            self.show_most_important_player()

    def on_player_appeared(self, _, name: str):
        logger.info(f"Player has appeared: {name}")
        if name in self.excluded_player:
            return
        if self.selected_player is None or name == self.selected_player:
            self.init_player(name)
            self.show_most_important_player()

    def on_player_vanished(self, _, player):
        try:
            player_name = player.props.player_name if hasattr(player, 'props') else str(player)
            logger.info(f"Player vanished: {player_name}")
            
            if player_name in self.player_activity:
                del self.player_activity[player_name]
            if player_name in self.player_last_status:
                del self.player_last_status[player_name]
            
            if self.current_displayed_player == player_name:
                self.current_displayed_player = None
        except Exception as e:
            logger.info(f"Player vanished (error getting name): {e}")
        
        self.show_most_important_player()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="increase verbosity (-v, -vv, -vvv)")
    parser.add_argument("-x", "--exclude", help="Comma-separated list of excluded player")
    parser.add_argument("--player", help="Only listen to a specific player")
    parser.add_argument("--enable-logging", action="store_true", help="Enable logging to file")
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    if arguments.enable_logging:
        logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media-player.log")
        logging.basicConfig(filename=logfile, level=logging.DEBUG,
                            format="%(asctime)s %(name)s %(levelname)s:%(lineno)d %(message)s")

    logger.setLevel(max((3 - (arguments.verbose or 0)) * 10, 0))

    player_manager = PlayerManager(arguments.player, arguments.exclude)
    player_manager.run()


if __name__ == "__main__":
    main()

