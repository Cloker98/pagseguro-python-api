from typing import List, Optional
import requests
import json

from datetime import date

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Data.Subscriber import Subscriber
from Data.Phone import Phone 
from Data.Address import Address
from Data.BillingInfo import BillingInfo
from Data.CardHolder import CardHolder
from Data.Card import Card

class SubscriberService:
     # Formato base para a data e hora
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"  # Sem milissegundos e timezone por padrão
    def __init__(self, base_url: str, token: str):
        """
        Inicializa o serviço para enviar pedidos de criação de QRCode de PIX.

        :param base_url: URL base do serviço.
        :param token: Token de autorização.
        """
        self.service_url = Util.validate_url(f"{base_url}/customers")
        self.token = token
        self.headers = {
            "accept": "application/json",
            "Authorization": f'Bearer {self.token}',
            "content-Type": "application/json"
        }
            
    def create_subscriber(self, subscriber: Subscriber):
        """
        Envia uma requisição para criar um QRCode de PIX e retorna o JSON de resposta.

        :param order: Objeto PixOrder a ser enviado.
        :return: Resposta da API em formato JSON.
        :raises RuntimeError: Quando ocorre algum erro na requisição.
        """
        try:
            # Serializa o objeto PixOrder para JSON, tratando o datetime
            #json_body = json.dumps(subscriber.to_dict(), indent=4)
            json_body = json.dumps(subscriber.to_dict(), ensure_ascii=False, indent=4)
            print(type(json_body))
            
            self.print_request("POST", self.service_url, self.headers, json_body)

            # Faz a requisição POST (a lógica de requisição continua a mesma)
            response = requests.post(url=self.service_url, headers=self.headers, data=json_body)
            #response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            # Verifica se a resposta contém conteúdo antes de fazer parsing
            #if response.text:
                #return response.json()  # Tenta converter o conteúdo para JSON
            #print(response.json())
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def check_subscriber_by_id(self, subscriber_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/customers/{subscriber_id}")
        try:
            self.print_request(method="GET", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.get(url=service_url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def list_subscribers(self, offset: int, limit: int, reference_id: str):
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/customers?offset={offset}&limit={limit}&reference_id={reference_id}")
        try:
            self.print_request(method="GET", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.get(url=self.service_url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def change_subscriber_personal_data(self, subscriber_id: str, subscriber: Subscriber):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/customers/{subscriber_id}")
        try:
            json_body = json.dumps(subscriber.to_dict(), ensure_ascii=False, indent=4)
            print(json_body)
            self.print_request(method="PUT", url=service_url, headers=self.headers, json_body=json_body)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers, data=json_body)
            #response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
    
    def change_subscriber_billing_info(self, subscriber_id: str, billing_info: List[BillingInfo]):
        #plan_id = SignaturePlan.
        billing_info = Util.get_list(billing_info if billing_info else [])
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/customers/{subscriber_id}/billing_info")
        try:
            json_body = json.dumps([billing.to_dict() for billing in billing_info], ensure_ascii=False, indent=4)
            print(json_body)
            self.print_request(method="PUT", url=service_url, headers=self.headers, json_body=json_body)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers, data=json_body)
            #response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")

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

    # Função fora da Classe para testar a Classe
def exemplo():
    #service = PixOrderService(base_url="https://example.com", token="your_token_here")
    service = SubscriberService(base_url="https://sandbox.api.assinaturas.pagseguro.com/", token="")
    phone_example = Phone("55", "11", "123456789", "MOBILE")
    # Exemplo de BillingInfo
    card_holder = CardHolder(name="João Silva", birth_date="1985-04-20", tax_id="92410172016", phone=phone_example)
    card = Card(number="5134651357093747", security_code=123, exp_year="2026", exp_month="12", holder=card_holder)
    card2 = Card(number="4012001037141112", security_code=123, exp_year="2026", exp_month="12", holder=card_holder)
    billing_info = BillingInfo(type="CREDIT_CARD", card=card) 
    new_billing_info=BillingInfo(type="CREDIT_CARD", card=card2)
    address = Address(street="Rua Exemplo", number="123", complement="Apto 45", locality="Centro", city="São Paulo", region_code="SP", country="BRA",postal_code="12345-678")
    subscriber = Subscriber(name="João Silva", email="joao.silva@example.com", tax_id="01234567890", address=address, phones=[phone_example], reference_id="ex-00001", birth_date=date(2000, 12, 20), billing_info=[billing_info])
    new_personal_data = Subscriber(name="Pablo Marçãl", email="pablo.marcal@example.com", address=address, phones=[phone_example], reference_id="ex-00001", birth_date=date(2000, 12, 20)) # Não pode alterar o CPF/CNPJ
    #new_subscriber_billing_info = Subscriber(billing_info=[new_billing_info])
    subscriber_id = "CUST_DAE9DC8D-542C-43F1-B6FA-DC923B3925C2"
    # Criar Plano
    try:
        #response_order = service.create_subscriber(subscriber) # Criar um assinante
        #response_order = service.check_subscriber_by_id(subscriber_id) # Busca um assinante pelo id
        #response_order = service.list_subscribers(0,100,"ex-00001") # Lista os assinantes pelos parametros passados
        #response_order = service.change_subscriber_personal_data(subscriber_id, new_personal_data) # Atualiza um assinante existente com novos dados pessoais
        response_order = service.change_subscriber_billing_info(subscriber_id, [new_billing_info]) # Atualiza um assinante existente com novas informações de cobrança
        
        print(response_order)
    except RuntimeError as e:
        print(e)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()