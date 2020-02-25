import pyqrcode

url = 'URL DO SERVIDOR MAI A ROTA'
product = 'NOME DO PRODUTO CADASTRADO NO BANCO DE DADOS'

# Criar Qrcodes
def create_qr(url,product):
    qr = pyqrcode.create(f'{url}{product}')
    qr.png(f'{product}.png',scale=6)