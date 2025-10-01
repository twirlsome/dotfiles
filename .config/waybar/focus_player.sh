#!/usr/bin/env bash
set -euo pipefail

# Step 1: Find the first actively playing player
player=""
while read -r p; do
    if playerctl -p "$p" status 2>/dev/null | grep -qi "Playing"; then
        player="$p"
        break
    fi
done < <(playerctl -l)

if [ -z "$player" ]; then
    notify-send "No active media player"
    exit 0
fi

# Step 2: Try to get desktop-entry, fallback to player name
desktop_entry=$(playerctl -p "$player" metadata xesam:desktop-entry 2>/dev/null || true)
class="${desktop_entry:-$player}"

# Step 3: Priority order (Hyprland window classes)
priorities=(
    "com.github.th_ch.youtube_music"
    "org.qutebrowser.qutebrowser"
    "firefox"
    "chromium"
    "google-chrome"
)

# Step 4: Search by priority
for prio in "${priorities[@]}"; do
    win=$(hyprctl clients -j | jq -r --arg c "$prio" \
        '.[] | select((.class|ascii_downcase)==($c|ascii_downcase)) | .address' | head -n1)
    if [ -n "$win" ]; then
        hyprctl dispatch focuswindow address:"$win"
        exit 0
    fi
done

# Step 5: Fallback to metadata class
win=$(hyprctl clients -j | jq -r --arg c "$class" \
    '.[] | select((.class|ascii_downcase)==($c|ascii_downcase)) | .address' | head -n1)

if [ -z "$win" ]; then
    notify-send "Could not find window for $player (desktop-entry: $desktop_entry, class: $class)"
    exit 1
fi

hyprctl dispatch focuswindow address:"$win"

