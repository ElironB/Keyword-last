from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/get-keyword-results/', methods=['GET'])
def get_keyword_results():
    keyword = request.args.get('keyword')
    url = f'https://tools.wordstream.com/fkt?website={keyword}'
    table_data = []  # Initialize outside try-except

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

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500

        finally:
            browser.close()

    if table_data:
        return jsonify(table_data)
    else:
        return jsonify({'message': 'Failed to extract data'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
