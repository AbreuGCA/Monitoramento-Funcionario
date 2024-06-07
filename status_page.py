# status_page.py

import tkinter as tk
import socket
import paho.mqtt.client as mqtt
import platform
import subprocess

class StatusPage(tk.Frame):
    def __init__(self, parent, mqtt_client):
        super().__init__(parent, bg='black')  # Definindo a cor de fundo como preto
        self.parent = parent
        self.mqtt_client = mqtt_client

        self.status_label = tk.Label(self, text="Status da Conexão", font=("Arial", 24), bg='black', fg='white')
        self.status_label.pack(pady=20)

        self.wifi_label = tk.Label(self, text="Status da Conexão Wi-Fi: ", font=("Arial", 18), bg='black', fg='white')
        self.wifi_label.pack(pady=10)

        self.mqtt_label = tk.Label(self, text="Status da Conexão MQTT: ", font=("Arial", 18), bg='black', fg='white')
        self.mqtt_label.pack(pady=10)

        self.update_status()

    def update_status(self):
        # Obtendo o nome do Wi-Fi (em sistemas Unix, geralmente é wlan0 ou eth0)
        wifi_name = self.get_wifi_name()
        self.wifi_label.config(text=f"Status da Conexão Wi-Fi: {wifi_name}")

        # Obtendo o nome do cliente MQTT e seu status
        mqtt_client_name = socket.gethostname()
        mqtt_status = "Conectado" if self.mqtt_client.is_connected() else "Desconectado"
        self.mqtt_label.config(text=f"Status da Conexão MQTT: {mqtt_client_name} ({mqtt_status})")

        # Atualizando o status a cada 5 segundos
        self.after(5000, self.update_status)

    def get_wifi_name(self):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if "SSID" in line:
                        wifi_name = line.split(":")[1].strip()
                        return wifi_name if wifi_name else "Não Conectado"
            else:
                result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
                wifi_name = result.stdout.strip()
                return wifi_name if wifi_name else "Não Conectado"
        except Exception as e:
            return f"Erro: {e}"

