from requests_html import HTMLSession
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/get-keyword-results/', methods=['GET'])
def get_keyword_results():
    keyword = request.args.get('keyword')
    url = f'https://tools.wordstream.com/fkt?website={keyword}'

    session = HTMLSession()
    r = session.get(url)

    # Render the page, this will execute JavaScript
    r.html.render(sleep=5)  # sleep may be necessary to wait for JS execution

    # Find the 'Continue' button and click it
    continue_button = r.html.find('#refine-continue', first=True)
    if continue_button:
        continue_button.click()
        r.html.render(sleep=5)  # render again if necessary

    # Extract data from the table
    table_data = []
    rows = r.html.find('tbody.sc-hQRsPl.hkwLLR.MuiTableBody-root tr')
    for row in rows:
        cols = row.find('th, td')
        row_data = {
            'keyword': cols[0].text,
            'search_volume': cols[1].text,
            'cpc_low': cols[2].text,
            'cpc_high': cols[3].text,
            'competition': cols[4].text
        }
        table_data.append(row_data)

    # Return the data
    return jsonify(table_data)

if __name__ == '__main__':
    app.run(debug=True)
