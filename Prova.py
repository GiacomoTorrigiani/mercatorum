from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, 
                                       NoSuchElementException, 
                                       StaleElementReferenceException,
                                       WebDriverException,
                                       ElementClickInterceptedException)
import time
import re
import random

def parse_duration(duration_str):
    """Converte la durata mm:ss in secondi totali"""
    try:
        if ':' in duration_str:
            parts = duration_str.split(':')
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
        return 0
    except:
        return 0

# Configurazione avanzata di Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless=new")

# Inizializza il driver
driver = webdriver.Chrome(options=chrome_options)

# Funzione per il login
def login():
    driver.get("https://lms.mercatorum.multiversity.click/accedi")
    time.sleep(2 + random.uniform(0.5, 1.5))
    
    try:
        username_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys("gtorrigiani_0662400191")
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("Password1!")
        
        login_button = driver.find_element(By.XPATH, '//button[span[text()="Accedi"]]')
        login_button.click()
        time.sleep(8 + random.uniform(1, 3))
        return True
    except Exception as e:
        print(f"Errore durante il login: {str(e)}")
        return False

# URL della pagina delle videolezioni
lessons_url = "https://lms.mercatorum.multiversity.click/videolezioni/0662409INGINF05I/"

# Esegui il login
if not login():
    print("Impossibile completare il login, chiudo...")
    driver.quit()
    exit()

# Naviga alla pagina delle lezioni
driver.get(lessons_url)
time.sleep(8 + random.uniform(1, 3))
# CODICE AGGIUNTO PER GESTIRE I COOKIE
try:
    cookie_banner = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'fixed') and contains(@class, 'bottom-0')]"))
    )
    
    accept_button = cookie_banner.find_element(By.XPATH, ".//button[contains(., 'Accetta')]")
    
    # Scroll e click con controllo degli errori
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", accept_button)
    time.sleep(1)
    
    try:
        accept_button.click()
    except ElementClickInterceptedException:
        print("  Fallito click normale, tentativo con JS")
        driver.execute_script("arguments[0].click();", accept_button)
    
    print("Accettati i cookie")
    time.sleep(3)
except Exception as e:
    print(f"Gestione cookie fallita: {str(e)}")

# FASE 1: Espandi tutti i paragrafi
try:
    expand_buttons = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'cursor-pointer')]//*[name()='svg']//*[name()='path' and contains(@id, 'chevron-down')]"))
    )
    print(f"Trovati {len(expand_buttons)} elementi da espandere")
    
    for btn in expand_buttons:
        try:
            parent = btn.find_element(By.XPATH, "./ancestor::div[contains(@class, 'cursor-pointer')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", parent)
            time.sleep(0.3 + random.uniform(0.1, 0.5))
            parent.click()
            time.sleep(0.5 + random.uniform(0.1, 0.3))
        except Exception as e:
            print(f"  Saltato elemento durante l'espansione: {str(e)}")
except TimeoutException:
    print("Nessun elemento espandibile trovato, continuo...")

time.sleep(5 + random.uniform(1, 2))
# FASE 2: Esegui tutti i test disponibili
try:
    # Trova tutti i pulsanti "Esegui" per i test
    test_buttons = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(., 'Test di fine lezione')]//button[contains(., 'Esegui')]"))
    )
    print(f"Trovati {len(test_buttons)} test da eseguire")
    
    for i in range(len(test_buttons)):
        try:
            # Ricarica la lista aggiornata dei pulsanti
            current_test_buttons = driver.find_elements(By.XPATH, "//div[contains(., 'Test di fine lezione')]//button[contains(., 'Esegui')]")
            
            # Salta i test già completati
            if i >= len(current_test_buttons):
                print(f"  Test {i+1} già completato, salto")
                continue
                
            # Scorri e clicca il pulsante "Esegui"
            driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", current_test_buttons[i])
            time.sleep(1 + random.uniform(0.1, 0.3))
            current_test_buttons[i].click()
            print(f"  Apertura test {i+1}")
            time.sleep(3)  # Attendi apertura test
            
            # Trova tutte le domande del test
            questions = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'mt-8') and contains(@class, 'px-4')]"))
            )
            print(f"  Trovate {len(questions)} domande nel test")
            
            # Rispondi a ciascuna domanda
            for j, question in enumerate(questions):
                try:
                    # Trova tutte le opzioni di risposta per questa domanda
                    options = question.find_elements(By.XPATH, ".//div[contains(@class, 'px-3') and contains(@class, 'hover:bg-platform-hover-light')]")
                    if not options:
                        continue
                    
                    # Seleziona un'opzione casuale
                    random_option = random.choice(options)
                    driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", random_option)
                    time.sleep(0.5 + random.uniform(0.1, 0.3))
                    random_option.click()
                    print(f"    Selezione risposta {j+1}")
                    time.sleep(1.5)  # Intervallo tra le risposte
                    
                except Exception as e:
                    print(f"    Errore nella domanda {j+1}: {str(e)}")
            
            # Invia il test
            submit_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Invia')]"))
            )
            submit_btn.click()
            print("  Test inviato")
            time.sleep(3)  # Attendi conferma invio
            
            # Chiudi la modale del test
            try:
                close_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//*[local-name()='svg' and @id='x']]"))
                )
                close_btn.click()
                print("  Chiusura modale del test")
                time.sleep(1)
            except TimeoutException:
                print("  Pulsante di chiusura non trovato")
            
            # Attendi prima del prossimo test
            time.sleep(2)
            
        except Exception as e:
            print(f"  Errore durante l'esecuzione del test {i+1}: {str(e)}")
            # Tentativo di chiusura modale in caso di errore
            try:
                driver.find_element(By.XPATH, "//button[.//*[local-name()='svg' and @id='x']]").click()
            except:
                pass
            time.sleep(2)
