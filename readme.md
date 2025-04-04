Perfecto. Aquí tienes el `README.md` mejorado con un diseño claro, bien estructurado y presentable para un repositorio en GitHub. Incluye secciones con encabezados jerárquicos, bloques de código, íconos Markdown (sin emoticones), y formato consistente para facilitar la lectura:

---

```markdown
# 🛠️ Ticket Monitoring Bot

Un bot desarrollado en Python que monitorea tickets en ServiceNow y envía notificaciones automáticas por WhatsApp cuando se detectan nuevos tickets asignados.

---

## 📌 Descripción

Este sistema automatizado permite:

- Detectar si Chrome está abierto en modo de depuración.
- Conectarse al navegador para buscar o abrir la pestaña de ServiceNow.
- Extraer información de cada ticket desde el iframe principal.
- Evaluar el SLA y estado de cada ticket.
- Enviar alertas automáticas por WhatsApp sobre tickets asignados.

---

## ⚙️ Tecnologías y Librerías

- **Python 3.7+**
- **Selenium**
- **PyWhatKit**
- **psutil**
- **Google Chrome (con debugging remoto)**

---

## 📁 Estructura del Proyecto

| Módulo / Función | Descripción |
|------------------|-------------|
| `start_chrome()` | Inicia Chrome con el puerto de depuración remota si no está activo. |
| `connect_to_chrome()` | Conecta Selenium al navegador. |
| `ensure_servicenow_tab(driver, url)` | Abre o verifica la pestaña de ServiceNow. |
| `extract_ticket_info(driver)` | Obtiene información de cada ticket. |
| `extract_ticket_table_info(driver, ticket)` | Evalúa el SLA de cada ticket. |
| `send_whatsapp_ticket(ticket, numero)` | Envía notificación por WhatsApp si el ticket es relevante. |

---

## 🧪 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ticket-monitoring-bot.git
cd ticket-monitoring-bot
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

> Asegúrate de tener `Chrome` instalado y que exista un perfil en `C:/ChromeProfile`.

### 3. Ejecutar el bot

```bash
python main.py
```

> El script abrirá Chrome, se conectará a ServiceNow y comenzará a monitorear los tickets.

---

## ⚠️ Consideraciones

- El uso de WhatsApp Web mediante `pywhatkit` requiere que la sesión esté iniciada.
- Se recomienda supervisar el uso de recursos si se ejecuta constantemente en segundo plano.
- Este bot **no** guarda información sensible ni credenciales.

---

## ✅ Requisitos Previos

- Chrome instalado (ruta por defecto: `C:/Program Files/Google/Chrome/Application/chrome.exe`)
- Usuario logueado previamente en WhatsApp Web
- Acceso autorizado a ServiceNow desde el navegador

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar funcionalidades, optimizar el código o reportar errores, no dudes en hacer un pull request o abrir un issue.

---

## 📜 Licencia

Este proyecto está licenciado bajo los términos del MIT License.

---

## 👨‍💻 Autor

Joel Abregu Manrique  
 