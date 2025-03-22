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

    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}"
    ], shell=False)

    print("🚀 Chrome iniciado con depuración remota...")
    time.sleep(5)

def connect_to_chrome():
    """Conecta Selenium a la instancia de Chrome ya abierta"""
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ Conectado a Chrome correctamente")
    return driver

def extract_ticket_data(driver):
    """Extrae los datos de los tickets desde la primera tabla del iframe 'gsft_main'"""
    try:
        print("⏳ Buscando el iframe 'gsft_main' usando JavaScript...")

        # Esperar a que haya iframes en la página
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )

        # Ejecutar JavaScript para acceder al iframe y extraer datos de la primera tabla
        script = """
        let iframe = window.frames[0];
        let tables = iframe.document.querySelectorAll("tbody.list2_body");
        if (tables.length === 0) return [];
        let rows = tables[0].querySelectorAll("tr");
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

        print(f"📋 Tickets encontrados en la primera tabla: {len(ticket_data)}")
        for idx, row in enumerate(ticket_data):
            print(f"📝 Ticket {idx + 1}: {row}")
    except Exception as e:
        print(f"❌ Error al extraer los tickets: {e}")

def main():
    start_chrome()
    driver = connect_to_chrome()

    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident.do%3Fsys_id%3Df365183f2b106a10167ffa6cee91bfb0%26sysparm_record_target%3Dincident%26sysparm_record_row%3D1%26sysparm_record_rows%3D9%26sysparm_record_list%3Dassignment_group%253D08d4f78ddb3c2f004619e665059619aa%255EstateNOT%2BIN6%252C7%252C8%255EORDERBYDESCopened_at"
    driver.get(servicenow_url)
    print("🌐 Página cargada correctamente")

    extract_ticket_data(driver)
    driver.quit()  # Cerrar Chrome después de extraer los datos

if __name__ == "__main__":
    main()