Projeto criado para publicações de robôs de scraping em forma de estudo e aprimoramento de conceitos.
----
### Tecnologias usadas:
- python
  - biblioteca Scrapy
  - biblioteca Json
  - biblioteca Regex
  - biblioteca Unidecode
  - biblioteca Pandas
----
### Robôs já criados:
- Yamaha - concessionária
- Casas Bahia - artigos diversos
- Nacional Supermercado - varejo alimentício
----
#### Para rodar o robô:
- fazer o git clone do projeto
- abrir o terminal
  - _caso precise, instale o arquivo requirements.txt para usufruir de módulos instalavéis_
  - ***pip install -r requirements.txt***
- dentro da pasta "robos" dar o comando: **scrapy crawl <nome do robô> -o results/out.csv** 
  - ex: ***scrapy crawl yamaha -o results/out.csv***
-  _extra1_: para que os arquivos csv não sejam sobrescritos, pode ser feito a alteração do nome para o desejado "_scrapy crawl yamaha -o **nome_qualquer.csv**_"
- _extra2_: caso queiram visualizar o csv gerado, aconselho a instalação da extensão do vscode **edit csv**