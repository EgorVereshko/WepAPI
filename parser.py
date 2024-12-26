import requests
from bs4 import BeautifulSoup

cookies = {
    'stest201': '0',
    'stest207': 'acc0',
    'stest209': 'ct2',
    'tp_city_id': '38109',
    'user_public_id': 'Iti%2FL%2BgtFfMaNvN%2BxzXj4sxCG022nUyLpFD5ktDGmFSRGYpGasdFmCWm75FweRZJ',
    'abTest': '%7B%22w02%22%3A%22w02_1%22%2C%22w05%22%3A%22w05_0%22%2C%22w06%22%3A%22w06_2%22%2C%22w07%22%3A%22w07_1%22%7D',
    '_gcl_au': '1.1.370209368.1732723351',
    '_ga': 'GA1.1.1599991396.1732723352',
    'tmr_lvid': 'bd8022aba2f0539a20f60da455fd270b',
    'tmr_lvidTS': '1729101945889',
    '_ym_uid': '1729101946187504432',
    '_ym_d': '1732723352',
    'afUserId': '78029815-b2e4-4a0e-8585-e58223054fa7-p',
    '_userGUID': '0:m402qxhh:aCbjHrmsrRYryjnrsCTuO2bbeMbKAXJq',
    'c2d_widget_id': '{%229eb3fbdda817d48faffc65c3446228e8%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%201ff033a32b37423c3c1e%5C%22%2C%5C%22client_token%5C%22:%5C%227b1781a05f62bccdaf0b8151ab808333%5C%22}%22}',
    'promo500closed': 'true',
    'stDeIdU': '28bfe406-f31c-46f1-9d15-91f2028d21b4',
    '_userGUID': '0:m402qxhh:aCbjHrmsrRYryjnrsCTuO2bbeMbKAXJq',
    'digi_uc': '|v:173272:150006|s:173272:149833',
    'AF_SYNC': '1734096289353',
    'qrator_jsr': '1734544476.328.0YLTs74Hp1gBNwUz-q9830jhp85kt367nv8vmvk02ni4ega35-00',
    'qrator_jsid': '1734544476.328.0YLTs74Hp1gBNwUz-rh7ii7nrgd260pqcplrbhbl8tr9o8fgb',
    'mindboxDeviceUUID': 'b4c866f4-1bb3-4298-b001-ae0c732598ca',
    'PHPSESSID': 'a4a937631ad3e94eb3888aabfc2e120d',
    'visitedPagesNumber': '1',
    'headerTopper_768758': '1',
    '_ym_isad': '2',
    'domain_sid': '28SU-Hrnzf20cbWT4e20y%3A1734544484479',
    '_ym_visorc': 'w',
    '_ga_010M8X07NE': 'GS1.1.1734544483.12.0.1734544489.54.0.0',
    '_ga_RD4H4CBNJ3': 'GS1.1.1734544484.12.0.1734544489.55.0.0',
    'tmr_detect': '0%7C1734544490011',
    'pageviewTimer': '8.089',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'stest201=0; stest207=acc0; stest209=ct2; tp_city_id=38109; user_public_id=Iti%2FL%2BgtFfMaNvN%2BxzXj4sxCG022nUyLpFD5ktDGmFSRGYpGasdFmCWm75FweRZJ; abTest=%7B%22w02%22%3A%22w02_1%22%2C%22w05%22%3A%22w05_0%22%2C%22w06%22%3A%22w06_2%22%2C%22w07%22%3A%22w07_1%22%7D; _gcl_au=1.1.370209368.1732723351; _ga=GA1.1.1599991396.1732723352; tmr_lvid=bd8022aba2f0539a20f60da455fd270b; tmr_lvidTS=1729101945889; _ym_uid=1729101946187504432; _ym_d=1732723352; afUserId=78029815-b2e4-4a0e-8585-e58223054fa7-p; _userGUID=0:m402qxhh:aCbjHrmsrRYryjnrsCTuO2bbeMbKAXJq; c2d_widget_id={%229eb3fbdda817d48faffc65c3446228e8%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%201ff033a32b37423c3c1e%5C%22%2C%5C%22client_token%5C%22:%5C%227b1781a05f62bccdaf0b8151ab808333%5C%22}%22}; promo500closed=true; stDeIdU=28bfe406-f31c-46f1-9d15-91f2028d21b4; _userGUID=0:m402qxhh:aCbjHrmsrRYryjnrsCTuO2bbeMbKAXJq; digi_uc=|v:173272:150006|s:173272:149833; AF_SYNC=1734096289353; qrator_jsr=1734544476.328.0YLTs74Hp1gBNwUz-q9830jhp85kt367nv8vmvk02ni4ega35-00; qrator_jsid=1734544476.328.0YLTs74Hp1gBNwUz-rh7ii7nrgd260pqcplrbhbl8tr9o8fgb; mindboxDeviceUUID=b4c866f4-1bb3-4298-b001-ae0c732598ca; PHPSESSID=a4a937631ad3e94eb3888aabfc2e120d; visitedPagesNumber=1; headerTopper_768758=1; _ym_isad=2; domain_sid=28SU-Hrnzf20cbWT4e20y%3A1734544484479; _ym_visorc=w; _ga_010M8X07NE=GS1.1.1734544483.12.0.1734544489.54.0.0; _ga_RD4H4CBNJ3=GS1.1.1734544484.12.0.1734544489.55.0.0; tmr_detect=0%7C1734544490011; pageviewTimer=8.089',
    'if-none-match': '"16873d-IGjZkk9zvaGQDN2u2yiuBvwU/ik"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
}

base_url = "https://ekaterinburg.technopark.ru/smartfony/samsung/"

def get_products(url):
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    products = []
    for product in soup.find_all("div", class_="product-card-big"):
        title = product.find("div", class_="product-card-big__name").get_text().strip()
        price_text = product.find("div", class_="product-prices__price").get_text()
        price = int("".join(filter(str.isdigit, price_text[:price_text.find('₽')].strip())))
        products.append({
            "Название": title,
            "Цена": price
        })
    return products

def get_all_products(base_url):
    all_products = []
    for page_number in range(1, 8):
        url = f"{base_url}?p={page_number}"
        products = get_products(url)
        if products:
            all_products.extend(products)
    return all_products