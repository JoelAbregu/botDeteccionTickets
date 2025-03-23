import pywhatkit as kit
import pyautogui
import time

numero = "+51908897808"
mensaje = "¡Hola! Este es un mensaje automático desde WhatsApp Web."

# Enviar mensaje
kit.sendwhatmsg_instantly(numero, mensaje)

# Esperar unos segundos para que se abra la pestaña
time.sleep(10)  

# Cerrar la pestaña con el atajo de teclado (Ctrl + W en Windows)
pyautogui.hotkey("ctrl", "w")  

print("✅ Pestaña de WhatsApp Web cerrada automáticamente.")
