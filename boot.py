import network
import socket
import machine
import time
import ujson

# Wi-Fi credentials
WIFI_SSID = "wlanssidname"
WIFI_PASSWORD = "wlanpassword"

# GPS UART setup (TX=16, RX=17)
uart = machine.UART(2, baudrate=9600, tx=16, rx=17,  timeout=5000)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to Wi-Fi", end="")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")

    print("\nConnected! IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# Read GPS data
def read_gps():
    while uart.any():
        gps_raw = uart.readline()
        try:
            gps_data = gps_raw.decode('utf-8')
            if "$GPGGA" in gps_data:
                gps_parts = gps_data.split(",")
                lat_raw = gps_parts[2]
                lon_raw = gps_parts[4]

                # Convert NMEA format to decimal degrees
                lat = float(lat_raw[:2]) + float(lat_raw[2:]) / 60
                lon = float(lon_raw[:3]) + float(lon_raw[3:]) / 60

                if gps_parts[3] == "S":
                    lat = -lat
                if gps_parts[5] == "W":
                    lon = -lon

                return lat, lon
        except:
            pass
    return None, None

# Create a simple web server
def start_server():
    addr = ("0.0.0.0", 80)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen(5)
    print("Web server running on port 80...")

    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()

        if "GET /gps" in request:
            lat, lon = read_gps()
            response = ujson.dumps({"lat": lat, "lon": lon})
            conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + response)

        else:
            response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
    <title>ESP32 GPS Tracker</title>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script>
        function initMap() {
            var map = L.map('map').setView([0, 0], 15);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap'
            }).addTo(map);
            var marker = L.marker([0, 0]).addTo(map);

            function refreshGPS() {
                fetch('/gps').then(response => response.json()).then(data => {
                    var lat = parseFloat(data.lat);
                    var lon = parseFloat(data.lon);
                    if (!isNaN(lat) && !isNaN(lon)) {
                        map.setView([lat, lon], 15);
                        marker.setLatLng([lat, lon]);
                        document.getElementById('gps-data').innerHTML = `Lat: ${lat}, Lng: ${lon}`;
                    }
                });
            }

            setInterval(refreshGPS, 3000);
        }
    </script>
</head>
<body onload="initMap()">
    <h1>ESP32 GPS Tracker</h1>
    <p id="gps-data">Waiting for GPS...</p>
    <div id="map" style="width:100%;height:400px;"></div>
</body>
</html>
"""
            conn.send(response)

        conn.close()

# Run the script
ip = connect_wifi()
start_server()
