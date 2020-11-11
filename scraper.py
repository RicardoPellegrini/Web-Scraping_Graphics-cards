import requests
from bs4 import BeautifulSoup

# URL da primeira página das placas de vídeo no site newegg.com
URL = 'https://www.newegg.com/p/pl?d=graphics+card&PageSize=96&page=1'

# Parsing da página HTML
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# Criação do arquivo csv para preenchimento dos dados obtidos
filename = "products.csv"
file = open(filename, 'w')
headers = 'brand,product_name,shipping\n'
file.write(headers)

# Paginação final da lista dos produtos
max_page = int(soup.find(class_='list-tool-pagination-text').strong.text.split('<!-- -->/<!-- -->')[0].split('/')[1])

# Loop por todas as páginas da busca
for i in range(1, max_page + 1):
  updating_URL = f'https://www.newegg.com/p/pl?d=graphics+card&PageSize=96&page={i}'
  page = requests.get(updating_URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  products = soup.findAll(class_="item-container")

  # Loop por todos os itens da página
  for product in products:
    try:
      title = product.find(class_='item-title').text
      brand = product.find(class_='item-branding').a.img['title']
      shipping = product.find(class_='price-ship').text.strip().split()[0]
    except:
      continue

    # Escreve os dados encontrados na linha do arquivo
    file.write(brand + ',' + title.replace(',', '|') + ',' + shipping + "\n")

file.close()