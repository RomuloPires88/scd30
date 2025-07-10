import time
import board
import adafruit_scd30
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import messagebox

# Sensor setup
i2c = board.I2C()
scd = adafruit_scd30.SCD30(i2c)

#Lists to store time and CO2 values
time_values = []
co2_values = []
start_time = time.time()
marker_time = None
collecting = True
running = True

def on_key_press(event):
	if event.key == ' ':
		marker_event(event)

def marker_event(event):
	global marker_time
	marker_time = time.time() - start_time
	print(f"Initial time difined at {marker_time:.2f} seconds")
	
def restart_reading_event(event):
	global collecting, time_values, co2_values, start_time, marker_time
	collecting = True
	time_values.clear()
	co2_values.clear()
	start_time = time.time()
	marker_time = None
	ax.clear()
	ax.set_title('CO2 vs Time')
	ax.set_xlabel('Time (s)')
	print("Data collection restarted and graph reset")
	
def stop_reading_event(event):
	global collecting
	collecting = False
	print("Data collection stopped")
	
def save_event(event):
    if marker_time is None:
        messagebox.showwarning("Initial Time not set", "Please press 'Initial Time' before saving the data.")
        print("Initial Time not set", "Please press 'Initial Time' before saving the data.")
        return

    save_directory = "/home/europi/Resultados"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    filename = f"CO2_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(save_directory, filename)

    try:
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'CO2 (ppm)', 'Temperature (ÂºC)', 'Humidity (%)'])
            for t, co2 in zip(time_values, co2_values):
                if t >= marker_time:
                    writer.writerow([t - marker_time, co2,temperature, humidity])
        messagebox.showinfo("Save Successful", f"Data saved to {file_path}")
        print(f"Data saved to {file_path}")
    except Exception as e:
        messagebox.showwarning("Error saving data", f"Error saving data: {e}")
        print(f"Error saving data: {e}")
		
def close_event(event):
	global running
	answer = messagebox.askyesno("Close Software", "Do you really want to close the software?")
	if answer:
		print("Closing the software")
		running = False
		plt.close()
		
# Button setup
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
fig.canvas.mpl_connect('key_press_event', on_key_press)

ax_marker = plt.axes([0.15,0.05,0.10,0.05])
btn_marker = Button(ax_marker, 'Initial Time', color = 'lightgray', hovercolor = 'lightblue')
btn_marker.on_clicked(marker_event)

ax_restart = plt.axes([0.30,0.05,0.10,0.05])
btn_restart = Button(ax_restart, 'Restart', color = 'lightgray', hovercolor = 'lightblue')
btn_restart.on_clicked(restart_reading_event)

ax_stop = plt.axes([0.45,0.05,0.10,0.05])
btn_stop = Button(ax_stop, 'Stop', color = 'lightgray', hovercolor = 'lightblue')
btn_stop.on_clicked(stop_reading_event)

ax_save = plt.axes([0.60,0.05,0.10,0.05])
btn_save = Button(ax_save, 'Save Results', color = 'lightgray', hovercolor = 'lightblue')
btn_save.on_clicked(save_event)

ax_close = plt.axes([0.75,0.05,0.10,0.05])
btn_close = Button(ax_close, 'Exit', color = 'lightgray', hovercolor = 'red')
btn_close.on_clicked(close_event)

# Resize
manager = plt.get_current_fig_manager()
try:
	manager.resize(1920,1080)
except Exception as e:
	print(f"Resize erro: {e}")
	
# Main loop
while running:
	if collecting and scd.data_available:
		elapsed_time = time.time() - start_time
		co2 = scd.CO2
		temperature = scd.temperature
		humidity = scd.relative_humidity
		
		time_values.append(elapsed_time)
		co2_values.append(co2)
		
		print(f"Time: {elapsed_time:.2f}s | CO2: {co2:.2f} ppm | Temp: {temperature:.1f}ÂºC | Hum: {humidity:.1f}%")
		
	ax.clear()
	ax.plot(time_values, co2_values, label = 'CO2 (ppm)')
	ax.set_xlabel('Time (s)')
	ax.set_ylabel('ppm')
	ax.set_title('CO2 vs Time')
	ax.text(0.95, 0.90, f"T: {temperature:.1f} ÂºC | H: {humidity:.1f} %",
			transform = ax.transAxes, ha = 'right', fontsize = 10,
			bbox = dict(boxstyle = "round", fc = "w"))
	if marker_time is not None:
		ax.axvline(marker_time, color = 'red', linestyle = '--', label = 'Initial Time')
	ax.legend()
	plt.pause(0.5)
