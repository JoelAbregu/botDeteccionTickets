import pywhatkit as kit
import time
import psutil
import socket
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================
# 🔹 Función para conectar a Chrome con depuración remota
# ==========================
def connect_to_chrome():
    #! Conecta a una instancia existente de Chrome con depuración remota.
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Conectado a Chrome correctamente")
        return driver
    except Exception as e:
        print(f"❌ No se pudo conectar a Chrome: {e}")
        return None

# ==========================
# 🔹 Función para verificar si un puerto está en uso
# ==========================
def is_port_in_use(port):
    #! Verifica si un puerto específico está en uso.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

# ==========================
# 🔹 Función para iniciar Chrome con depuración remota
# ==========================
def start_chrome():
    #! Inicia Chrome en modo depuración remota si no está ya abierto.
    if is_port_in_use(9222):  
        print("✅ Chrome ya está en ejecución con depuración remota.")
        return  
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():
            print("🔍 Chrome ya está en ejecución, pero sin depuración remota.")
            break  
    try:
        subprocess.Popen([
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "--remote-debugging-port=9222",
            "--user-data-dir=C:/ChromeProfile"
        ], shell=False)
        print("🚀 Chrome iniciado con depuración remota...")
        for _ in range(10):  
            if is_port_in_use(9222):
                print("✅ Chrome con depuración remota disponible.")
                return
            time.sleep(1)
        print("❌ Error: Chrome no se inició correctamente con depuración remota.")
    except Exception as e:
        print(f"❌ Error al iniciar Chrome: {e}")

# ==========================
# 🔹 Función para verificar si la pestaña de ServiceNow está abierta
# ==========================
def ensure_servicenow_tab(driver, url):
    #! Verifica si la pestaña de ServiceNow está abierta y la abre si es necesario.
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if url in driver.current_url:
            print("✔ Pestaña de ServiceNow ya está abierta.")
            return True
    print("🌐 Pestaña de ServiceNow no encontrada, abriendo nueva pestaña...")
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10) 
    return True

# ==========================
# 🔹 Función para enviar texto por whatsapp
# ==========================
def send_whatsapp_text(numero, mensaje):
    #! Envía un mensaje de WhatsApp 
    try:
        kit.sendwhatmsg_instantly(phone_no=numero, message=mensaje, wait_time=20, tab_close=True)
        print(f"✅ Mensaje enviado a {numero} y pestaña cerrada.")
    except Exception as e:
        print(f"❌ Error al enviar mensaje de WhatsApp a {numero}: {e}")

# ==========================
# 🔹 Función para enviar mensaje por whatsapp
# ==========================
def send_whatsapp_ticket(ticket, numero):
    #! Envía un mensaje de WhatsApp si el ticket cumple con las condiciones.
    mensaje =  (f"🚀 *NUEVO TICKET ASIGNADO* 🚀\n\n"
                f"🔹 *Código:* {ticket['codigo']}\n"
                f"📌 *Estado:* {ticket['estado']}\n"
                f"🏢 *Sede:* {ticket['sede']}\n"
                f"👤 *Asignado a:* {ticket['asignado']}\n"
                f"📝 *Detalle breve:* - {ticket['descripcion']}\n"
                f"🔗 *Enlace:* {ticket['url']}\n\n"
                f"⚡ Revisa y atiende cuanto antes. ¡Gracias! 👍")
    try:
        kit.sendwhatmsg_instantly(phone_no=numero, message=mensaje, wait_time=20, tab_close=True)
        print(f"✅ Mensaje de WhatsApp enviado a {numero} y pestaña cerrada.")
    except Exception as e:
        print(f"❌ Error al enviar mensaje de WhatsApp a {numero}: {e}")

