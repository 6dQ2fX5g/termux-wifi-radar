# WiFi Radar HUD for Termux

An offline, local WiFi scanner and radar HUD for Termux. This tool leverages the `termux-api` to scan for WiFi networks in real-time and visualizes them on a stylish, blue-themed radar interface served locally on your device.

## ✨ Features

-   **Live WiFi Scanning:** Detects all nearby WiFi networks.
-   **Distance Estimation:** Provides an approximate distance in meters to each network based on signal strength (RSSI).
-   **HUD Radar Visualization:** Displays detected networks on a satellite-style radar, plotting them based on their estimated distance.
-   **Intel Timeline:** Automatically logs every scan with a timestamp for later analysis. All data is saved locally.
-   **Fully Offline & Local:** No internet connection required. The server runs on your device, and all data stays on your device.
-   **Web Interface:** Access the radar and data list through your mobile browser.
-   **One-Command Install:** A simple installation script to get you up and running in minutes.

---

## 📋 Requirements

-   An Android device.
-   [Termux](https://f-droid.org/en/packages/com.termux/) app installed.
-   [Termux:API](https://f-droid.org/en/packages/com.termux.api/) app installed from F-Droid.
-   **Location Permissions** must be granted to both Termux and Termux:API apps for WiFi scanning to work.

---

## 🚀 Installation

Open Termux and paste the following command. It will automatically install all dependencies, download the source code, and create a convenient `wifi-radar` command.

```bash
curl -sL https://raw.githubusercontent.com/el-teu-nom/termux-wifi-radar/main/install.sh | bash
```

---

## ⚡ Usage

1.  After installation, **close and reopen Termux**.
2.  Run the tool by simply typing:
    ```bash
    wifi-radar
    ```
3.  The script will start the web server. Open your mobile's web browser and navigate to:
    ```
    http://localhost:8000
    ```
4.  You should now see the WiFi Radar HUD in action!

---

## 🔧 How It Works

-   **Backend:** A Python script using the **Flask** micro-framework runs a local web server inside Termux.
-   **Scanning:** A background thread periodically calls `termux-wifi-scaninfo` to get raw JSON data of nearby networks.
-   **Data Processing:** The script calculates the estimated distance for each network and saves the scan results to a local `scan_log.json` file.
-   **Frontend:** A single `index.html` file with vanilla JavaScript fetches the latest scan data from the Flask API every few seconds and dynamically draws the networks on an HTML5 Canvas element.

## ⚠️ Disclaimer

-   The **distance calculation is an estimation** based on RSSI (signal strength) and is not perfectly accurate. Environmental factors like walls and interference can significantly affect the results.
-   The radar visualizes **distance, not direction**. Since a single device cannot determine the angle of a WiFi signal, the radar distributes the networks around the circle for visualization purposes only. Their angular position on the radar is not their real-world physical position.
