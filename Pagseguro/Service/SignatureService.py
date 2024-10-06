from typing import List, Optional
import requests
import json

from datetime import date

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Data.Signature import Signature, BestInvoiceData
from Data.SignaturePaymentMethod import SignaturePaymentMethod
from Data.Amount import Amount
from Service.SignaturePlan import SignaturePlan
from Service.Response.Link import Link
# Informações do Assinante
from Data.Subscriber import Subscriber
from Data.Phone import Phone 
from Data.Address import Address
from Data.BillingInfo import BillingInfo
from Data.CardHolder import CardHolder
from Data.Card import Card

class SignatureService:
     # Formato base para a data e hora
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"  # Sem milissegundos e timezone por padrão
    def __init__(self, base_url: str, token: str):
        """
        Inicializa o serviço para enviar pedidos de criação de QRCode de PIX.

        :param base_url: URL base do serviço.
        :param token: Token de autorização.
        """
        self.service_url = Util.validate_url(f"{base_url}/subscriptions")
        self.token = token
        self.headers = {
            "accept": "application/json",
            "Authorization": f'Bearer {self.token}',
            "content-Type": "application/json"
        }
            
    def create_signature(self, signature: Signature):
        """
        Envia uma requisição para criar um QRCode de PIX e retorna o JSON de resposta.

        :param order: Objeto PixOrder a ser enviado.
        :return: Resposta da API em formato JSON.
        :raises RuntimeError: Quando ocorre algum erro na requisição.
        """
        try:
            # Serializa o objeto PixOrder para JSON, tratando o datetime
            #json_body = json.dumps(subscriber.to_dict(), indent=4)
            json_body = json.dumps(signature.to_dict(), ensure_ascii=False, indent=4)
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
        
    def check_signature_by_id(self, signature_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}")
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
        
    def list_signatures(self, reference_id: Optional[str] = None, status: Optional[List[str]] = None, payment_method_type: Optional[List[str]]= None, created_at_start: Optional[date]=None, created_at_end: Optional[date]=None):
        # URL base
        base_url = "https://sandbox.api.assinaturas.pagseguro.com/subscriptions?"
        
        # Lista de parâmetros da URL
        params = []
        
        # Se `status` for uma lista, adicione cada status como um parâmetro separado
        if status:
            params += [f"Status={s}" for s in status]
        
        # Se `payment_method_type` for uma lista, adicione cada tipo de pagamento como um parâmetro separado
        if payment_method_type:
            params += [f"payment_method_type={pmt}" for pmt in payment_method_type]
        
        # Adiciona `created_at_start` e `created_at_end` se forem fornecidos
        if created_at_start:
            params.append(f"created_at_start={created_at_start}")
        if created_at_end:
            params.append(f"created_at_end={created_at_end}")
        
        # Adiciona `reference_id` se for fornecido
        if reference_id:
            params.append(f"reference_id={reference_id}")
        
        # Monta a URL final com os parâmetros
        service_url = base_url + "&".join(params)
        
        # Validação da URL
        service_url = Util.validate_url(service_url)

        try:
            self.print_request(method="GET", url=service_url, headers=self.headers)
            
            # Faz a requisição GET
            response = requests.get(url=service_url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def list_subscribers_invoice(self, signature_id: str, offset: Optional[int] = None, limit: Optional[int] = None, status: Optional[List[str]] = None):
         # URL base
        base_url = f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}/invoices?"
        
        # Lista de parâmetros da URL
        params = []
        
        # Se `status` for uma lista, adicione cada status como um parâmetro separado
        if status:
            params += [f"status={s}" for s in status]
        else:
            params.append("status=PAID%2CUNPAID%2CWAITING%2COVERDUE")
        
        # Adiciona `created_at_start` e `created_at_end` se forem fornecidos
        if offset:
            params.append(f"offset={offset}")
        else:
            params.append("offset=0")

        if limit:
            params.append(f"limit={limit}")
        else:
            params.append("limit=100")
        
        # Monta a URL final com os parâmetros
        service_url = base_url + "&".join(params)
        
        # Validação da URL
        service_url = Util.validate_url(service_url)

        try:
            self.print_request(method="GET", url=service_url, headers=self.headers)
            
            # Faz a requisição GET
            response = requests.get(url=service_url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def change_signature_data(self, signature_id: str, signature: Signature):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}")
        try:
            json_body = json.dumps(signature.to_dict(), ensure_ascii=False, indent=4)
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
        
    def cancel_signature_by_id(self, signature_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}/cancel")
        try:
            self.print_request(method="PUT", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers)
            #response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def suspend_signature_by_id(self, signature_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}/suspend")
        try:
            self.print_request(method="PUT", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers)
            #response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
    
    def activate_signature_by_id(self, signature_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}/activate")
        try:
            self.print_request(method="PUT", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers)
            #response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def delete_signature_coupons_by_id(self, signature_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/subscriptions/{signature_id}/coupons")
        try:
            self.print_request(method="DELETE", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.delete(url=service_url, headers=self.headers)
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
    #service = SignatureService(base_url="https://sandbox.api.assinaturas.pagseguro.com/", token="your_token_here")
    service = SignatureService(base_url="https://sandbox.api.assinaturas.pagseguro.com/", token="")
    plan_id = "PLAN_A8032840-6038-46CD-8E6F-AFE82AB78E63"
    # Exemplo de objetos relacionados
    plan_existente_example = SignaturePlan(plan_id=plan_id)
    amount_example = Amount(value=100, currency="BRL")
    new_amount_example = Amount(value=1000, currency="BRL")
    # Para um assinante já existente, basta fornecer apenas o id. Para um inexistente, deve fornecer os outros parâmetros de Subscriber
    customer_existente_example = Subscriber(subscriber_id="CUST_DAE9DC8D-542C-43F1-B6FA-DC923B3925C2") 
    customer_non_existente_example = Subscriber(name="João Silva", email="joao.silva@example.com")
    #best_invoice_date_example = BestInvoiceData() 
    
    card_example = Card(security_code=123)
    signature_payment_method_example = SignaturePaymentMethod(card=card_example)
    # Exemplo de assinatura
    reference_id_example="subscription-review-qa-a"
    signature = Signature(reference_id=reference_id_example, plan=plan_existente_example, customer=customer_existente_example, signature_payment_method=signature_payment_method_example, amount=amount_example)
    # Ao alterar uma assinatura você pode mudar os parâmetros: "pro_rata", "best_invoice_date", "next_invoice_at", "amount", "plan" e "coupon".
    new_signature = Signature(plan=plan_existente_example, amount=new_amount_example)
    # Criar Plano
    signature_id = "SUBS_AC22CC40-9E60-402D-A214-AEE249D0BB84"
    try:
        response_order = service.create_signature(signature) # Criar uma assinatura
        #response_order = service.check_signature_by_id(signature_id) # Busca uma assinatura pelo id
        #response_order = service.list_signatures() # Lista assinaturas, podendo filtrar elas por reference_id, array de Status, array de método de pagamento (payment_method_type), data do intervalo de busca sendo o ínicio (created_at_start) e o fim (created_at_end) # passível de revisão a parte do intervalo
        #response_order = service.list_subscribers_invoice(signature_id) # Listar faturas de uma assinatura, podendo filtrar por status, offset e limit
        #response_order = service.change_signature_data(signature_id=signature_id, signature=new_signature) # Atualiza um assinante existente com novas informações de cobrança
        #response_order = service.cancel_signature_by_id(signature_id) # Cancela assinatura, após cancelada a assinatura não pode ser reativada.
        #response_order = service.suspend_signature_by_id(signature_id) # Utilize esse recurso para suspender uma assinatura caso o seu cliente (assinante) não tenha pago a última fatura, por exemplo. Você tem a opção de reativar a assinatura no futuro utilizando o endpoint Ativar assinatura.
        #response_order = service.activate_signature_by_id(signature_id) # Utilize esse recurso para ativar uma assinatura previamente suspensa.
        #response_order = service.delete_signature_coupons_by_id(signature_id) # Com esse recurso, você pode remover os cupons associados à assinatura informada.

        print(response_order)
    except RuntimeError as e:
        print(e)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()