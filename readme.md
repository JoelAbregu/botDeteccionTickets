---

# 🎯 Monitor de Tickets ServiceNow con Alertas por WhatsApp

Este proyecto automatiza el monitoreo de incidentes en **ServiceNow**, extrae información clave de los tickets asignados y envía alertas mediante **WhatsApp** a través de la biblioteca `pywhatkit`. Ideal para equipos de soporte técnico que necesitan mantenerse informados en tiempo real sobre nuevos tickets o cambios en su estado.

---

## 🚀 Características

- Conexión automática a Chrome con **depuración remota**.
- Detección inteligente de **nuevos tickets**.
- Extracción de detalles clave: código, estado, sede, asignado, descripción, SLA.
- Envío instantáneo de mensajes de **WhatsApp** con formato personalizado.
- Monitoreo cíclico y actualización en tiempo real desde la interfaz de ServiceNow.
- Integración con **Selenium WebDriver** y control de procesos con `psutil`.

---

## 🧠 Tecnologías utilizadas

- `Python 3.x`
- `Selenium`
- `pywhatkit`
- `psutil`
- `subprocess`, `socket`, `time`

---

## ⚙️ Requisitos previos

- Tener **Google Chrome** instalado en:
  ```
  C:/Program Files/Google/Chrome/Application/chrome.exe
  ```
- Ejecutar Chrome con el siguiente comando para habilitar la depuración remota:

  ```bash
  chrome.exe --remote-debugging-port=9222 --user-data-dir=C:/ChromeProfile
  ```

- Instalar las dependencias con pip:

  ```bash
  pip install pywhatkit selenium psutil
  ```

---

## 🧪 Cómo usar

1. **Ejecuta el script principal:**

   ```bash
   python main.py
   ```

2. El bot abrirá o se conectará a Chrome, navegará al listado de tickets de ServiceNow y comenzará a monitorear nuevos casos.

3. Cuando se detecte un nuevo ticket con ciertas condiciones (por ejemplo, estado *Asignado* y sede específica), se enviará una notificación por WhatsApp al número configurado.

---

## 📌 Personalización

Puedes modificar las condiciones de envío de mensajes editando la sección:

```python
if ticket['estado'] == "Asignado" and ticket['sede'] == "Pisco Sur" and ticket['asignado'] == "SoporteTI - Centro":
    send_whatsapp_ticket(ticket, "+51977470126")
```

---

## 🛑 Detener el bot

Para finalizar la ejecución, presiona `Ctrl + C` o implementa un evento externo que active `stop_event`.

---

## 📎 Notas importantes

- El script usa `window.frames[0]` para acceder al iframe de ServiceNow. Asegúrate de que la estructura del HTML no haya cambiado.
- Para evitar bloqueos o errores por tiempos de carga, se utilizan `time.sleep()` estratégicamente. Estos valores pueden ajustarse según el rendimiento de tu red o dispositivo.
- WhatsApp Web puede requerir estar autenticado previamente para enviar mensajes.

---

## 👨‍💻 Autor

**Joel Abregu Manrique**  
 