import tkinter as tk
import paho.mqtt.client as mqtt
import datetime

class MonitoramentoPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='black')  # Definindo a cor de fundo como preto
        self.parent = parent

        # Criando um frame para conter o cartão e os elementos abaixo dele
        content_frame = tk.Frame(self, bg='black')
        content_frame.pack(side='left', padx=20, pady=15)  # Posicionando o frame à esquerda

        # Adicionando o cartão ao frame de conteúdo
        self.card = tk.Label(content_frame, text="Funcionário 1", bg='red', width=30, height=10, font=("Arial", 18), fg='white')
        self.card.pack(side='top', padx=20, pady=15)  # Posicionando o cartão acima dos outros elementos

        # Adicionando o título "Histórico de Leituras" ao frame de conteúdo
        self.interactions_label = tk.Label(content_frame, text="Histórico de Leituras", bg='black', fg='white', font=("Arial", 14))
        self.interactions_label.pack(side='top', padx=20, pady=5)  # Posicionando o título acima da lista

        # Adicionando a lista de interações ao frame de conteúdo
        self.interactions_list = tk.Listbox(content_frame, bg='black', fg='white', font=("Arial", 12), width=50, height=10)
        self.interactions_list.pack(side='top', padx=20, pady=5)  # Posicionando a lista abaixo do título

        # Configurando o cliente MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("broker.hivemq.com", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("empresa/autorizado")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        valor = int(msg.payload)

        # Determinando a mensagem com base no valor recebido do tópico MQTT
        if valor == 1:
            message = "Cartão autorizado lido"
            bg_color = 'green'
        else:
            message = "Nenhuma leitura de cartão"
            bg_color = 'red'

        # Obtendo o horário atual
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Concatenando o horário e a mensagem em uma única string
        interaction_message = f"{current_time}: {message}"

        # Adicionando a interação à lista
        self.interactions_list.insert(tk.END, interaction_message)

        # Atualizando a cor do cartão
        self.card.config(bg=bg_color)
