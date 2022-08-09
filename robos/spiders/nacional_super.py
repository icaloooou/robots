# -*- coding: utf-8 -*-
import scrapy
import re
from unidecode import unidecode


class NacionalSupermercadoSpider(scrapy.Spider):
    name = 'nacional_super'
    start_urls = ['https://folhetosnacional.com.br/horario/']

    def parse(self, response):
        link_list = response.css('a.btn::attr(href)').getall()
        for link in link_list[3:]:
            url = 'https://folhetosnacional.com.br' + link
            yield scrapy.Request(url, callback=self.get_stores,
                                    meta={'link': link})

    def get_stores(self, response):
        meta = response.meta
        store_name = (response.css('p.text-blue.text-truncate.d-inline-block.fz-lg'+
                        '.font-bold.lh-1.mb-0 strong::text').get().replace('-', ' '))
        addr = response.css('strong.text-address__two-line::text').get().strip()
        address = addr.split('-')[0].strip() if '-' in addr else addr
        neigh = addr.split('-')[1].strip() if '-' in addr else ''
        city_state = (meta['link'].replace('-', ' ').title()
                        .replace(unidecode(store_name).title(), '')
                        .replace('Lojas', '').replace('/', '').strip())
        regex_city_state = re.search(r'(\D.*) (\D{2})', str(city_state))
        city = regex_city_state.group(1) if regex_city_state else ''
        state = regex_city_state.group(2) if regex_city_state else ''

        yield {
            'Rede': 'Nacional Supermercado',
            'Nome Fantasia': store_name,
            'Logradouro': address,
            'Bairro': neigh,
            'Uf': state.upper(),
            'Municipio': city
        }
