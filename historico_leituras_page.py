#historico_leituras_page

import tkinter as tk
import paho.mqtt.client as mqtt
import datetime

class HistoricoLeiturasPage(tk.Frame):
    def __init__(self, parent, mqtt_client):
        super().__init__(parent, bg='black')
        self.parent = parent
        self.mqtt_client = mqtt_client

        self.label = tk.Label(self, text="Histórico de Leituras", font=("Arial", 24), bg='black', fg='white')
        self.label.pack(pady=20)

        self.leituras_list = tk.Listbox(self, bg='black', fg='white', font=("Arial", 12), width=50, height=20)
        self.leituras_list.pack(pady=10)

        self.mqtt_client.subscribe("empresa/autorizado")
        self.mqtt_client.subscribe("empresa/negado")
        self.mqtt_client.message_callback_add("empresa/autorizado", self.on_message)
        self.mqtt_client.message_callback_add("empresa/negado", self.on_message)

    def on_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode('utf-8')
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            interaction_message = f"{current_time}: {msg.topic} - {message}"
            self.leituras_list.insert(tk.END, interaction_message)
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

