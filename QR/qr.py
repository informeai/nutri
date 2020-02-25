import pyqrcode

url = 'nutri-informeai.herokuapp.com/products/'
product = 'tortaconfeitada'

# Criar Qrcodes
def create_qr(url,product):
    qr = pyqrcode.create(f'{url}{product}')
    qr.png(f'{product}.png',scale=6)

if __name__ == '__main__':
    create_qr(url,product)