import tkinter as tk
import paho.mqtt.client as mqtt
from tkinter.simpledialog import askstring

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

        self.set_wifi_button = tk.Button(self, text="Definir Wi-Fi", command=self.definir_wifi, bg='gray', fg='white', font=("Arial", 12))
        self.set_wifi_button.pack(pady=10)

        # Subscrever aos tópicos relevantes
        self.mqtt_client.subscribe("empresa/wifi")
        self.mqtt_client.subscribe("empresa/cmd")
        self.mqtt_client.on_message = self.on_message

        # Obter o status atual
        self.atualizar_status()

    def on_message(self, client, userdata, msg):
        # Lidar com mensagens recebidas dos tópicos MQTT
        if msg.topic == "empresa/wifi":
            # Atualizar o status da conexão Wi-Fi
            self.wifi_label.config(text=f"Status da Conexão Wi-Fi: {msg.payload.decode()}")
        elif msg.topic == "empresa/cmd":
            # Lidar com comandos recebidos
            self.handle_command(msg.payload.decode())

    def handle_command(self, command):
        # Lidar com os comandos recebidos via MQTT
        if command == "GET WIFI":
            # Enviar uma solicitação para obter as informações de Wi-Fi
            self.mqtt_client.publish("empresa/cmd", "GET WIFI")
        elif command.startswith("SET WIFI"):
            # Extrair o novo SSID e senha do comando
            ssid_password = command.split('"')[1:3]
            if len(ssid_password) == 2:
                novo_ssid, nova_senha = ssid_password
                # Atualizar a interface com as novas informações de Wi-Fi
                self.wifi_label.config(text=f"Status da Conexão Wi-Fi: SSID: {novo_ssid}, Senha: {nova_senha}")
        else:
            # Comando desconhecido
            print("Comando desconhecido:", command)

    def definir_wifi(self):
        novo_ssid = askstring("Definir Wi-Fi", "Digite o novo SSID:")
        nova_senha = askstring("Definir Wi-Fi", "Digite a nova senha:")
        if novo_ssid is not None and nova_senha is not None:
            # Publicar o novo SSID e senha no tópico MQTT para configurar o dispositivo
            self.mqtt_client.publish("empresa/cmd", f"SET WIFI \"{novo_ssid}\" \"{nova_senha}\"")

    def atualizar_status(self):
        # Publicar uma solicitação para obter o status da conexão Wi-Fi
        self.mqtt_client.publish("empresa/cmd", "GET WIFI")
