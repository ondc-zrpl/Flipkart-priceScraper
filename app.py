from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

app = Flask(__name__)

def get_product_details(pid, lid):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
    }

    print(f"Using User-Agent: {headers['User-Agent']}")

    url = f'https://www.flipkart.com/brooks-launch-9-running-shoes-men/p/itmc1fa98405e951?pid={pid}&lid={lid}'
    response = requests.get(url, headers=headers)
    print("response is", response)
    if response.status_code != 200:
        return {
            'error': f"Request failed with status code {response.status_code}."
        }    

    soup = BeautifulSoup(response.content, 'html.parser')

    # Product name
    product_name = soup.find('span', {'class': 'VU-ZEz'}).text

    # Product Price
    price_tag = soup.find('div', {'class': 'Nx9bqj CxhGGd'})
    product_price = '0'
    if price_tag:
        product_price = price_tag.text.replace('₹', '').replace(',', '')
        product_price = float(product_price)

    # Image URL
    image_tag = soup.find('img', {'class': 'DByuf4 IZexXJ jLEJ7H'})
    image_url = ''
    if image_tag and 'src' in image_tag.attrs:
        image_url = image_tag['src']

    return {
        'title': product_name,
        'price': product_price,
        'image_url': image_url
    }

@app.route('/get_product_info', methods=['GET'])
def get_product_info():
    pid = request.args.get('pid')
    lid = request.args.get('lid')

    if not pid or not lid:
        return jsonify(error='Both "pid" and "lid" parameters are required.'), 400

    product_info = get_product_details(pid, lid)
    return jsonify(product_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
