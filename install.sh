#!/bin/bash

echo "=== Instal·lador de WiFi Radar per a Termux ==="

# Actualitzar paquets
echo "[1/5] Actualitzant paquets..."
pkg update -y && pkg upgrade -y

# Instal·lar dependències
echo "[2/5] Instal·lant dependències (python, termux-api, git)..."
pkg install python termux-api git -y

# Instal·lar Flask
echo "[3/5] Instal·lant Flask..."
pip install flask

# Clonar el repositori
echo "[4/5] Descarregant el codi font des de GitHub..."
git clone https://github.com/el-teu-nom/termux-wifi-radar.git ~/termux-wifi-radar

# Crear un àlies per executar fàcilment
echo "[5/5] Creant un accés directe 'wifi-radar'..."
echo "alias wifi-radar='python ~/termux-wifi-radar/wifi_radar.py'" >> ~/.bashrc
source ~/.bashrc

echo ""
echo "=== Instal·lació completada! ==="
echo "Tanca i torna a obrir Termux."
echo "Després, simplement escriu 'wifi-radar' per iniciar el programa."
echo "Recorda donar permisos de localització a Termux i Termux:API."
