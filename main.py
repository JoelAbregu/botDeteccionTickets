import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def connect_to_chrome():
    """Conecta a una instancia existente de Chrome con depuración remota, si existe."""
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Conectado a Chrome correctamente")
        return driver
    except Exception as e:
        print(f"❌ No se pudo conectar a Chrome: {e}")
        return None

def start_chrome():
    """Inicia Chrome en modo depuración remota si no está ya abierto."""
    if connect_to_chrome():
        return  # Si ya hay una instancia, no abre otra
    subprocess.Popen([
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "--remote-debugging-port=9222",
        "--user-data-dir=C:/ChromeProfile"
    ], shell=False)
    print("🚀 Chrome iniciado con depuración remota...")
    time.sleep(5)

def ensure_servicenow_tab(driver, url):
    """Verifica si la pestaña de ServiceNow está abierta y la abre si es necesario."""
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if url in driver.current_url:
            print("✔ Pestaña de ServiceNow ya está abierta.")
            return True
    print("🌐 Pestaña de ServiceNow no encontrada, abriendo nueva pestaña...")
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)  # Esperar a que cargue completamente
    return True

def wait_for_login(driver):
    """Espera si el usuario necesita iniciar sesión en Microsoft antes de continuar."""
    while "login.microsoftonline.com" in driver.current_url:
        print("⏳ Esperando inicio de sesión en Microsoft...")
        time.sleep(5)
    print("✅ Sesión iniciada, continuando con el bot...")

def count_tickets(driver):
    """Cuenta los tickets dentro del iframe 'gsft_main' y obtiene detalles."""
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )
        tickets = driver.execute_script("""
            let iframe = window.frames[0];
            let rows = iframe.document.querySelectorAll("tbody.list2_body tr");
            let ticketData = [];
            rows.forEach(row => {
                let id = row.querySelector("td:nth-child(3) a")?.innerText || "Sin ID";
                let location = row.querySelectorAll("td")[5]?.innerText || "Sin ubicación";
                let ticket_url = row.querySelector("td:nth-child(3) a")?.href || "#";
                ticketData.push({"id": id, "ubicacion": location, "url": ticket_url});
            });
            return ticketData;
        """)
        return tickets
    except Exception as e:
        print(f"❌ Error al contar tickets: {e}")
        return []

def get_ticket_details(driver, ticket):
    """Abre un ticket en segundo plano, extrae el porcentaje de negocio y estado, y cierra la pestaña."""
    try:
        main_window = driver.current_window_handle  # Guardar la ventana principal
        driver.execute_script(f"window.open('{ticket['url']}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "percent_complete_text")))
        
        details = driver.execute_script("""
            let details = {};
            details["estado"] = document.querySelector("td:nth-child(7)")?.innerText || "Sin estado";
            details["porcentaje_negocio"] = document.querySelector(".percent_complete_text")?.innerText || "0%";
            return details;
        """)
        driver.close()
        driver.switch_to.window(main_window)  # Volver a la pestaña principal
        return details
    except Exception as e:
        print(f"❌ Error al obtener detalles del ticket {ticket['id']}: {e}")
        return {}

def send_telegram_message(tickets):
    """Envía notificación de nuevos tickets a Telegram."""
    telegram_token = "TOKEN_AQUI"
    chat_id = "CHAT_ID_AQUI"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    
    for ticket in tickets:
        details = get_ticket_details( ticket)
        message = (f"🚨 *Nuevo Ticket Detectado* 🚨\n"
                   f"🔹 *ID:* {ticket['id']}\n"
                   f"📍 *Ubicación:* {ticket['ubicacion']}\n"
                   f"📊 *Porcentaje de Negocio:* {details.get('porcentaje_negocio', 'No disponible')}\n"
                   f"📌 *Estado:* {details.get('estado', 'No disponible')}")
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"📩 Notificación enviada para el ticket {ticket['id']}")
        else:
            print(f"⚠ Error al enviar mensaje para {ticket['id']}")

def main():
    start_chrome()
    driver = connect_to_chrome()
    if not driver:
        print("❌ No se pudo conectar a Chrome. Cerrando el bot...")
        return
    servicenow_url="https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2520IN6%252C7%252C8%255E"
    ensure_servicenow_tab(driver, servicenow_url)
    wait_for_login(driver)
    
    print("⏳ Contando tickets iniciales...")
    initial_tickets = count_tickets(driver)
    
    for ticket in initial_tickets:
        details = get_ticket_details(driver, ticket)
        print(f"📝 Ticket: {ticket['id']}, 📍 Ubicación: {ticket['ubicacion']}, "
              f"📊 Porcentaje Negocio: {details.get('porcentaje_negocio', 'No disponible')}, "
              f"📌 Estado: {details.get('estado', 'No disponible')}")

    print(f"✅ Tickets iniciales: {len(initial_tickets)}")
    last_ticket_ids = {ticket["id"] for ticket in initial_tickets}
    
    while True:
        time.sleep(60)
        print("🔄 Refrescando la página...")
        driver.refresh()
        time.sleep(10)
        
        new_tickets = count_tickets(driver)
        new_ticket_ids = {ticket["id"] for ticket in new_tickets}
        
        added_tickets = [t for t in new_tickets if t["id"] not in last_ticket_ids]
        if added_tickets:
            print(f"⚡ Se detectaron {len(added_tickets)} nuevos tickets.")
            send_telegram_message(added_tickets)
            last_ticket_ids = new_ticket_ids
        else:
            print("ℹ No hay nuevos tickets.")

if __name__ == "__main__":
    main()