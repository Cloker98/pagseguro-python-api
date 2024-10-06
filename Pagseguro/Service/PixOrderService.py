from typing import Optional
import requests
import json
from datetime import datetime, timedelta

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Service.PixOrder import PixOrder
from Data.QrCode import QrCode
from Data.Customer import Customer
from Data.Item import Item
from Data.Phone import Phone

class PixOrderService:
    # Formato base para a data e hora
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"  # Sem milissegundos e timezone por padrão
    def __init__(self, base_url: str, token: str):
        """
        Inicializa o serviço para enviar pedidos de criação de QRCode de PIX.

        :param base_url: URL base do serviço.
        :param token: Token de autorização.
        """
        self.service_url = Util.validate_url(f"{base_url}/orders")
        self.token = token
        self.headers = {
            "accept": "*/*",
            "Authorization": f'Bearer {self.token}',
            "content-Type": "application/json"
        }
        
    def send(self, order: PixOrder):
        """
        Envia uma requisição para criar um QRCode de PIX e retorna o JSON de resposta.

        :param order: Objeto PixOrder a ser enviado.
        :return: Resposta da API em formato JSON.
        :raises RuntimeError: Quando ocorre algum erro na requisição.
        """
        try:
            # Serializa o objeto PixOrder para JSON, tratando o datetime
            #json_body = json.dumps(order, default=self.json_serializer, indent=4)
            json_body = json.dumps(order.to_dict(), indent=4)
            print(json_body)
            self.print_request("POST", self.service_url, self.headers, json_body)

            # Faz a requisição POST (a lógica de requisição continua a mesma)
            response = requests.post(url=self.service_url, headers=self.headers, data=json_body)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
    
    @staticmethod
    def json_serializer(obj):
        """
        Serializa objetos que não são serializáveis por padrão no JSON, como objetos datetime.

        :param obj: Objeto a ser serializado.
        :return: Objeto serializado como string ou dicionário.
        """
        if isinstance(obj, datetime):
            # Formatando para "YYYY-MM-DDTHH:MM:SS.fff±hh:mm"
            formatted_date = obj.strftime(PixOrderService.DATE_TIME_FORMAT)  # Parte básica da data
            milliseconds = f"{obj.microsecond // 1000:03d}"  # Obtém milissegundos
            timezone = obj.strftime('%z')  # Obtém o timezone
            timezone_formatted = f"{timezone[:3]}:{timezone[3:]}"  # Formata o timezone para ±hh:mm
            return f"{formatted_date}.{milliseconds}{timezone_formatted}"  # Combina tudo

        if isinstance(obj, QrCode):
            # Customiza a serialização do QRCode
            '''
            "expiration_date": obj.expiration_date.strftime(PixOrderService.DATE_TIME_FORMAT) + \
                                  f".{obj.expiration_date.microsecond // 1000:03d}" + \
                                  obj.expiration_date.strftime('%z')[:3] + ':' + \
                                  obj.expiration_date.strftime('%z')[3:]
            '''
            '''
            return {
                "amount": {"value": obj.amount},
                "expiration_date": obj.expiration_date.strftime(PixOrderService.DATE_TIME_FORMAT) + \
                                f".{obj.expiration_date.microsecond // 1000:03d}" + \
                                obj.expiration_date.strftime('%z')[:3] + '-03:00' #+ \
                                # obj.expiration_date.strftime('%z')[3:]
            }
        return {key: value for key, value in obj.__dict__.items() if value is not None}
        '''
            return {
                "id": obj.id,
                "amount": {"value": obj.amount},
                "expiration_date": obj.expiration_date.strftime(PixOrderService.DATE_TIME_FORMAT),
                "text": obj.text,
                "arrangements": obj.arrangements or [],
                "links": [
                    {
                        "rel": link.rel,
                        "href": link.href,
                        "media": link.media,
                        "type": link.type
                    }
                    for link in obj.links
                ] if obj.links else []
            }
        return {key: value for key, value in obj.__dict__.items() if value is not None}

    '''
    @staticmethod
    def print_request(method: str, url: str, headers: dict, json_body: str):
        """
        Imprime o comando cURL equivalente à requisição HTTP.

        :param method: Método HTTP (GET, POST, etc.).
        :param url: URL da requisição.
        :param headers: Cabeçalhos da requisição.
        :param json_body: Corpo da requisição em JSON.
        """
        print("Request")
        print(f"curl --location --request {method} {url} \\")
        PixOrderService.print_header(headers, "Authorization", "-H ")
        print("-H 'Content-Type: application/json' \\")
        print(f"--data-raw '{json_body}'")
        print()
    '''
    @staticmethod
    def print_request(method: str, url: str, headers: dict, json_body: Optional[str] = None):
        """
        Imprime o comando cURL equivalente à requisição HTTP.

        :param method: Método HTTP (POST).
        :param url: URL da requisição.
        :param headers: Cabeçalhos da requisição.
        :param json_body: Corpo da requisição em JSON.
        """
        print("Request")
        print(f"curl --location --request {method} {url} \\")
        for key, value in headers.items():
            print(f"-H '{key}: {value}' \\")
        if(json_body):
            print(f"--data-raw '{json_body}'")
        print()

    @staticmethod
    def print_header(headers: dict, header_name: str, prefix: str = ""):
        """
        Imprime um cabeçalho da requisição.

        :param headers: Cabeçalhos da requisição.
        :param header_name: Nome do cabeçalho a ser impresso.
        :param prefix: Prefixo para o cabeçalho.
        """
        value = headers.get(header_name)
        if value:
            print(f"{prefix}{header_name}: {value}")

    @staticmethod
    def print_response(response: requests.Response):
        """
        Imprime detalhes da resposta HTTP.

        :param response: Resposta da requisição.
        """
        print("Response")
        print(f"Status Code: {response.status_code}")
        print(response.text)
        print()
        
    '''
    @staticmethod
    def print_response(response: requests.Response):
        """
        Imprime detalhes da resposta HTTP.

        :param response: Resposta da requisição.
        """
        print("Response")
        PixOrderService.print_header(response.headers, ":status")
        PixOrderService.print_header(response.headers, "content-type")
        print()
        print(response.text)
        print()
    '''

