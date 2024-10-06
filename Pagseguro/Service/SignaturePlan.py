from typing import List, Optional
from datetime import datetime
from enum import Enum

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.Amount import Amount
from Data.Interval import Interval
from Data.Trial import Trial
from Data.PlanPaymentMethod import PlanPaymentMethod
from Service.Response.Link import Link

class SignaturePlanStatus(Enum):
   ACTIVE = 0
   INACTIVE = 1

class SignaturePlan:
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

    def __init__(self, reference_id: Optional[str] = None, name: Optional[str] = None, interval: Optional[Interval] = None, trial: Optional[Trial] = None, amount: Optional[Amount] = None, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, status: Optional[List[str]] = None, description: Optional[str] = None, plan_id: Optional[str] = None, links: Optional[List[Link]] = None, setup_fee: Optional[int] = None, limit_subscriptions: Optional[int] = None, plan_payment_method: Optional[PlanPaymentMethod] = ["CREDIT_CARD"]):
        """id: Optional[str] = None
        Representa os detalhes de um plano de assinatura.

        :param plan_id: Identificador único do plano. Exemplo: "PLAN_XXXX".
        :param reference_id: Identificador único atribuído ao plano pelo vendedor. Exemplo: "ex-00001".
        :param status: Status do plano. Pode ser "ACTIVE" ou "INACTIVE".
        :param name: Nome do plano. Exemplo: "ACME Premium plan".
        :param description: Descrição do plano. Exemplo: "Esse é um plano premium de assinatura".
        :param setup_fee: Taxa inicial cobrada pela assinatura. Exemplo: 15.
        :param limit_subscriptions: Limite de assinaturas no plano. Exemplo: 100.
        :param interval: Objeto contendo os detalhes de intervalo de tempo das cobranças.
        :param trial: Objeto contendo os detalhes sobre o período de teste do plano.
        :param payment_method: Lista de métodos de pagamento aceitos. Exemplo: ["credit_card", "boleto"].
        :param created_at: Data de criação do plano. Exemplo: "2023-01-01T12:00:00Z".
        :param updated_at: Data da última atualização do plano. Exemplo: "2023-02-15T12:00:00Z".
        :param links: Lista de links referentes ao plano.
        """
        self.plan_id = self.non_blank(plan_id)
        self.reference_id = reference_id
        self.status = status
        self.name = name
        self.description = self.non_blank(description)
        self.amount = amount
        self.setup_fee = self.non_null_int(setup_fee)
        self.limit_subscriptions = limit_subscriptions
        self.interval = interval
        self.trial = trial
        self.plan_payment_method = plan_payment_method
        self.created_at = created_at
        self.updated_at = updated_at
        self.links = links or []

    @staticmethod
    def non_blank(value: Optional[str]) -> Optional[str]:
        """Retorna None se o valor for nulo ou vazio, senão retorna o valor."""
        return None if value is None or value.strip() == '' else value
    
    @staticmethod
    def non_null_int(value: Optional[int]) -> int:
        """
        Retorna 0 se o valor for None, senão retorna o valor.

        :param value: O valor inteiro ou None.
        :return: O valor ou 0 se for None.
        """
        return 0 if value is None else value
    
    def __repr__(self):
        """
        Retorna uma representação em string do objeto Plan, contendo os principais atributos.

        :return: String representativa do objeto Plan.
        """
        return (f"Plan(id={self.plan_id}, reference_id={self.reference_id}, status={self.status}, "
                f"name={self.name}, description={self.description})")

    def to_dict(self):
        """
        Converte o objeto Plan para um dicionário, contendo todos os seus atributos.

        :return: Dicionário com os detalhes do plano.
        """
        data = {
            #"id": self.plan_id,
            #"reference_id": self.reference_id,
            #"status": self.status,  # Enum representado pelo nome
            #"name": self.name,
            #"description": self.description,
            #"amount": self.amount.to_dict(),  # Supondo que Amount tenha um método to_dict()
            #"setup_fee": self.setup_fee,
            #"limit_subscriptions": self.limit_subscriptions,
            #"interval": self.interval.to_dict(),  # Supondo que Interval tenha um método to_dict()
            #"trial": self.trial.to_dict(),  # Supondo que Trial tenha um método to_dict()
            #"payment_method": self.payment_method,
            #"created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S") if self.created_at else None,
            #"updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S") if self.updated_at else None,
            #"links": [link.to_dict() for link in self.links]  # Supondo que Link tenha um método to_dict()
        }
        if self.plan_id:
            data["id"] = self.plan_id
        if self.reference_id:
            data["reference_id"] = self.reference_id
        if self.status:
            data["status"] = self.status
        if self.name:
            data["name"] = self.name
        if self.description:
            data["description"] = self.description
        if self.amount:
            data["amount"] = self.amount.to_dict()
        if self.setup_fee:
            data["setup_fee"] = self.setup_fee  # Inclui splits no dicionário, se existir
        if self.interval:
            data["interval"] = self.interval.to_dict()
        if self.trial:
            data["trial"] = self.trial.to_dict()
        if self.limit_subscriptions:
            data["limit_subscriptions"] = self.limit_subscriptions
        if self.plan_payment_method:
            data["payment_method"] = self.plan_payment_method
        
        return data
        

# Exemplo de uso
def exemplo_plan():
    amount = Amount(1000)
    interval_mensal = Interval(1, "MONTH")
    trial_ativo = Trial(7, True, True)
    PlanPaymentMethod(["CREDIT_CARD"])
    # Para criação do plano é necessário pelo menos o "reference_id", "name", "interval", "trial" e "amount"
    signature_plan = SignaturePlan(reference_id="ex-00001", name="ACME Premium plan", interval=interval_mensal, trial=trial_ativo, amount=amount)

    print(signature_plan.to_dict())

if __name__ == "__main__":
    exemplo_plan()