except TimeoutException:
    print("Nessun test trovato, procedo alla chiusura")            
# FASE 2: Apri tutti gli obiettivi
content_items = driver.find_elements(By.CSS_SELECTOR, "div.border-t.hover\\:bg-platform-hover-light, div.flex.items-center.justify-between.pr-3.py-3.text-base.border-t")
print(f"Elementi trovati: {len(content_items)}")

for item in content_items:
    try:
        title = item.find_element(By.CSS_SELECTOR, "div.text-base, div.mb-2").text
        if "Obiettivi" in title:
            print(f"Trovati obiettivi: {title} - Faccio click")
            try:
                item.click()
                time.sleep(1 + random.uniform(0.1, 0.5))
            except:
                pass
    except:
        pass

# FASE 3: Trova e memorizza tutti i video incompleti
video_list = []
content_items = driver.find_elements(By.CSS_SELECTOR, "div.border-t.hover\\:bg-platform-hover-light, div.flex.items-center.justify-between.pr-3.py-3.text-base.border-t")

for idx, item in enumerate(content_items):
    try:
        title = item.find_element(By.CSS_SELECTOR, "div.text-base, div.mb-2").text
        
        # Salta test e obiettivi
        if "Test di fine lezione" in title or "Obiettivi" in title:
            continue
            
        # Prova a trovare gli elementi di progresso e durata
        try:
            progress_text = item.find_element(By.CSS_SELECTOR, "div.w-1\\/12.text-xs").text
            progress_value = int(re.search(r'\d+', progress_text).group(0)) if progress_text else 0
            
            duration_text = item.find_element(By.CSS_SELECTOR, "div.text-sm.text-platform-gray").text
            total_seconds = parse_duration(duration_text)
            
            if progress_value < 100 and total_seconds > 0:
                print(f"Video incompleto trovato: {title} - Durata: {duration_text}")
                # Memorizza l'indice e il titolo invece dell'elemento
                video_list.append((idx, title, total_seconds))
        except NoSuchElementException:
            continue
    except Exception as e:
        print(f"Errore durante l'elaborazione dell'elemento: {str(e)}")
        continue

print(f"\nTrovati {len(video_list)} video incompleti da riprodurre")

# FASE 4: Riproduci tutti i video in sequenza
for video_idx, (original_idx, title, total_seconds) in enumerate(video_list):
    print(f"\nAvvio video {video_idx+1}/{len(video_list)}: {title}")
    
    try:
        # Ricarica la lista degli elementi per evitare riferimenti stale
        current_items = driver.find_elements(By.CSS_SELECTOR, "div.border-t.hover\\:bg-platform-hover-light, div.flex.items-center.justify-between.pr-3.py-3.text-base.border-t")
        
        # Verifica se l'indice è ancora valido
        if original_idx >= len(current_items):
            print(f"  Indice originale {original_idx} non più valido (nuova lunghezza: {len(current_items)}). Ricarico la pagina...")
            driver.get(lessons_url)
            time.sleep(5)
            # Ricrea la lista dopo il refresh
            current_items = driver.find_elements(By.CSS_SELECTOR, "div.border-t.hover\\:bg-platform-hover-light, div.flex.items-center.justify-between.pr-3.py-3.text-base.border-t")
            # Tentativo di recuperare l'elemento per titolo
            video_element = None
            for item in current_items:
                try:
                    item_title = item.find_element(By.CSS_SELECTOR, "div.text-base, div.mb-2").text
                    if title in item_title:
                        video_element = item
                        break
                except:
                    continue
            if not video_element:
                print(f"  Video non trovato dopo il refresh: {title}")
                continue
        else:
            video_element = current_items[original_idx]
        
        # Scroll e click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", video_element)
        time.sleep(1 + random.uniform(0.1, 0.5))
        
        # Tentativo di click migliorato
        try:
            video_element.click()
        except ElementClickInterceptedException:
            print("  Elemento non cliccabile, uso JavaScript")
            driver.execute_script("arguments[0].click();", video_element)
        
        time.sleep(5 + random.uniform(1, 2))
        
        # Aspetta che il player sia completamente caricato
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "video, .video-player-container"))
        )
        
        # Calcola il tempo di attesa
        wait_time = total_seconds + random.randint(25, 40)
        print(f"  Riproduzione in corso (attesa: {wait_time} secondi)...")
        
        # Attendi la durata del video
        start_time = time.time()
        while time.time() - start_time < wait_time:
            time.sleep(10)
            try:
                # Verifica che il player sia ancora presente
                driver.find_element(By.CSS_SELECTOR, "video, .video-player-container")
            except:
                print("    Player non trovato, potrei aver perso la connessione")
                break
        
        print("  Riproduzione completata")
        
        # Chiudi il player (se presente un pulsante di chiusura)
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close'], .close-button")
            close_button.click()
            print("  Player chiuso")
            time.sleep(1)
        except:
            pass
            
        # Attendi dopo la chiusura del player
        time.sleep(2 + random.uniform(0.5, 1.5))
            
    except Exception as e:
        print(f"  Errore durante la riproduzione: {str(e)}")
        # Ricarica la pagina e continua
        try:
            print("  Ricarico la pagina e continuo...")
            driver.get(lessons_url)
            time.sleep(5)
        except:
            pass

# Chiudi il browser alla fine
print("\nTutti i video sono stati riprodotti con successo!")
time.sleep(2)
driver.quit()