import os
import json
import subprocess
import math
import time
from flask import Flask, jsonify, render_template

# Inicialitzem l'aplicació Flask
app = Flask(__name__, template_folder='.')

LOG_FILE = "scan_log.json"

def calculate_distance(rssi, tx_power=-50, n=2.5):
    """
    Estima la distància basant-se en la força del senyal (RSSI).
    És una ESTIMACIÓ i pot no ser precisa.
    rssi: Signal strength in dBm.
    tx_power: The signal strength at 1 meter. Valor típic entre -40 i -60.
    n: Path-loss exponent. Varia segons l'entorn (2 a camp obert, 4 a través de parets).
    """
    try:
        # Fórmula de pèrdua de senyal en logaritmes
        distance = 10 ** ((tx_power - rssi) / (10 * n))
        return round(distance, 2)
    except Exception:
        return -1 # Retorna -1 si hi ha un error

def get_wifi_scan():
    """
    Executa l'escaneig de WiFi a través de Termux:API i processa les dades.
    """
    try:
        # Important: Android requereix permisos de localització per escanejar WiFi.
        # Assegura't que Termux i Termux:API els tenen.
        scan_output = subprocess.check_output("termux-wifi-scaninfo", shell=True)
        networks = json.loads(scan_output)
        
        processed_networks = []
        for net in networks:
            distance = calculate_distance(net['rssi'])
            processed_networks.append({
                'ssid': net['ssid'],
                'bssid': net['bssid'],
                'rssi': net['rssi'],
                'frequency': net['frequency_mhz'],
                'distance_m': distance
            })
        
        # Ordenem per distància estimada
        processed_networks.sort(key=lambda x: x['distance_m'])
        return processed_networks

    except subprocess.CalledProcessError:
        print("Error: No s'ha pogut executar termux-wifi-scaninfo. Assegura't que Termux:API està instal·lat i els permisos correctes.")
        return None
    except json.JSONDecodeError:
        print("Error: La sortida de termux-wifi-scaninfo no és un JSON vàlid.")
        return None

def log_scan(scan_data):
    """
    Guarda les dades de l'escaneig a l'arxiu de log (Intel Timeline).
    """
    log_entry = {
        'timestamp': int(time.time()),
        'scan': scan_data
    }
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"No s'ha pogut escriure al log: {e}")


# Variable global per guardar l'últim escaneig a memòria
latest_scan_data = []

# --- Rutes de l'API ---

@app.route('/')
def index():
    """Serveix la pàgina HTML principal."""
    return render_template('index.html')

@app.route('/api/scan')
def api_scan():
    """Retorna l'últim escaneig en format JSON."""
    global latest_scan_data
    return jsonify(latest_scan_data)

@app.route('/api/history')
def api_history():
    """Retorna tot l'historial d'escanejos."""
    history = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                history.append(json.loads(line))
    return jsonify(history)


def background_scanner():
    """
    Funció que s'executa en segon pla per escanejar contínuament.
    """
    global latest_scan_data
    print("Iniciant escàner en segon pla...")
    while True:
        scan_data = get_wifi_scan()
        if scan_data:
            latest_scan_data = scan_data
            log_scan(scan_data)
            print(f"Escaneig completat. Trobat(s) {len(scan_data)} xarxa(es).")
        else:
            print("Escaneig fallit.")
        time.sleep(5) # Espera 5 segons entre escanejos

if __name__ == '__main__':
    # Creem un fil per a l'escàner per no bloquejar el servidor web
    import threading
    scanner_thread = threading.Thread(target=background_scanner, daemon=True)
    scanner_thread.start()
    
    # Executem el servidor web, accessible des de qualsevol IP de la xarxa local
    print("Servidor web iniciat a http://0.0.0.0:8000")
    print("Obre el navegador del teu mòbil a http://localhost:8000")
    app.run(host='0.0.0.0', port=8000)
