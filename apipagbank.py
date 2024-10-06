#python -m pip install requests
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Classes de serviço e dados
from Pagseguro.Service.PixOrderService import PixOrderService
from Pagseguro.Data.Customer import Customer
from Pagseguro.Data.Item import Item
from Pagseguro.Data.QrCode import QrCode
from Pagseguro.Service.PixOrder import PixOrder
from Pagseguro.Service.Response.ResponseError import ResponseError
from Pagseguro.Service.Response.Link import Link
#from Pagseguro.Util import Util

# Carrega as variáveis de ambiente do arquivo .env
# Exemplo de uso
#dotenv_path = Util.find_dotenv_file()
#print(dotenv_path)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if not load_dotenv(dotenv_path):
#if not load_dotenv():
    print("Arquivo .env não foi carregado corretamente.")

# variáveis de ambiente do banco de dados
'''
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
USERSERVER = os.getenv("USERSERVER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
'''

# variáveis de ambiente do gateway de pagamento
TOKEN = os.getenv("PAYMENT_SERVICE_TOKEN")
BASE_URL = os.getenv("PAYMENT_SERVICE_URL")
NOTIFICATION_URL = os.getenv("PAYMENT_NOTIFICATION_URL")
REFERENCE_ID = os.getenv("PAYMENT_REFERENCE_ID")

#print(BASE_URL)
#print(TOKEN)
#print(NOTIFICATION_URL)
#print(REFERENCE_ID)

class AppSample:
    # CPF válido gerado aleatoriamente
    CPF_CNPJ_CLIENTE = "14880686077"

    @staticmethod
    def main():
        base_url = os.getenv("PAYMENT_SERVICE_URL")
        token = os.getenv("PAYMENT_SERVICE_TOKEN")
        notification_url = os.getenv("PAYMENT_NOTIFICATION_URL")
        reference_id = os.getenv("PAYMENT_REFERENCE_ID")

        print(base_url)
        print(token)
        print(notification_url)
        print(reference_id)

        #service = PixOrderService(base_url, token)
        service = PixOrderService(BASE_URL, TOKEN)
        customer = Customer("Manoel", "teste@teste.com", AppSample.CPF_CNPJ_CLIENTE)
        item = Item(name="Test Item", unit_amount=1000, quantity=2)
        expiration_date = datetime.now() + timedelta(days=3) # Data de expiração futura (3 dias no futuro)
        #expiration_date_iso = expiration_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '-03:00'  # Incluindo o fuso horário
        qrcode = QrCode(id="123", text="Copia e Cola", amount=500, expiration_date=expiration_date)
        request = PixOrder(reference_id=reference_id, customer=customer, qrcode=qrcode, notification_url=notification_url, items=[item])

        try:
            response = service.send(request)
            AppSample.print_response(response)
        except ResponseError as e:
            print("Erro ao processar requisição")
            for error_message in e.error_messages():
                print(error_message)

    @staticmethod
    def print_response(response):
        print(f"Order reference_id: {response['reference_id']}")
        print(f"QRCode id: {response['id']}")
        print(f"created_at: {response['created_at']}")
        print(f"customer: {response['customer']}")
        AppSample.print_links(response['links'], "")
        for url in response['notification_urls']:
            print(url)
        for qr_code in response['qr_codes']:
            AppSample.print_qr_code(qr_code)

    @staticmethod
    def print_qr_code(code):
        print("QRCode:")
        print(f"\tid: {code['id'] if 'id' in code else 'ID not available'}")  # Corrigido para acessar o dicionário
        print(f"\ttext: {code.get('text', 'Text not available')}")  # Usando .get() para acessar chaves opcionais
        print(f"\texpiration_date: {code['expiration_date']}")
        print(f"\tarrangements: {code.get('arrangements', 'Arrangements not available')}")
        AppSample.print_links(code['links'], "\t")

    @staticmethod
    def print_links(links: List[Link], indent: str):
        print(f"{indent}links:")
        for link in links:
            print(f"{indent}\t{link}")

if __name__ == "__main__":
    AppSample.main()