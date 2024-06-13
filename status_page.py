import tkinter as tk
import paho.mqtt.client as mqtt
from tkinter.simpledialog import askstring

class StatusPage(tk.Frame):
    def __init__(self, parent, mqtt_client):
        super().__init__(parent, bg='black')
        self.parent = parent
        self.mqtt_client = mqtt_client

        self.status_label = tk.Label(self, text="Status da Conexão", font=("Arial", 24), bg='black', fg='white')
        self.status_label.pack(pady=20)

        self.wifi_label = tk.Label(self, text="Status da Conexão Wi-Fi: ", font=("Arial", 18), bg='black', fg='white')
        self.wifi_label.pack(pady=10)

        self.mqtt_label = tk.Label(self, text="Status da Conexão MQTT: Conectado", font=("Arial", 18), bg='black', fg='white')
        self.mqtt_label.pack(pady=10)

        self.set_wifi_button = tk.Button(self, text="Definir Wi-Fi", command=self.definir_wifi, bg='gray', fg='white', font=("Arial", 12))
        self.set_wifi_button.pack(pady=10)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.atualizar_status, bg='gray', fg='white', font=("Arial", 12))
        self.refresh_button.pack(pady=10)

        self.mqtt_client.subscribe("empresa/wifi")
        self.mqtt_client.message_callback_add("empresa/wifi", self.on_wifi_message)

        self.atualizar_status()

    def on_wifi_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            self.wifi_label.config(text=f"Status da Conexão Wi-Fi: {payload}")
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def definir_wifi(self):
        novo_ssid = askstring("Definir Wi-Fi", "Digite o novo SSID:")
        nova_senha = askstring("Definir Wi-Fi", "Digite a nova senha:")
        if novo_ssid and nova_senha:
            self.mqtt_client.publish("empresa/cmd", f"SET WIFI \"{novo_ssid}\" \"{nova_senha}\"")

    def atualizar_status(self):
        self.mqtt_client.publish("empresa/cmd", "GET WIFI")
