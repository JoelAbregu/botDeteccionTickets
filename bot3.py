import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start_chrome():
    """Abre Chrome con depuración remota activada automáticamente"""
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    user_data_dir = "C:/ChromeProfile"

    subprocess.Popen([chrome_path, "--remote-debugging-port=9222", f"--user-data-dir={user_data_dir}"], shell=False)
    print("🚀 Chrome iniciado con depuración remota...")
    time.sleep(5)


def connect_to_chrome():
    """Conecta Selenium a la instancia de Chrome ya abierta"""
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ Conectado a Chrome correctamente")
    return driver


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
                    let url = link.href;
                    tickets.push({ estado, codigo, sede, url });
                }
            });
            return tickets;
        """)
        
        for idx, ticket in enumerate(ticket_data):
            print(f"🎫 Ticket {idx + 1}: | Código: {ticket['codigo']} | Sede: {ticket['sede']} | Estado: {ticket['estado']}")
        
        return ticket_data
    except Exception as e:
        print(f"❌ Error al extraer datos del ticket: {e}")
        return []


def extract_ticket_table_info(driver, ticket_url):
    """Extrae solo el estado y el porcentaje de negocio transcurrido dentro del ticket"""
    try:
        driver.get(ticket_url)
 
        # Esperar a que haya iframes en la página
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )

        # Ejecutar JavaScript para acceder al iframe y extraer solo los datos deseados
        script = """
        let iframe = window.frames[0];
        let tables = iframe.document.querySelectorAll("tbody.list2_body");
        if (tables.length === 0) return [];
        let rows = tables[0].querySelectorAll("tr");
        let data = [];
        rows.forEach(row => {
            let columns = row.querySelectorAll("td");
            if (columns.length > 7) {
                let estado = columns[6].innerText.trim();
                let porcentaje = columns[9].innerText.trim();
                data.push({ estado, porcentaje });
            }
        });
        return data;
        """
        ticket_data = driver.execute_script(script)

        print(f"📋 Datos extraídos en la primera tabla: {len(ticket_data)} registros")
        for idx, row in enumerate(ticket_data):
            print(f"📝 Registro {idx + 1}: Estado: {row['estado']}, Porcentaje: {row['porcentaje']}")
    except Exception as e:
        print(f"❌ Error al extraer los datos: {e}")


def main():
    start_chrome()
    driver = connect_to_chrome()

    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2520IN6%252C7%252C8%255E"
    driver.get(servicenow_url)
    print("🌐 Página cargada correctamente")

    # Extraer datos de los tickets
    tickets = extract_ticket_info(driver)
    
    # Extraer datos de la tabla dentro de cada ticket
    for ticket in tickets:
        extract_ticket_table_info(driver, ticket['url'])
    
    driver.quit()


if __name__ == "__main__":
    main()
