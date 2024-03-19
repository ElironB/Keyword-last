from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/get-keyword-results/', methods=['GET'])
def get_keyword_results():
    keyword = request.args.get('keyword')
    url = f'https://tools.wordstream.com/fkt?website={keyword}'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        try:
            page.click("#refine-continue")
            print("Button Clicked")

            page.wait_for_selector('table.sc-bTmccw.cFltLW.MuiTable-root', timeout=20000)
            page.wait_for_selector('p.sc-bczRLJ.jDmpHO.MuiTypography-root', state='hidden', timeout=20000)
            print("Table Loaded")

            table_data = []
            rows = page.query_selector_all('tbody.sc-hQRsPl.hkwLLR.MuiTableBody-root tr')
            for row in rows:
                cols = row.query_selector_all('th, td')
                row_data = {
                    "keyword": cols[0].inner_text(),
                    "search_volume": cols[1].inner_text(),
                    "cpc_low": cols[2].inner_text(),
                    "cpc_high": cols[3].inner_text(),
                    "competition": cols[4].inner_text()
                }
                table_data.append(row_data)

            if table_data:
                return jsonify(table_data)
            else:
                return jsonify({'Failed to extract data :('}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            browser.close()

if __name__ == '__main__':
    # Set the FLASK_ENV environment variable to 'development' to enable debug mode
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
