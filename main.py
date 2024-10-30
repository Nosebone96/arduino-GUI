import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import random  # Solo para simular datos, eliminar en la versión final

class ArduinoSensorDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard de Sensores Arduino")
        self.master.geometry("800x600")
        
        self.style = ttkb.Style(theme="darkly")
        
        self.create_widgets()
        
        self.is_connected = False
        self.serial_port = None
        
        # Datos para la gráfica
        self.max_points = 100
        self.temperatures = deque(maxlen=self.max_points)
        self.light_levels = deque(maxlen=self.max_points)
        self.sound_levels = deque(maxlen=self.max_points)

        
        self.update_graph()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Dashboard de Sensores", font=("Helvetica", 24))
        title_label.pack(pady=10)
        
        # Frame para los datos de los sensores
        sensor_frame = ttk.Frame(main_frame)
        sensor_frame.pack(fill=tk.X, pady=10)
        
        # Etiquetas para los datos de los sensores
        self.temp_label = self.create_sensor_label(sensor_frame, "Temperatura:", 0)
        self.light_label = self.create_sensor_label(sensor_frame, "Luz:", 1)
        self.sound_label = self.create_sensor_label(sensor_frame, "Sonido:", 2)
        
        # Botón de conexión
        self.connect_button = ttk.Button(main_frame, text="Conectar", command=self.connect_bluetooth, style="success.TButton")
        self.connect_button.pack(pady=10)
        
        # Frame para la gráfica
        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear la gráfica
        self.fig, self.ax = plt.subplots(figsize=(10, 4), facecolor='#2c3e50')
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar la gráfica
        self.ax.set_facecolor('#2c3e50')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.set_title('Datos de los Sensores en Tiempo Real', color='white')
        self.ax.set_xlabel('Tiempo', color='white')
        self.ax.set_ylabel('Valor', color='white')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Líneas para cada sensor
        self.temp_line, = self.ax.plot([], [], label='Temperatura', color='#e74c3c')
        self.light_line, = self.ax.plot([], [], label='Luz', color='#f1c40f')
        self.sound_line, = self.ax.plot([], [], label='Sonido', color='#2ecc71')
        
        self.ax.legend(loc='upper left')

    def create_sensor_label(self, parent, text, column):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=column, padx=10)
        
        label = ttk.Label(frame, text=text, font=("Helvetica", 14))
        label.pack()
        
        value_label = ttk.Label(frame, text="--", font=("Helvetica", 18, "bold"))
        value_label.pack()
        
        return value_label

    def connect_bluetooth(self):
        if self.is_connected: #aquí había un" not self.is_connected"
            try:
                # Ajusta 'COM3' al puerto correcto de tu dispositivo Bluetooth
                self.serial_port = serial.Serial('COM3', 9600, timeout=1)
                self.is_connected = True
                self.connect_button.config(text="Desconectar", style="danger.TButton")
                threading.Thread(target=self.read_data, daemon=True).start()
            except serial.SerialException:
                threading.Thread(target=self.read_data, daemon=True).start()
                self.temp_label.config(text="Error de conexión")
        else:
            self.serial_port.close()
            self.is_connected = False
            self.connect_button.config(text="Conectar", style="success.TButton")
            self.temp_label.config(text="--")
            self.light_label.config(text="--")
            self.sound_label.config(text="--")

    def read_data(self):
        print('si')
        while self.is_connected:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode('utf-8').strip()
                self.master.after(0, self.update_gui, data)
            else:
                # Simular datos (eliminar en la versión final)
                self.master.after(0, self.update_gui, f"{random.randint(20, 30)},{random.randint(0, 1000)},{random.randint(0, 100)}")
                self.master.after(100)  # Simular delay
        if not self.is_connected:
            print('no')
            while not self.is_connected:
                self.master.after(0, self.update_gui, f"{random.randint(20, 30)},{random.randint(0, 1000)},{random.randint(0, 100)}")
                self.master.after(2000)
                self.master.after(100, self.update_graph)
                print('inventa datos')


    def update_gui(self, data):
        print('update')
        try:
            temp, light, sound = map(float, data.split(','))
            self.temp_label.config(text=f"{temp:.1f}°C")
            self.light_label.config(text=f"{light:.0f} lux")
            self.sound_label.config(text=f"{sound:.0f} dB")
            
            self.temperatures.append(temp)
            self.light_levels.append(light)
            self.sound_levels.append(sound)
        except ValueError:
            print(f"Datos inválidos recibidos: {data}")

    def update_graph(self):
        print('grafica')
        self.temp_line.set_data(range(len(self.temperatures)), self.temperatures)
        self.light_line.set_data(range(len(self.light_levels)), self.light_levels)
        self.sound_line.set_data(range(len(self.sound_levels)), self.sound_levels)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        
if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = ArduinoSensorDashboard(root)
    root.mainloop()