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
from typing import List

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

        self.init_players()

    def init_players(self):
        # Initialize currently-known players
        for player in self.manager.props.player_names:
            if player.name in self.excluded_player:
                continue
            if self.selected_player is not None and self.selected_player != player.name:
                logger.debug(f"{player.name} is not the filtered player, skipping it")
                continue
            self.init_player(player)

    def run(self):
        logger.info("Starting main loop")
        self.loop.run()

    def init_player(self, player):
        logger.info(f"Initialize new player: {player.name}")
        player = Playerctl.Player.new_from_name(player)
        player.connect("playback-status", self.on_playback_status_changed, None)
        player.connect("metadata", self.on_metadata_changed, None)
        self.manager.manage_player(player)
        # force initial metadata handling (may emit nothing if no metadata)
        self.on_metadata_changed(player, player.props.metadata)

    def get_players(self) -> List[Player]:
        return self.manager.props.players

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
        else:
            output = {
                "text": text,
                "class": "custom-" + player.props.player_name,
                "alt": player.props.player_name
            }
        sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def clear_output(self):
        # Convenience to send the 'nothing' object
        self.write_output("", None)

    def on_playback_status_changed(self, player, status, _=None):
        logger.debug(f"Playback status changed for player {player.props.player_name}: {status}")
        # Re-evaluate metadata display when playback status changes
        self.on_metadata_changed(player, player.props.metadata)

    def get_first_playing_player(self):
        players = self.get_players()
        logger.debug(f"Getting first playing player from {len(players)} players")
        if len(players) > 0:
            # prefer any that are playing (reverse so most recently added preferred)
            for p in players[::-1]:
                if p.props.status == "Playing":
                    return p
            # otherwise return the first known player
            return players[0]
        logger.debug("No players found")
        return None

    def show_most_important_player(self):
        logger.debug("Showing most important player")
        current_player = self.get_first_playing_player()
        if current_player is not None:
            # display metadata for that player (may result in nothing if no metadata)
            self.on_metadata_changed(current_player, current_player.props.metadata)
        else:
            # no players at all -> collapse
            self.clear_output()

    def on_metadata_changed(self, player, metadata, _=None):
        """
        Create a cleaned-up track string only if meaningful metadata exists.
        Otherwise emit the 'nothing' state.
        """
        try:
            logger.debug(f"Metadata changed for player {player.props.player_name}")
            player_name = player.props.player_name

            # Safely fetch artist/title (may be None)
            artist = player.get_artist()
            title = player.get_title()

            # Normalize and escape ampersands if present (avoid HTML mis-parsing)
            artist = artist.replace("&", "&amp;") if artist else ""
            title = title.replace("&", "&amp;") if title else ""

            # Build track_info only if we have something meaningful
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
                # no useful metadata -> emit nothing
                logger.debug("No artist or title found; emitting nothing")
                # only show nothing if this is the most important player
                current_playing = self.get_first_playing_player()
                if current_playing is None or current_playing.props.player_name == player.props.player_name:
                    self.clear_output()
                return

            # Prefix with play/pause icon
            if player.props.status == "Playing":
                track_info = " " + track_info
            else:
                track_info = " " + track_info

            # only print if this is the most important player
            current_playing = self.get_first_playing_player()
            if current_playing is None or current_playing.props.player_name == player.props.player_name:
                self.write_output(track_info, player)
            else:
                logger.debug(f"Other player {current_playing.props.player_name} is playing, skipping output for {player.props.player_name}")
        except Exception:
            # On any unexpected error, do not crash — emit nothing
            logger.exception("Exception in on_metadata_changed; emitting nothing")
            self.clear_output()

    def on_player_appeared(self, _, player):
        logger.info(f"Player has appeared: {player.name}")
        if player.name in self.excluded_player:
            logger.debug("New player appeared, but it's in exclude player list, skipping")
            return
        if player is not None and (self.selected_player is None or player.name == self.selected_player):
            self.init_player(player)
        else:
            logger.debug("New player appeared, but it's not the selected player, skipping")

    def on_player_vanished(self, _, player):
        # Called when a player vanishes; update display to next important player or nothing
        try:
            logger.info(f"Player vanished: {player.props.player_name if hasattr(player, 'props') else player}")
        except Exception:
            logger.info("Player vanished (unknown)")
        # Re-evaluate the most important player and show appropriate output (or nothing)
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

    # Initialize logging to a file if requested
    if arguments.enable_logging:
        logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media-player.log")
        logging.basicConfig(filename=logfile, level=logging.DEBUG,
                            format="%(asctime)s %(name)s %(levelname)s:%(lineno)d %(message)s")

    # Default logger level is WARN; -v lowers it
    logger.setLevel(max((3 - (arguments.verbose or 0)) * 10, 0))

    logger.info("Creating player manager")
    if arguments.player:
        logger.info(f"Filtering for player: {arguments.player}")
    if arguments.exclude:
        logger.info(f"Exclude player {arguments.exclude}")

    player_manager = PlayerManager(arguments.player, arguments.exclude)
    player_manager.run()


if __name__ == "__main__":
    main()

