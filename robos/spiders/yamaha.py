# -*- coding: utf-8 -*-
import scrapy
import json


class YamahaSpider(scrapy.Spider):
    name = 'yamaha'
    start_urls = ['https://www3.yamaha-motos.com.br/concessionarias']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Ocp-Apim-Subscription-Key': '11a79400519c4bac879b4001d1e7bdb4',
        'Content-Type': 'application/json',
    }

    def start_requests(self):
        with open('robos/spiders/resources/estados_brasileiros.json', 'r') as file:
            arq_json = json.load(file)
        for item in arq_json:
            state = item.get('uf')
            url = (
                'https://gwapi.yamaha-motor.com.br/cloud-services/api/cloud-consultas/seller-locate'+
                f'?uf={state}&city='
            )
            yield scrapy.Request(url, headers=self.headers, callback=self.get_cities)

    def get_cities(self, response):
        cities_list = json.loads(response.text)['data']
        for cities in cities_list:
            state = cities.get('uf', '')
            city = cities.get('city', '')
            url = (
                'https://gwapi.yamaha-motor.com.br/cloud-services/api/cloud-consultas/seller-locate'+
                f'?uf={state}&city={city}'
            )
            yield scrapy.Request(url, headers=self.headers, callback=self.get_units)

    def get_units(self, response):
        stores_list = json.loads(response.text)
        for store in stores_list['data']:
            address = store.get('address', '')
            postal_code = store.get('cep', '')
            city = store.get('city', '')
            cnpj = store.get('cnpj', '')
            ddd = store.get('ddd', '')
            nid = store.get('id', '')
            lat = store.get('lat', '')
            long = store.get('lng', '')
            neigh = store.get('neighborhood', '')
            phone = store.get('phone', '')
            unit_name = store.get('trade_name', '')
            state = store.get('uf', '')

            yield {
                'Rede': 'Yamaha',
                'Nome Fantasia': unit_name,
                'Logradouro': address,
                'Bairro': neigh,
                'Cep': postal_code,
                'Ddd': ddd,
                'Telefone': phone,
                'Uf': state,
                'Municipio': city,
                'Codigo Unidade': nid,
                'Cnpj': cnpj,
                'Latitude': lat,
                'Longitude': long
            }
