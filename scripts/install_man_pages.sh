#!/bin/bash

# Define the source directory and the destination directory for man pages
MAN_SRC_DIR="$(pwd)/man"
MAN_DST_DIR="/usr/local/share/man/man1"

# Check if the destination directory exists
if [ ! -d "$MAN_DST_DIR" ]; then
    echo "Creating man1 directory..."
    sudo mkdir -p "$MAN_DST_DIR"
fi

# Copy man pages to the destination directory
echo "Copying man pages to $MAN_DST_DIR..."
for man_page in "$MAN_SRC_DIR"/*; do
    sudo cp "$man_page" "$MAN_DST_DIR/"
done

# Update the man database
echo "Updating the man database..."
sudo mandb

echo "Man pages installed and database updated."

