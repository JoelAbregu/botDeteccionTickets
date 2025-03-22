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

def count_tickets(driver):
    """Cuenta los tickets dentro del iframe 'gsft_main' usando JavaScript"""
    try:
        print("⏳ Buscando el iframe 'gsft_main' usando JavaScript...")

        # Esperar a que haya iframes en la página
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return window.frames.length;") > 0
        )

        # Ejecutar JavaScript para acceder al iframe y contar los tickets
        ticket_count = driver.execute_script("""
            let iframe = window.frames[0];  // Acceder al primer iframe
            return iframe.document.querySelectorAll("tbody.list2_body tr").length;
        """)

        print(f"📋 Tickets encontrados: {ticket_count}")
    except Exception as e:
        print(f"❌ Error al contar los tickets: {e}")

def main():
    start_chrome()
    driver = connect_to_chrome()

    servicenow_url = "https://tasa.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dassignment_group%253D7373b389db3c2f004619e66505961977%255EstateNOT%2520IN6%252C7%252C8%255Ebusiness_service%253D76d93b33dbae4810b193550a48961934%255E"

    driver.get(servicenow_url)
    print("🌐 Página cargada correctamente")

    count_tickets(driver)

    driver.quit()  # Cerrar Chrome después de contar los tickets

if __name__ == "__main__":
    main()
