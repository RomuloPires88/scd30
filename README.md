# CO₂, Temperature and Humidity Monitor with SCD30 Sensor
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)


This Python project continuously monitors CO₂ levels, temperature, and humidity using the **Sensirion SCD30** sensor. It displays real-time graphs with matplotlib and allows saving collected data to CSV files.

---

## Features

- 🔴 Continuous reading of CO₂ (ppm), temperature (°C), and humidity (%)
- 📈 Real-time dynamic plotting, updated every 0.5 seconds
- 🧭 Marker button or **spacebar shortcut** to define an initial reference time
- ⏱️ Interactive buttons to:
  - ⏳ Set the initial time marker
  - 🔄 Restart data collection and clear the graph
  - ⏸️ Pause data collection
  - 💾 Save collected data from the marked time to CSV
  - ❌ Exit the program with confirmation
- ⚠️ Basic error handling and notifications via Tkinter message boxes

---

## Requirements

- Python 3.7+
- `adafruit-circuitpython-scd30` library
- `matplotlib` library
- `tkinter` (usually included with Python)
- Hardware: SCD30 sensor connected via I2C (e.g., Raspberry Pi with SCD30 sensor)

Install dependencies with:

```bash
pip install adafruit-circuitpython-scd30 matplotlib
