# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

class CepsBrasil(scrapy.Spider):
    name = 'ceps_brasil'
    start_urls = ['https://cepbrasil.org/']

    def parse(self, response):
        df_list = []
        states_list = response.css('a.box::attr(href)').getall()
        states_name = response.css('div.col-md-4.coluna h4::text').getall()
        for state_l, state_n in zip(states_list, states_name):
            states = requests.get(self.start_urls[0] + state_l.replace('/', '') + '/')
            soup_states = self.beautiful_soup(states.text)
            cities_list = soup_states.find_all('a', 'box')
            for cl in cities_list:
                cities_name = cl.find('h4').string
                cities_url = cl.get('href')
                cities = requests.get(states.url + cities_url + '/')
                soup_cities = self.beautiful_soup(cities.text)
                neigh_list = soup_cities.find_all('a', 'box')
                for nl in neigh_list:
                    neigh_name = nl.find('h4').string
                    neigh_url = nl.get('href')
                    neighs = requests.get(cities.url + neigh_url + '/')
                    soup_neighs = self.beautiful_soup(neighs.text)
                    zipCode_all = soup_neighs.find_all('a', 'box')
                    for item in zipCode_all:
                        regex_zipCode = re.search(r'CEP\s(\d{5}\-\d{3})\s-\s(\D.*)', item.find('h4').string)
                        zip_code = regex_zipCode.group(1) if regex_zipCode else 'Sem informação'
                        address_name = regex_zipCode.group(2) if regex_zipCode else 'Sem informação'
                        df_list.append(pd.DataFrame([
                            {'state': state_n,
                            'city': cities_name,
                            'neighborhood': neigh_name,
                            'zip_code': zip_code,
                            'address': address_name}]
                        ))
        df_one = pd.concat(df_list)
        self.write_data(df_one)

    def beautiful_soup(self, text):
        return BeautifulSoup(text, 'html.parser')
    
    def write_data(self, dataframe):
        dataframe.to_csv('results/ceps_brasil.csv', index=False)
    

''' A implementação do código com muitos fors, não ficou tão performável quanto o esperado.
Minha outra solução seria escrever cada estado em um bucket no s3 e ao final da execução,
unir todos os arquivos em um único, para visualização completa dos dados. Porém essa
solução poderia ficar ainda melhor se tirassemos o robô da lib do scrapy.'''