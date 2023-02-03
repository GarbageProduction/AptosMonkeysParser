import json
import re

import requests


class HttpClient:
    def get_html(self, url: str) -> str:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('server error')
        return response.text


class AptosMonkeysRarityParser:
    def __init__(self, http_client: HttpClient) -> None:
        self.__http_client = http_client

    def send_request_to_topaz(self) -> dict:
        request = self.__http_client.get_html(
            'https://api-v1.topaz.so/api/listing-view-p?collection_id=0xf932dcb9835e681b21d2f411ef99f4f5e577e6ac299eebee2272a39fb348f702%3A%3AAptos%20Monkeys&from=0&to=49&sort_mode=PRICE_LOW_TO_HIGH&buy_now=false&page=0&min_price=undefined&max_price=null&filters=')
        return json.loads(request)

    def parse_items(self) -> None:
        data = self.send_request_to_topaz()
        for item in data['data']:
            number = int(re.findall(r'\d+', item['token_name'])[0])
            price = item['price'] * 10 ** -8
            rarity = self.parse_rarity(number)
            print('Number', number, 'Rarity', rarity, 'Price', price)

    def request_to_apt_rarity(self, number: int) -> str:
        request = self.__http_client.get_html(f'https://rarity.aptosmonkeys.club/token/{number}')
        return request

    def parse_rarity(self, number: int) -> int:
        request = self.request_to_apt_rarity(number)
        matches = re.search('Rarity rank:.(?P<rarity>\d+)', request)
        v = matches.groupdict()
        rarity = int(v['rarity'])
        return rarity


def main() -> None:
    http_client = HttpClient()
    aptos_parser = AptosMonkeysRarityParser(http_client)
    aptos_parser.parse_items()


main()
