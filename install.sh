#!/bin/bash

echo "=== Wifi Radar installer for Termux ==="

echo "[1/5] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[2/5] Downloading dependencies (python, termux-api, git)..."
pkg install python termux-api git -y

echo "[3/5] installing Flask..."
pip install flask

echo "[4/5] Downloading code from Github..."
git clone https://github.com/6dQ2fX5g/termux-wifi-radar.git ~/termux-wifi-radar

echo "[5/5] Creating direct access 'wifi-radar'..."
echo "alias wifi-radar='python ~/termux-wifi-radar/wifi_radar.py'" >> ~/.bashrc
source ~/.bashrc

echo ""
echo "=== Installation complete! ==="
echo "Close and reopen Termux."
echo "After that, simply write 'wifi-radar' to start the program."
echo "Remember giving Termux and Termux API location access."
