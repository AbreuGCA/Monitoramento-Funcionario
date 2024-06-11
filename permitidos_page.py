import tkinter as tk
import paho.mqtt.client as mqtt
from tkinter.simpledialog import askstring

class PermitidosPage(tk.Frame):
    def __init__(self, parent, mqtt_client):
        super().__init__(parent, bg='black')  # Definindo a cor de fundo como preto
        self.parent = parent
        self.mqtt_client = mqtt_client  # Atribuindo o cliente MQTT recebido como argumento

        content_frame = tk.Frame(self, bg='black')
        content_frame.pack(padx=20, pady=15)  # Posicionando o frame

        self.permitidos_label = tk.Label(content_frame, text="IDs Permitidos", bg='black', fg='white', font=("Arial", 18))
        self.permitidos_label.pack(side='top', padx=20, pady=10)  # Posicionando o título acima da lista

        self.permitidos_list = tk.Listbox(content_frame, bg='black', fg='white', font=("Arial", 12), width=50, height=10)
        self.permitidos_list.pack(side='top', padx=20, pady=5)  # Posicionando a lista abaixo do título

        # Botões para adicionar e remover IDs
        self.adicionar_button = tk.Button(content_frame, text="Adicionar ID", command=self.adicionar_id, bg='gray', fg='white', font=("Arial", 12))
        self.adicionar_button.pack(side='left', padx=10, pady=5)

        self.remover_button = tk.Button(content_frame, text="Remover ID", command=self.remover_id, bg='gray', fg='white', font=("Arial", 12))
        self.remover_button.pack(side='left', padx=10, pady=5)

        # Enviar comando MQTT para obter a lista de IDs permitidos
        self.mqtt_client.publish("empresa/cmd", "LIST IDS")
        self.mqtt_client.subscribe("empresa/ids")
        self.mqtt_client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        # Verificar se a mensagem recebida é do tópico "empresa/ids" e atualizar a lista de IDs permitidos
        if msg.topic == "empresa/ids":
            ids = msg.payload.decode("utf-8").split(", ")
            self.permitidos_list.delete(0, tk.END)  # Limpa a lista atual
            for id in ids:
                self.permitidos_list.insert(tk.END, id)

    def adicionar_id(self):
        novo_id = askstring("Adicionar ID", "Digite o ID que deseja adicionar:")
        if novo_id is not None:
            # Adicionar o ID à lista na interface gráfica
            self.permitidos_list.insert(tk.END, novo_id)
            # Publicar o novo ID no tópico MQTT "empresa/cmd" para atualizar o ESP32
            self.mqtt_client.publish("empresa/cmd", f"ADD ID {novo_id}")

    def remover_id(self):
        index = self.permitidos_list.curselection()
        if index:
            id_remover = self.permitidos_list.get(index)
            # Remover o ID da lista na interface gráfica
            self.permitidos_list.delete(index)
            # Publicar o ID a ser removido no tópico MQTT "empresa/cmd" para atualizar o ESP32
            self.mqtt_client.publish("empresa/cmd", f"DELETE ID {id_remover}")
