from typing import Optional
import requests
import json
from datetime import datetime, timedelta

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Service.SignaturePlan import SignaturePlan
from Data.Amount import Amount
from Data.Interval import Interval
from Data.Trial import Trial
from Data.PlanPaymentMethod import PlanPaymentMethod

class SignaturePlanService:
     # Formato base para a data e hora
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"  # Sem milissegundos e timezone por padrão
    def __init__(self, base_url: str, token: str):
        """
        Inicializa o serviço para enviar pedidos de criação de QRCode de PIX.

        :param base_url: URL base do serviço.
        :param token: Token de autorização.
        """
        self.service_url = Util.validate_url(f"{base_url}/plans")
        self.token = token
        self.headers = {
            "accept": "application/json",
            "Authorization": f'Bearer {self.token}',
            "content-Type": "application/json"
        }
        
    def create_plan(self, plan: SignaturePlan):
        """
        Envia uma requisição para criar um QRCode de PIX e retorna o JSON de resposta.

        :param order: Objeto PixOrder a ser enviado.
        :return: Resposta da API em formato JSON.
        :raises RuntimeError: Quando ocorre algum erro na requisição.
        """
        try:
            # Serializa o objeto PixOrder para JSON, tratando o datetime
            #json_body = json.dumps(order, default=self.json_serializer, indent=4)
            json_body = json.dumps(plan.to_dict(), indent=4)
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
        
    def check_plan_by_id(self, plan_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/plans/{plan_id}")
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
        
    def list_plans(self, offset: int, limit: int, reference_id: str):
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/plans?offset={offset}&limit={limit}&reference_id={reference_id}")
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
        
    def change_plan(self, plan_id: str, plan: SignaturePlan):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/plans/{plan_id}")
        try:
            json_body = json.dumps(plan.to_dict(), indent=4)
            print(json_body)
            self.print_request(method="PUT", url=service_url, headers=self.headers, json_body=json_body)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers, data=json_body)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
        
    def activate_plan_by_id(self, plan_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/plans/{plan_id}/activate")
        try:
            self.print_request(method="PUT", url=service_url, headers=self.headers)

            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            if response.status_code == 204:
                # Código 204 significa "No Content", então a inativação foi bem-sucedida sem resposta JSON
                return {"message": "Plan activated successfully"}
            
            # Verifica se a resposta contém conteúdo antes de fazer parsing
            if response.text:
                return response.json()  # Tenta converter o conteúdo para JSON
        
            return {"message": "Plan activation successful, but no content in response"}
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON decode error: {e}")
    
    def inactivate_plan_by_id(self, plan_id: str):
        #plan_id = SignaturePlan.
        service_url = Util.validate_url(f"https://sandbox.api.assinaturas.pagseguro.com/plans/{plan_id}/inactivate")
        try:
            self.print_request(method="PUT", url=service_url, headers=self.headers)
    
            # Faz a requisição GET (a lógica de requisição continua a mesma)
            response = requests.put(url=service_url, headers=self.headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            if response.status_code == 204:
                # Código 204 significa "No Content", então a inativação foi bem-sucedida sem resposta JSON
                return {"message": "Plan inactivated successfully"}
            
            # Verifica se a resposta contém conteúdo antes de fazer parsing
            if response.text:
                return response.json()  # Tenta converter o conteúdo para JSON
        
            return {"message": "Plan inactivation successful, but no content in response"}
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
    service = SignaturePlanService(base_url="https://sandbox.api.assinaturas.pagseguro.com/", token="")
    amount = Amount(1000)
    interval_mensal = Interval(1, "MONTH")
    interval_anual = Interval(1, "YEAR")  
    trial_ativo = Trial(7, True, True) # O padrão
    trial_desativado = Trial(0, False, True)
    PlanPaymentMethod(["CREDIT_CARD"])
    # Para criação do plano é necessário pelo menos o "reference_id", "name", "interval", "trial" e "amount" --- POST ---
    signature_plan = SignaturePlan(reference_id="ex-00001", name="ACME Premium plan", interval=interval_mensal, trial=trial_ativo, amount=amount)
    new_signature_plan = SignaturePlan(reference_id="ex-00001", name="ACME Deluxe plan", interval=interval_anual, trial=trial_desativado, amount=amount)
    plan_id = "PLAN_A8032840-6038-46CD-8E6F-AFE82AB78E63"
    # Criar Plano
    try:
        #response_order = service.create_plan(signature_plan) # Criar um plano de assinatura
        #response_order = service.check_plan_by_id(plan_id) # Busca um plano de assinatura pelo id
        #response_order = service.list_plans(0,100,"ex-00001") # Lista os planos de assinatura pelos parametros passados
        #response_order = service.change_plan(plan_id, new_signature_plan) # Atualiza um plano existente com novas configurações
        response_order = service.activate_plan_by_id(plan_id) # Ativa um plano para que seja possível vincular assinaturas a ele.
        #response_order = service.inactivate_plan_by_id(plan_id) # Inativa um plano existente. Você não conseguirá associar assinaturas a um plano inativo.
        print(response_order)
    except RuntimeError as e:
        print(e)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()