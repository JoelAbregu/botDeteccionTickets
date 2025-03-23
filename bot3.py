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

def count_and_extract_ticket_links(driver):
    """Cuenta los tickets y extrae los enlaces a los tickets"""
    try:
        print("⏳ Buscando el iframe 'gsft_main' usando JavaScript...")

        # Esperar a que haya iframes en la página
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )

        # Ejecutar JavaScript para acceder al iframe y contar los tickets
        ticket_links = driver.execute_script("""
            let iframe = window.frames[0];  // Acceder al primer iframe
            let rows = iframe.document.querySelectorAll("tbody.list2_body tr");
            let links = [];
            rows.forEach(row => {
                let link = row.querySelector("a");
                if (link) {
                    links.push(link.href);  // Obtener el enlace de cada ticket
                }
            });
            return links;
        """)

        print(f"📋 Enlaces de tickets encontrados: {len(ticket_links)}")
        for idx, link in enumerate(ticket_links):
            print(f"🔗 Enlace del ticket {idx + 1}: {link}")
        
        return ticket_links
    except Exception as e:
        print(f"❌ Error al extraer los enlaces de los tickets: {e}")
        return []

def extract_ticket_data(driver, ticket_url):
    """Navega a un ticket específico y extrae su información"""
    try:
        print(f"🔍 Abriendo el ticket: {ticket_url}")
        driver.get(ticket_url)  # Abrir solo el ticket específico
        time.sleep(5)  # Esperar a que la página cargue completamente

        # Esperar a que haya iframes en la página
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )

        # Ejecutar JavaScript para extraer datos del ticket abierto
        script = """
        let iframe = window.frames[0]; 
        let table = iframe.document.querySelector("tbody.list2_body");
        if (!table) return [];
        let rows = table.querySelectorAll("tr");
        let data = [];
        rows.forEach(row => {
            let columns = row.querySelectorAll("td");
            let rowData = [];
            columns.forEach(col => {
                rowData.push(col.innerText.trim());
            });
            data.push(rowData);
        });
        return data;
        """
        ticket_data = driver.execute_script(script)

        print(f"📋 Datos extraídos del ticket: {ticket_url}")
        for idx, row in enumerate(ticket_data):
            print(f"📝 {idx + 1}: {row}")
    except Exception as e:
        print(f"❌ Error al extraer los datos del ticket: {e}")

def main():
    start_chrome()
    driver = connect_to_chrome()

    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2520IN6%252C7%252C8%255E"
    driver.get(servicenow_url)
    print("🌐 Página cargada correctamente")

    # Extraer los enlaces de los tickets
    ticket_links = count_and_extract_ticket_links(driver)

    # Para cada enlace de ticket, extraer la información
    # ticket_links[0]
    # extract_ticket_data(driver, ticket_links[0])
    for ticket_url in ticket_links:
        extract_ticket_data(driver, ticket_url)

    driver.quit()  # Cerrar Chrome después de extraer los datos

if __name__ == "__main__":
    main()
