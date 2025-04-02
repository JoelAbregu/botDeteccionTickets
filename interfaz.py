import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext, Canvas
import threading
import bot  # Importamos las funciones de bot.py
import sys
import time

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Monitoreo de Tickets")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        self.style = ttk.Style("darkly")

        # 🎨 Fondo con degradado
        self.bg_color1 = "#191622"
        self.bg_color2 = "#282A36"
        self.create_gradient_background()

        # 📜 Consola
        self.log_area = scrolledtext.ScrolledText(
            root, width=80, height=15, state='disabled',
            bg="#2A2139", fg="#E1EFFF", font=("Cascadia Code", 11),
            insertbackground="#FF79C6", borderwidth=2, relief="flat"
        )
        self.log_area.pack(pady=10, padx=10, fill=BOTH, expand=True)
        self.log_area["yscrollcommand"] = lambda *args: None  # Ocultar scrollbar

        # 🔹 Botones
        self.create_buttons()

        # 🔹 Estado del bot
        self.bot_thread = None
        self.running = False  # Control de ejecución
        self.stop_event = threading.Event()  # Señal para detener el bot

        # Redirigir salida estándar a la interfaz
        sys.stdout = self

    def create_gradient_background(self):
        """ Crea un fondo con degradado oscuro """
        self.canvas_bg = Canvas(self.root, width=700, height=450, highlightthickness=0)
        self.canvas_bg.place(relwidth=1, relheight=1)

        for i in range(450):
            color = self._interpolate_color(self.bg_color1, self.bg_color2, i / 450)
            self.canvas_bg.create_line(0, i, 700, i, fill=color)

    def create_buttons(self):
        """ Crea los botones de Iniciar y Detener """
        button_frame = ttk.Frame(self.root, bootstyle="dark")
        button_frame.pack(pady=15)

        # 🎯 Botón "Iniciar Bot"
        self.start_btn = ttk.Button(
            button_frame, text="🚀 Iniciar Bot", bootstyle="success-outline",
            command=self.start_bot
        )
        self.start_btn.pack(side=LEFT, padx=10)

        # 🛑 Botón "Detener Bot"
        self.stop_btn = ttk.Button(
            button_frame, text="🛑 Detener Bot", bootstyle="danger-outline",
            command=self.stop_bot, state=DISABLED
        )
        self.stop_btn.pack(side=LEFT, padx=10)

    def _interpolate_color(self, color1, color2, t):
        """ Mezcla dos colores en base a t (0-1) """
        c1 = [int(color1[i:i + 2], 16) for i in (1, 3, 5)]
        c2 = [int(color2[i:i + 2], 16) for i in (1, 3, 5)]
        mix = [int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3)]
        return f"#{mix[0]:02x}{mix[1]:02x}{mix[2]:02x}"

    def start_bot(self):
        """ Inicia el bot en un hilo separado """
        if self.running:
            return

        self.clear_console()
        self.log("🚀 Iniciando el bot...")
        self.running = True
        self.stop_event.clear()  # Resetear evento de detención

        # Crear un nuevo hilo para el bot
        self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
        self.bot_thread.start()

        self.start_btn["state"] = DISABLED
        self.stop_btn["state"] = NORMAL

    def run_bot(self):
        """ Ejecuta el bot mientras no se detenga """
        try:
            bot.main(self.stop_event)  # ✅ PASAR stop_event a bot.py
        except Exception as e:
            self.log(f"⚠ Error en el bot: {e}")

        self.log("🛑 Bot detenido.")

    def stop_bot(self):
        """ Detiene la ejecución del bot """
        if not self.running:
            return

        self.log("🛑 Deteniendo el bot...")
        self.stop_event.set()  # ✅ Activar evento para detener el bot
        self.running = False

        self.start_btn["state"] = NORMAL
        self.stop_btn["state"] = DISABLED

    def clear_console(self):
        """ Limpia el área de la consola """
        self.log_area.config(state='normal')
        self.log_area.delete("1.0", "end")
        self.log_area.config(state='disabled')

    def log(self, message):
        """ Muestra mensajes en la consola """
        self.log_area.config(state='normal')
        self.log_area.insert("end", message + "\n")
        self.log_area.config(state='disabled')
        self.log_area.see("end")

    def write(self, message):
        """ Redirige la salida estándar a la consola """
        self.log(message.strip())

    def flush(self):
        pass

# ==========================
# 🔹 Función para iniciar la interfaz desde main.py
# ==========================
def iniciar_interfaz():
    root = ttk.Window(themename="darkly")
    app = BotGUI(root)
    root.mainloop()
