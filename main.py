import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


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

def get_tickets(driver):
    """Obtiene los tickets del iframe 'gsft_main'"""
    try:
        print("⏳ Buscando el iframe 'gsft_main' usando JavaScript...")
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )
        
        tickets = driver.execute_script("""
            let iframe = window.frames[0];
            let rows = iframe.document.querySelectorAll("tbody.list2_body tr");
            let ticketData = [];
            rows.forEach(row => {
                let id = row.querySelector("td:nth-child(3) a")?.innerText || "Sin ID";
                let sede = row.querySelectorAll("td")[5]?.innerText || "Sin Sede";
                ticketData.push({"id": id, "sede": sede});
            });
            return ticketData;
        """)
        print(f"📋 Tickets encontrados: {len(tickets)}")
        for ticket in tickets:
            print(f"📝 Ticket: {ticket['id']}, 📍 Sede: {ticket['sede']}")
        return tickets
    except Exception as e:
        print(f"❌ Error al obtener tickets: {e}")
        return []


def send_telegram_message(tickets):
    """Envía una notificación de nuevos tickets a Telegram"""
    telegram_token = "7841835490:AAHPpxf4u3ltaM9Lzpt785pZUA6qYjcPKC8"
    chat_id = "5264268680"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    for ticket in tickets:
        message = f"🚨 *Nuevo Ticket Detectado* 🚨\n🔹 *ID:* {ticket['id']}\n📍 *Sede:* {ticket['sede']}"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"📩 Notificación enviada para el ticket {ticket['id']}")
        else:
            print(f"⚠ Error al enviar mensaje para {ticket['id']}")


def main():
    start_chrome()
    driver = connect_to_chrome()
    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2520IN6%252C7%252C8%255E"
    driver.get(servicenow_url)
    print("🌐 Página cargada correctamente")
    time.sleep(15)

    # Primera ejecución: solo contar y guardar los tickets
    last_tickets = {t["id"] for t in get_tickets(driver)}
    print("✅ Tickets iniciales almacenados. No se enviarán notificaciones.")

    while True:
        time.sleep(60)  # Esperar antes de refrescar
        print("🔄 Refrescando la página...")
        driver.refresh()
        time.sleep(20)  # Esperar a que la página cargue completamente
        
        new_tickets = get_tickets(driver)
        current_tickets = {t["id"] for t in new_tickets}
        
        new_entries = [t for t in new_tickets if t["id"] not in last_tickets]
        
        if new_entries:
            print(f"⚡ Se detectaron {len(new_entries)} nuevos tickets.")
            send_telegram_message(new_entries)
        else:
            print("ℹ No hay nuevos tickets.")
        
        last_tickets = current_tickets


if __name__ == "__main__":
    main()