# Função fora da Classe para testar a Classe
def exemplo():
    #service = PixOrderService(base_url="https://example.com", token="your_token_here")
    service = PixOrderService(base_url="https://sandbox.api.pagseguro.com/", token="")
 
    # Criando uma instância de PixOrder para teste
    #phone_example1 = Phone(area="11", number="123456789")  # Supondo que exista uma implementação da classe Phone
    #phone_example2 = Phone(area="21", number="987654321")  # Supondo que exista uma implementação da classe Phone
    #phones = [phone_example1, phone_example2]
    #customer = Customer(name="John Doe", email="john@example.com", tax_id="12345678909", phones=phones)
    customer = Customer(name="John Doe", email="john@example.com", tax_id="92410172016")
    item = Item(name="Test Item", unit_amount=1000, quantity=2)
    #expiration_date = datetime.strptime("2021-08-29T20:15:59-03:00", QrCode.DATE_TIME_FORMAT)
    expiration_date = datetime.now() + timedelta(days=3) # Data de expiração futura (3 dias no futuro)
    #qrcode = QrCode(id="123", text="Copia e Cola", amount=500, expiration_date=expiration_date)
    qrcode = QrCode(amount=500, expiration_date=expiration_date)  # Passando expiration_date como objeto datet
    pix_order = PixOrder(reference_id="ref123", customer=customer, qrcode=qrcode, notification_url="http://example.com/notify", items=[item])
    # Enviar pedido
    try:
        response_order = service.send(pix_order)
        print(response_order)
    except RuntimeError as e:
        print(e)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()