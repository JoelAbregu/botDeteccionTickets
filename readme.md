# 🤖 Bot de Monitoreo de Tickets en ServiceNow vía WhatsApp

Este proyecto es un **bot automatizado en Python** que se conecta a **ServiceNow** y detecta nuevos tickets en tiempo real. Cuando se identifica un nuevo ticket asignado, el bot **envía una notificación instantánea a través de WhatsApp** al responsable correspondiente, mejorando significativamente la atención de incidencias.

## 🚀 Funcionalidades Principales

- 🔍 **Monitoreo en tiempo real** de tickets en ServiceNow mediante web scraping con Selenium.
- 📲 **Envío automático de mensajes por WhatsApp** usando la librería `pywhatkit`.
- 📁 Extracción detallada de información del ticket (estado, sede, asignado, descripción, SLA).
- 🧠 Clasificación automática de tickets y lógica condicional para el envío de alertas.
- 🛠️ Compatibilidad con depuración remota de Google Chrome para automatizar sin bloqueos.

## 🧪 Tecnologías Utilizadas

- Python 3
- [Selenium](https://www.selenium.dev/)
- [pywhatkit](https://github.com/Ankit404butfound/PyWhatKit)
- Google Chrome (con `--remote-debugging-port`)
- psutil, socket, subprocess

## ⚙️ Requisitos

- Google Chrome instalado.
- Librerías de Python instaladas:

```bash
pip install selenium pywhatkit psutil
```

- Crear un perfil de Chrome con depuración remota:

```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeProfile"
```

## 🧭 ¿Cómo funciona?

1. El bot inicia o se conecta a Chrome en modo depuración.
2. Accede a la URL de incidentes de ServiceNow.
3. Lee los tickets y detecta si hay alguno nuevo desde el último escaneo.
4. Si encuentra nuevos tickets asignados, envía notificaciones vía WhatsApp al número correspondiente.
5. También extrae información del SLA de cada ticket y la imprime por consola.

## 📦 Estructura del Código

- `start_chrome()` – Inicia Chrome con depuración.
- `connect_to_chrome()` – Conecta Selenium a una instancia existente.
- `extract_ticket_info()` – Extrae tickets desde la tabla de ServiceNow.
- `send_whatsapp_ticket()` – Envía mensajes por WhatsApp con el contenido del ticket.
- `extract_ticket_table_info()` – Extrae detalles del SLA del ticket.

## 🔐 Consideraciones de Seguridad

- Este bot funciona en tu entorno local y requiere tener sesión iniciada en WhatsApp Web para poder enviar mensajes.
- Asegúrate de tener permisos adecuados para acceder a ServiceNow y manipular los datos.

## 📸 Ejemplo de Notificación en WhatsApp

```
🚀 NUEVO TICKET ASIGNADO 🚀

🔹 Código: INC123456
📌 Estado: Asignado
🏢 Sede: Pisco Sur
👤 Asignado a: SoporteTI - Centro
📝 Detalle breve: Problema con conexión de red
🔗 Enlace: https://tasa.service-now.com/...

⚡ Revisa y atiende cuanto antes. ¡Gracias! 👍
```

## 🧑‍💻 Autor

**Joel Abregu Manrique**  
Ingeniero de Software | Soporte TI | Automatización de procesos  
📧 abregumanriquef@gmail.com  
🔗 [LinkedIn](#) (agrega tu perfil si deseas)

---

¿Quieres que lo guarde como archivo `.md` también?