#!/usr/bin/env python3
import gi
gi.require_version("Playerctl", "2.0")
from gi.repository import Playerctl, GLib

import sys
import json
import signal
import logging
import argparse
from pathlib import Path

logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    logger.info("Received signal to stop, exiting")
    sys.stdout.write("\n")
    sys.stdout.flush()
    # loop.quit()
    sys.exit(0)

class PlayerManager:
    def __init__(self, selected_player=None, excluded_player=None):
        self.loop = GLib.MainLoop()
        self.manager = Playerctl.PlayerManager()
        self.manager.connect("name-appeared", lambda *args: self.on_player_appeared(*args))
        self.manager.connect("player-vanished", lambda *args: self.on_player_vanished(*args))

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        self.selected_player = selected_player
        self.excluded_player = excluded_player.split(',') if excluded_player else []

        for player in self.manager.props.player_names:
            if player.name in self.excluded_player or (
                self.selected_player is not None and self.selected_player != player.name
            ):
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
        self.on_metadata_changed(player, player.props.metadata)

    def get_players(self):
        return self.manager.props.players

    def write_output(self, text, player):
        logger.debug(f"Writing output: {text}")
        sys.stdout.write(json.dumps({
            "text": text,
            "class": f"custom-{player.props.player_name}",
            "alt": player.props.player_name,
        }) + "\n")
        sys.stdout.flush()

    def clear_output(self):
        sys.stdout.write("\n")
        sys.stdout.flush()

    def on_playback_status_changed(self, player, status, _=None):
        logger.debug(f"Playback status changed for player {player.props.player_name}: {status}")
        self.on_metadata_changed(player, player.props.metadata)

    def get_player_to_display(self):
        players = self.get_players()
        logger.debug(f"Getting first playing player from {len(players)} players")
        if not players:
            logger.debug("No players found")
            return None
        return next((player for player in reversed(players) if player.props.status == "Playing"), players[0])

    def show_most_important_player(self):
        logger.debug("Showing most important player")
        current_player = self.get_player_to_display()
        if current_player is not None:
            self.on_metadata_changed(current_player, current_player.props.metadata)
        else:
            self.clear_output()

    def on_metadata_changed(self, player, metadata, _=None):
        logger.debug(f"Metadata changed for player {player.props.player_name}")
        player_name = player.props.player_name
        artist = player.get_artist()
        title = player.get_title()

        if artist is not None:
            artist = artist.replace("&", "&amp;")
        if title is not None:
            title = title.replace("&", "&amp;")

        track_id = metadata["mpris:trackid"] if metadata is not None and "mpris:trackid" in metadata.keys() else ""
        track_info = (
            "Advertisement"
            if player_name == "spotify" and ":ad:" in track_id
            else f"{title} - {artist}" if artist is not None and title is not None
            else title
        )

        if track_info:
            status_icon = "" if player.props.status == "Playing" else ""
            track_info = f"{status_icon} {track_info}"
        # only print output if no other player is playing
        current_playing = self.get_player_to_display()
        if current_playing is None or current_playing.props.player_name == player.props.player_name:
            self.write_output(track_info, player)
        else:
            logger.debug(f"Other player {current_playing.props.player_name} is playing, skipping")

    def on_player_appeared(self, _, player):
        logger.info(f"Player has appeared: {player.name}")
        if player.name in self.excluded_player or (self.selected_player is not None and self.selected_player != player.name):
            logger.debug("New player appeared, but it's filtered out, skipping")
            return
        self.init_player(player)

    def on_player_vanished(self, _, player):
        logger.info(f"Player {player.props.player_name} has vanished")
        self.show_most_important_player()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-x", "--exclude", help="Comma-separated list of excluded player")
    parser.add_argument("--player", help="Define for which player to listen")
    parser.add_argument("--enable-logging", action="store_true")
    args = parser.parse_args()

    if args.enable_logging:
        logfile = Path(__file__).resolve().with_name("media-player.log")
        logging.basicConfig(
            filename=logfile,
            level=logging.DEBUG,
            format="%(asctime)s %(name)s %(levelname)s:%(lineno)d %(message)s"
        )

    logger.setLevel(max((3 - args.verbose) * 10, 0))

    logger.info("Creating player manager")
    if args.player:
        logger.info(f"Filtering for player: {args.player}")
    if args.exclude:
        logger.info(f"Exclude player {args.exclude}")

    PlayerManager(args.player, args.exclude).run()