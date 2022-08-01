# -*- coding: utf-8 -*-
import scrapy
import json
import re


class CasasBahia(scrapy.Spider):
    name = 'casas_bahia'


    def start_requests(self):
        headers = {
            'authority': 'vv-retira-ponto-retirada-api-retira.viavarejo.com.br',
            'accept': '*/*',
            'origin': 'https://www.casasbahia.com.br',
            'referer': 'https://www.casasbahia.com.br/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"'
        }
        url = ('https://vv-retira-ponto-retirada-api-retira.viavarejo.com.br/api/v2/'+
                'Dados/institucional?cep=09520-010&&raioEmKm=10000000&Limit=100000')
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        stores_list = json.loads(response.text)
        for store in stores_list['pontosRetirada']:
            bandeira = store.get('bandeiraFormatada', '')
            if 'Casas Bahia' in bandeira:
                is_open = store.get('aberta', '')
                open = 'Sim' if is_open == True else 'Não'

                cnpj = store.get('cnpj', '')
                addr = store.get('endereco', '')
                regex_addr = re.search(r'(\D.*\,\s\d.*|\D.*\,\s\D.*|\D.*\,\s)\s\-\s(\D.*)\,\s(\D.*)\s\-\s(\D{2})\,\s(\d.*)', str(addr))
                address = regex_addr.group(1).title() if regex_addr else addr
                neigh = regex_addr.group(2).title() if regex_addr else ''
                city = regex_addr.group(3).title() if regex_addr else ''
                state = regex_addr.group(4).upper() if regex_addr else ''
                postal_code = regex_addr.group(5) if regex_addr else ''

                lat = store.get('latitude', '')
                long = store.get('longitude', '')
                store_name = store.get('nomeFormatado', '')

                yield {
                    'Rede': 'Casas Bahia',
                    'Nome Fantasia': store_name,
                    'Logradouro': address,
                    'Bairro': neigh,
                    'Cep': postal_code,
                    'Uf': state,
                    'Municipio': city,
                    'Cnpj': cnpj,
                    'Aberta': open,
                    'Latitude': lat,
                    'Longitude': long
                }
