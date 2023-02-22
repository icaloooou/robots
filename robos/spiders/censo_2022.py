# -*- coding: utf-8 -*-
import scrapy
import requests
import pandas as pd

# DOWNLOAD DATA
class Censo2022(scrapy.Spider):
    name = 'censo_2022'
    start_urls = ['https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Previa_da_Populacao/']

    def parse(self, response):
        all_ = response.css('a:contains(xls)::attr(href)').getall()
        if len(all_) > 1:
            file = ''
        file = response.css('a:contains(xls)::attr(href)').get()

        r = requests.get(self.start_urls[0] + file)
        file = open("municipios.xls", "wb")
        file.write(r.content)
        file.close()

        # TREATMENT
        columns = ['UF', 'COD_UF', 'COD_MUN', 'NOME_MUN', 'POP']
        datum = pd.read_excel('municipios.xls', sheet_name='Municípios', skiprows=2, skipfooter=34, header=None, names=columns)
        data_ = datum.replace(to_replace=r'\(\d.*\)', value='', regex=True)
        data_ = data_.replace(to_replace=r'\.', value='', regex=True)

        # AVAILABILITY DATA
        data_.to_csv('results/censo.csv', index=False)
