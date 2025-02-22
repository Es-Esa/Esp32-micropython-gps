📍 ESP32 GPS Tracker with Web Interface

This project turns an ESP32-WROOM-32D into a GPS tracker that connects to Wi-Fi, reads data from a NEO-6M GPS module, and displays the location on a webpage using OpenStreetMap.
This project will later come a part of an autonomus anchor for my boat motor.

📌 Features

✅ Connects ESP32 to Wi-Fi

✅ Reads GPS coordinates (latitude, longitude)

✅ Serves a webpage displaying GPS location on OpenStreetMap

✅ Updates every 3 seconds

🛠️ Required Hardware

ESP32-WROOM-32D

NEO-6M GPS Module

Jumper wires

🔹 Step 1: Flash MicroPython on ESP32

📌 Install esptool.py (Python-based flashing tool)

pip install esptool

📌 Erase ESP32 Flash Memory

Connect ESP32 to USB and run:

esptool.py --port COM11 erase_flash

(Replace COM11 with your actual ESP32 port)

📌 Flash MicroPython Firmware

Download the latest MicroPython firmware for ESP32 from micropython.org. Then flash it:

esptool.py --port COM11 --baud 460800 write_flash --flash_size=detect 0 firmware.bin

🔹 Step 2: Install ampy for File Transfers

Install the correct ampy package for transferring files to ESP32:

pip install adafruit-ampy

Test if ampy works:

ampy --help

If ampy is not found, try:

python -m ampy --help

🔹 Step 3: Connect GPS Module to ESP32

📌 Wiring Diagram

GPS Module (NEO-6M)

ESP32 Pin

VCC

VIN (5V)

GND

GND

TX (GPS Output)

GPIO17 (ESP32 RX)

RX (GPS Input)

GPIO16 (ESP32 TX)

PPS (Optional)

Not needed

If no GPS data appears, try swapping TX and RX!

🔹 Step 4: Upload boot.py to ESP32

📌 Upload boot.py to ESP32

ampy --port COM11 put boot.py

Restart ESP32:

ampy --port COM11 reset

🔹 Step 5: Access the Web Interface

Find ESP32’s IP Address

Open a serial monitor (e.g., Putty, screen, or minicom)

Run: mode COM11:115200

ESP32 will print its IP Address (e.g., 192.168.1.42)

Open a Browser and Visit:

http://192.168.1.42

(Replace 192.168.1.42 with your actual ESP32 IP)

You should see GPS coordinates on OpenStreetMap! 🎉


