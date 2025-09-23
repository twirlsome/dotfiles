#!/bin/bash

# Define destination
DST="$HOME/repos/dotfiles/.config"

# List of config folders to sync
declare -a CONFIGS=(
    "waybar"
    "nvim"
    "kitty"
    "hypr"
    "wofi"
    "cava"
    "qutebrowser"
)

echo "Syncing selected config files..."

for name in "${CONFIGS[@]}"; do
    SRC="$HOME/.config/$name"
    DEST="$DST/$name"

    echo "→ $name"
    rm -rf "$DEST"              # Remove previous copy
    cp -r "$SRC" "$DEST"        # Copy fresh version
done

echo "Done. You may now commit your changes with Git."

