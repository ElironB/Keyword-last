from flask import Flask, jsonify, request
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

@app.route('/get-keyword-results/', methods=['GET'])
def get_keyword_results():
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--no-sandbox")  # This make Chromium reachable
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    
    keyword = request.args.get('keyword')
    url = f'https://tools.wordstream.com/fkt?website={keyword}'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    try:
        # Click the 'Continue' button
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'refine-continue'))
        )
        continue_button.click()
        driver.save_screenshot('debug1_screenshot.png')
        print("Button Clicked")

        # Wait for the table to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sc-bTmccw.cFltLW.MuiTable-root'))
        )
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.sc-bczRLJ.jDmpHO.MuiTypography-root'))
        )
        # Extract data from the table
        table_data = []
        rows = driver.find_elements(By.CSS_SELECTOR, 'tbody.sc-hQRsPl.hkwLLR.MuiTableBody-root tr')
        for row in rows:
            cols = row.find_elements(By.CSS_SELECTOR, 'th, td')
            row_data = {
                'keyword': cols[0].text,
                'search_volume': cols[1].text,
                'cpc_low': cols[2].text,
                'cpc_high': cols[3].text,
                'competition': cols[4].text
            }
            table_data.append(row_data)
        return jsonify(table_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
