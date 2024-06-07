# main.py

import tkinter as tk
from status_page import StatusPage
from monitoramento_page import MonitoramentoPage
import paho.mqtt.client as mqtt

def show_monitoramento():
    monitoramento_frame.grid(row=1, column=0, sticky='nsew')
    status_frame.grid_forget()

def show_status():
    status_frame.grid(row=1, column=0, sticky='nsew')
    monitoramento_frame.grid_forget()

def sair():
    root.quit()

root = tk.Tk()
root.title("Atividade de Leitura de Cartões")
root.configure(bg='black')
root.attributes('-fullscreen', True)

navbar = tk.Frame(root, bg='gray', padx=20, pady=20)
navbar.grid(row=0, column=0, sticky='ew')
root.grid_columnconfigure(0, weight=1)

monitoramento_button = tk.Button(navbar, text="Monitoramento Cartões", command=show_monitoramento, bg='gray', fg='white', font=("Arial", 14, "bold"))
monitoramento_button.pack(side='left', padx=10, pady=5)

status_button = tk.Button(navbar, text="Status", command=show_status, bg='gray', fg='white', font=("Arial", 14, "bold"))
status_button.pack(side='left', padx=10, pady=5)

sair_button = tk.Button(navbar, text="Sair", command=sair, bg='gray', fg='white', font=("Arial", 14, "bold"))
sair_button.pack(side='right', padx=10, pady=5)

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

status_frame = StatusPage(root, client)
monitoramento_frame = MonitoramentoPage(root)

root.client = client  # Passando o cliente MQTT para a janela principal

show_monitoramento()  # Exibindo a página de monitoramento inicialmente

root.mainloop()
