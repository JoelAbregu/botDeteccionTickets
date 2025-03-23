
import psutil
import socket
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
import psutil
import socket

def is_port_in_use(port):
    """Verifica si un puerto específico está en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def start_chrome():
    """Inicia Chrome en modo depuración remota si no está ya abierto."""
    if is_port_in_use(9222):  # Verifica si ya hay algo corriendo en el puerto
        print("✅ Chrome ya está en ejecución con depuración remota.")
        return  

    # Buscar si Chrome ya está corriendo
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():
            print("🔍 Chrome ya está en ejecución, pero sin depuración remota.")
            break  # Si está abierto, no intentamos abrir otro

    try:
        subprocess.Popen([
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "--remote-debugging-port=9222",
            "--user-data-dir=C:/ChromeProfile"
        ], shell=False)
        print("🚀 Chrome iniciado con depuración remota...")

        # Esperar hasta que el puerto esté disponible
        for _ in range(10):  # Intenta durante 10 segundos
            if is_port_in_use(9222):
                print("✅ Chrome con depuración remota disponible.")
                return
            time.sleep(1)

        print("❌ Error: Chrome no se inició correctamente con depuración remota.")
    except Exception as e:
        print(f"❌ Error al iniciar Chrome: {e}")

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

def extract_ticket_info(driver):
    """Extrae el estado, código, sede y enlaces de los tickets en la lista"""
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
                    let sede = cols[5].innerText.trim();
                    let estado = cols[8].innerText.trim();
                    let asignado = cols[10].innerText.trim();
                    let url = link.href;
                    tickets.push({ estado, codigo, sede, url, asignado });
                }
            });
            return tickets;
        """)
        
        print(f"\n🎫 Total de tickets encontrados: {len(ticket_data)}")
        print("=" * 60)

        for idx, ticket in enumerate(ticket_data, start=1):
            print(f"🎫 Ticket {idx:02d} | Código: {ticket['codigo']:10} | Sede: {ticket['sede']:10} | Estado: {ticket['estado']:10} | Asignado: {ticket['asignado']:10} ")

        print("=" * 60)
        
        return ticket_data
    except Exception as e:
        print(f"❌ Error al extraer datos del ticket: {e}")
        return []

def extract_ticket_table_info(driver, ticket):
    """Extrae el estado y los porcentajes dentro del ticket y los almacena en ticket['porcentajes']."""
  
    try:
        driver.get(ticket["url"])
        time.sleep(7) 

        # Esperar a que haya iframes en la página
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
                data.push({porcentaje });
            }
        });
        return data;
        """
        ticket_data = driver.execute_script(script)

        # Si hay datos, guardamos los porcentajes en la lista del ticket
        ticket["porcentajes"] = [row["porcentaje"] for row in ticket_data] if ticket_data else ["Sin datos"]

    except Exception as e:
        print(f"❌ Error al extraer los datos del ticket {ticket['codigo']}: {e}")
 

def main():
    start_chrome()
    driver = connect_to_chrome()
    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2520IN6%252C7%252C8%255E"
    ensure_servicenow_tab(driver, servicenow_url)  

    while True:
        print("🔄 Ejecutando ciclo de monitoreo de tickets...")
        driver.refresh()
        time.sleep(10)
        tickets = extract_ticket_info(driver)
        for ticket in tickets:
            extract_ticket_table_info(driver, ticket)
        # 📌 IMPRIMIR RESULTADOS FINALES
        print(f"\n🎫 Total de tickets encontrados: {len(tickets)}")
        for ticket in tickets:
            porcentajes_str = " | ".join(ticket["porcentajes"])
            print(f"🎫 Ticket {ticket['codigo']} | SLA: {porcentajes_str}")
        driver.get(servicenow_url)
        time.sleep(30) 



if __name__ == "__main__":
    main()

