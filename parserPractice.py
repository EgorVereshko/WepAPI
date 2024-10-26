import requests
from bs4 import BeautifulSoup
import json

cookies = {
    'stest201': '0',
    'stest207': 'acc1',
    'stest209': 'ct1',
    'user_public_id': 'elt3dz8rMBM%2B%2FAl4mpKmuNfL1x%2BL4M%2BpNB7EE2YkGL89eeg%2FaF%2BIZRUZeLUVd5mc',
    'tp_referrer': 'https%3A%2F%2Fwww.google.com%2F',
    '_gcl_au': '1.1.667691182.1729101945',
    'stDeIdU': '0c585d86-6427-4ecf-ba3f-2cd8462818eb',
    'tmr_lvid': 'bd8022aba2f0539a20f60da455fd270b',
    'tmr_lvidTS': '1729101945889',
    '_ga': 'GA1.1.525944661.1729101946',
    '_ym_uid': '1729101946187504432',
    '_ym_d': '1729101946',
    'uxs_uid': '44633d50-8be9-11ef-9bae-a5cf53ea40e1',
    'afUserId': '78029815-b2e4-4a0e-8585-e58223054fa7-p',
    '_userGUID': '0:m2c6no3i:NbqOTJwSv26~suUtaczKA~v_aEetoThv',
    'promo500closed': 'true',
    'tp_campaign_url': 'https%3A%2F%2Fekaterinburg.technopark.ru%2Fsmartfony%2Fsamsung%2F%3Futm_referrer%3Dhttps%253A%252F%252Fekaterinburg.technopark.ru%252F',
    'qrator_jsr': '1729941871.551.trMXBxPz9vKP2RIo-etgd0e9duis6irm28p3gn1ifej0atgr1-00',
    'qrator_jsid': '1729941871.551.trMXBxPz9vKP2RIo-nbf0779j2o16fjs624qj67di0rnl0vkv',
    'tp_city_id': '36966',
    'PHPSESSID': '3a4743d5108db1f5737d856458ad070f',
    'abTest': '%7B%22w02%22%3A%22w02_0%22%2C%22w05%22%3A%22w05_0%22%2C%22w07%22%3A%22w07_1%22%7D',
    'mindboxDeviceUUID': 'df3296e0-7e28-4031-a63f-d7b152258b79',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22df3296e0-7e28-4031-a63f-d7b152258b79%22%7D',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'domain_sid': 'yyWwXSPxH6gR6zcISHB0t%3A1729941877447',
    'AF_SYNC': '1729941877852',
    'dSesn': '5e59e522-1202-98c8-6294-189a79271830',
    '_dvs': '0:m2q2qa2w:q4bv8qo0ScSKLm8TvMBEcAW5uMdCPF~g',
    '_userGUID': '0:m2c6no3i:NbqOTJwSv26~suUtaczKA~v_aEetoThv',
    'c2d_widget_id': '{%229eb3fbdda817d48faffc65c3446228e8%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%200d62dd4f43cf70e43193%5C%22%2C%5C%22client_token%5C%22:%5C%22ec6713aadbfcaa55533c63e33eefa589%5C%22}%22}',
    'smartSearchUserAllowed': 'true',
    'visitedPagesNumber': '2',
    'tmr_detect': '0%7C1729941895457',
    '_ga_RD4H4CBNJ3': 'GS1.1.1729941876.7.1.1729941895.41.0.0',
    '_ga_010M8X07NE': 'GS1.1.1729941876.8.1.1729941895.41.0.0',
    'rightBanner_763543': '2',
    'pageviewTimer': '23.604',
    'pageviewTimerFired15': 'true',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'stest201=0; stest207=acc1; stest209=ct1; user_public_id=elt3dz8rMBM%2B%2FAl4mpKmuNfL1x%2BL4M%2BpNB7EE2YkGL89eeg%2FaF%2BIZRUZeLUVd5mc; tp_referrer=https%3A%2F%2Fwww.google.com%2F; _gcl_au=1.1.667691182.1729101945; stDeIdU=0c585d86-6427-4ecf-ba3f-2cd8462818eb; tmr_lvid=bd8022aba2f0539a20f60da455fd270b; tmr_lvidTS=1729101945889; _ga=GA1.1.525944661.1729101946; _ym_uid=1729101946187504432; _ym_d=1729101946; uxs_uid=44633d50-8be9-11ef-9bae-a5cf53ea40e1; afUserId=78029815-b2e4-4a0e-8585-e58223054fa7-p; _userGUID=0:m2c6no3i:NbqOTJwSv26~suUtaczKA~v_aEetoThv; promo500closed=true; tp_campaign_url=https%3A%2F%2Fekaterinburg.technopark.ru%2Fsmartfony%2Fsamsung%2F%3Futm_referrer%3Dhttps%253A%252F%252Fekaterinburg.technopark.ru%252F; qrator_jsr=1729941871.551.trMXBxPz9vKP2RIo-etgd0e9duis6irm28p3gn1ifej0atgr1-00; qrator_jsid=1729941871.551.trMXBxPz9vKP2RIo-nbf0779j2o16fjs624qj67di0rnl0vkv; tp_city_id=36966; PHPSESSID=3a4743d5108db1f5737d856458ad070f; abTest=%7B%22w02%22%3A%22w02_0%22%2C%22w05%22%3A%22w05_0%22%2C%22w07%22%3A%22w07_1%22%7D; mindboxDeviceUUID=df3296e0-7e28-4031-a63f-d7b152258b79; directCrm-session=%7B%22deviceGuid%22%3A%22df3296e0-7e28-4031-a63f-d7b152258b79%22%7D; _ym_isad=2; _ym_visorc=b; domain_sid=yyWwXSPxH6gR6zcISHB0t%3A1729941877447; AF_SYNC=1729941877852; dSesn=5e59e522-1202-98c8-6294-189a79271830; _dvs=0:m2q2qa2w:q4bv8qo0ScSKLm8TvMBEcAW5uMdCPF~g; _userGUID=0:m2c6no3i:NbqOTJwSv26~suUtaczKA~v_aEetoThv; c2d_widget_id={%229eb3fbdda817d48faffc65c3446228e8%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%200d62dd4f43cf70e43193%5C%22%2C%5C%22client_token%5C%22:%5C%22ec6713aadbfcaa55533c63e33eefa589%5C%22}%22}; smartSearchUserAllowed=true; visitedPagesNumber=2; tmr_detect=0%7C1729941895457; _ga_RD4H4CBNJ3=GS1.1.1729941876.7.1.1729941895.41.0.0; _ga_010M8X07NE=GS1.1.1729941876.8.1.1729941895.41.0.0; rightBanner_763543=2; pageviewTimer=23.604; pageviewTimerFired15=true',
    'if-none-match': '"13a8db-7OF+RbNTnDLYWi0+qbfna5ubKD4"',
    'priority': 'u=0, i',
    'referer': 'https://www.technopark.ru/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
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

with open("products.json", "w", encoding='utf-8') as f: json.dump(get_all_products(base_url), f, ensure_ascii=False, indent=4)
print(f"Данные успешно записаны в файл products.json")