# ==========================
# 🔹 Función para extraer información de los tickets
# ==========================
previous_tickets = set()
def extract_ticket_info(driver):
    #! Extrae el estado, código, sede y enlaces de los tickets en la lista y detecta nuevos tickets.
    global previous_tickets
    time.sleep(20) 
    try:
        ticket_data = driver.execute_script("""
            let iframe = window.frames[0];  // Acceder al primer iframe
            let rows = iframe.document.querySelectorAll("tbody.list2_body tr");
            let tickets = [];
            rows.forEach(row => {
                let cols = row.querySelectorAll("td");
                let link = row.querySelector("a");
                if (cols.length > 2 && link) {
                    let codigo = cols[2].innerText.trim();
                    let descripcion = cols[4].innerText.trim();
                    let sede = cols[5].innerText.trim();
                    let estado = cols[8].innerText.trim();
                    let asignado = cols[10].innerText.trim(); 
                    let url = link.href;
                    tickets.push({ estado, codigo, sede, url, asignado, descripcion });
                }
            });
            return tickets;
        """)
        
        current_tickets = {ticket['codigo'] for ticket in ticket_data}
        new_tickets = current_tickets - previous_tickets
        previous_tickets = current_tickets 
        print(f"\n🎫 Total de tickets encontrados: {len(ticket_data)}")
        print("=" * 60)
        
        # Mostrar información de los tickets
        for idx, ticket in enumerate(ticket_data, start=1):
            print(f"🎫 Ticket {idx:02d} | Código: {ticket['codigo']:10} | Sede: {ticket['sede']:10} | Estado: {ticket['estado']:10} | Asignado: {ticket['asignado']:10} ")
        print("=" * 60)
        
        # Notificar sobre nuevos tickets y enviar mensajes de WhatsApp
        if new_tickets:
            for ticket in ticket_data:
                if ticket['codigo'] in new_tickets:
                    print(f"📢 Nuevo ticket encontrado: Código: {ticket['codigo']}, Sede: {ticket['sede']}, Estado: {ticket['estado']}, Asignado: {ticket['asignado']}")

                    # Enviar mensaje de WhatsApp si cumple con las condiciones
                    # if ticket['estado'] == "Asignado" and ticket['sede'] in ["Samanco", "Astillero", "Chimbote"] and ticket['asignado'] == "SoporteTI - Norte":
                        # send_whatsapp_ticket(ticket, "+51932125452")
                    if ticket['estado'] == "Asignado" and ticket['sede'] == "Pisco Sur" and ticket['asignado'] == "SoporteTI - Centro":
                        send_whatsapp_ticket(ticket, "+51977470126")
                    if ticket['estado'] == "Asignado":
                        send_whatsapp_ticket(ticket, "+51977470126")
                        # time.sleep(20) 
                        # send_whatsapp_ticket(ticket, "+51941382228")
                        # time.sleep(20) 
                        # send_whatsapp_ticket(ticket, "+51932125452")
        return ticket_data
    except Exception as e:
        print(f"❌ Error al extraer datos del ticket: {e}")
        return []

# ==========================
# 🔹 Función para sacar el SLA de cada ticket
# ==========================
def extract_ticket_table_info(driver, ticket):
    #! Extrae el estado y los porcentajes dentro del ticket y los almacena en ticket['porcentajes'].
    try:
        driver.get(ticket["url"])

        # Esperar a que haya iframes en la página
        time.sleep(30) 
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )

        # Ejecutar JavaScript para extraer los datos
        script = """
        let iframe = window.frames[0];
        let tables = iframe.document.querySelectorAll("tbody.list2_body");
        if (tables.length === 0) return [];
        let rows = tables[0].querySelectorAll("tr");
        let data = [];
        rows.forEach(row => {
            let columns = row.querySelectorAll("td");
            if (columns.length > 7) {
                let porcentaje = columns[9] ? columns[9].innerText.trim() : "N/A";
                let definicion = columns[3] ? columns[3].innerText.trim() : "N/A";
                let tiempoRestante = columns[7] ? columns[7].innerText.trim() : "N/A";
                data.push({porcentaje,definicion,tiempoRestante});
            }
        });
        return data;
        """
        ticket_data = driver.execute_script(script)

        # Si hay datos, almacenamos los valores en el ticket
        if ticket_data:
            ticket["porcentajes"] = [row["porcentaje"] for row in ticket_data]
            ticket["definiciones"] = [row["definicion"] for row in ticket_data]
            ticket["tiemposRestantes"] = [row["tiempoRestante"] for row in ticket_data]
        else:
            ticket["porcentajes"] = ["Sin datos"]
            ticket["definiciones"] = ["Sin datos"]
            ticket["tiemposRestantes"] = ["Sin datos"]
        print(f"🎫 Ticket {ticket['codigo']:10} | Porcentajes: {ticket['porcentajes']} | Definiciones: {ticket['definiciones']} | Tiempos Restantes: {ticket['tiemposRestantes']}")
    except Exception as e:
        print(f"❌ Error al extraer los datos del ticket {ticket['codigo']}: {e}")

def main(stop_event):
    start_chrome()
    driver = connect_to_chrome()
    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2520IN6%252C7%252C8%255E"
    ensure_servicenow_tab(driver, servicenow_url)  

    while not stop_event.is_set():  # 🔹 Se detiene si stop_event está activado
        print("🔄 Ejecutando ciclo de monitoreo de tickets...")
        time.sleep(10)
        
        tickets = extract_ticket_info(driver)
        for ticket in tickets:
            extract_ticket_table_info(driver, ticket)
        
        print(f"\n🎫 Total de tickets encontrados: {len(tickets)}")
        for ticket in tickets:
            extract_ticket_table_info(driver, ticket)
            #check_sla_alerts(ticket)  # Comparamos los SLA y enviamos alertas si aplica
            # porcentajes_str = " | ".join(ticket["porcentajes"])
            # print(f"🎫 Ticket {ticket['codigo']} | SLA: {porcentajes_str}")
        
        driver.get(servicenow_url)
        time.sleep(30)
        driver.refresh()

    print("🛑 El bot ha sido detenido.")

if __name__ == "__main__":
    main()