#!/usr/bin/env bash
set -e

# Step 1: Find the first actively playing player
player=$(playerctl -l | while read -r p; do
    if playerctl -p "$p" status 2>/dev/null | grep -qi "Playing"; then
        echo "$p"
        break
    fi
done)

if [ -z "$player" ]; then
    notify-send "No active media player"
    exit 0
fi

# Step 2: Try to get desktop-entry, fallback to player name
desktop_entry=$(playerctl -p "$player" metadata xesam:desktop-entry 2>/dev/null || true)
if [ -z "$desktop_entry" ]; then
    desktop_entry="$player"
fi

# Step 3: Map to Hyprland window class (initial guess)
case "$desktop_entry" in
    spotify|spotify.desktop) class="Spotify" ;;
    qutebrowser|qutebrowser.desktop) class="org.qutebrowser.qutebrowser" ;;
    firefox|firefox.desktop|firefox.*) class="firefox" ;;
    chromium|chromium.*|google-chrome|google-chrome.desktop) class="chromium" ;;
    brave|brave-browser|brave-browser.desktop) class="Brave-browser" ;;
    mpv|mpv.desktop) class="mpv" ;;
    youtube-music|youtube-music.desktop) class="com.github.th_ch.youtube_music" ;;
    *) class="$desktop_entry" ;;  # fallback
esac

# Step 4: Focus the window based on priority
# 1. YouTube Music
win=$(hyprctl clients -j | jq -r '.[] | select(.class=="com.github.th_ch.youtube_music") | .address' | head -n1)
if [ -n "$win" ]; then
    hyprctl dispatch focuswindow address:"$win"
    exit 0
fi

# 2. qutebrowser
win=$(hyprctl clients -j | jq -r '.[] | select(.class=="org.qutebrowser.qutebrowser") | .address' | head -n1)
if [ -n "$win" ]; then
    hyprctl dispatch focuswindow address:"$win"
    exit 0
fi

# 3. firefox
win=$(hyprctl clients -j | jq -r '.[] | select(.class=="firefox") | .address' | head -n1)
if [ -n "$win" ]; then
    hyprctl dispatch focuswindow address:"$win"
    exit 0
fi

# 4. chromium / Google Chrome
win=$(hyprctl clients -j | jq -r '.[] | select(.class=="chromium" or .class=="google-chrome") | .address' | head -n1)
if [ -n "$win" ]; then
    hyprctl dispatch focuswindow address:"$win"
    exit 0
fi

# Step 5: Fallback to any matching class from metadata
win=$(hyprctl clients -j | jq -r \
    --arg class "$class" \
    '.[] | select(.class == $class) | .address' | head -n1)

if [ -z "$win" ]; then
    notify-send "Could not find window for $player (desktop-entry: $desktop_entry, class: $class)"
    exit 1
fi

hyprctl dispatch focuswindow address:"$win"

