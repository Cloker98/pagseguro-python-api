from typing import List, Optional
import os
import sys 
from datetime import date, datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Data.BillingInfo import BillingInfo
from Data.SignaturePaymentMethod import SignaturePaymentMethod
from Service.Response.Link import Link
from Data.Amount import Amount
from Service.SignaturePlan import SignaturePlan
from Data.Subscriber import Subscriber

class BestInvoiceData:
    def __init__(self, day: str, month: str):
        """
        Contém informações sobre o melhor dia e mês para emissão de uma fatura.

        :param day: Dia da emissão da fatura.
        :param month: Mês da emissão da fatura.
        """
        self.day = day
        self.month = month

    def __repr__(self):
        return f"BestInvoiceData(day={self.day}, month={self.month})"

    def to_dict(self):
        return {
            "day": self.day,
            "month": self.month
        }

class Signature:
    def __init__(self, best_invoice_date: Optional[BestInvoiceData] = None, signature_id: Optional[str] = None, reference_id: Optional[str] = None, amount: Optional[Amount] = None, status: Optional[str] = None, plan: Optional[SignaturePlan] = None, signature_payment_method: Optional[List[SignaturePaymentMethod]] = None, next_invoice_at: Optional[str] = None, pro_rata: Optional[bool] = False, customer: Optional[Subscriber] = None, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, exp_at: Optional[datetime] = None, links: Optional[List[Link]] = None):
        """
        Representa uma assinatura de um cliente.

        :param signature_id: Id da assinatura no formato SUBS_UUID.
        :param reference_id: Código externo informado pelo merchant.
        :param amount: Objeto contendo os valores da assinatura.
        :param status: Status da assinatura (ex: OVERDUE).
        :param plan: Detalhes do plano do cliente.
        :param payment_method: Lista de objetos de informações de pagamento.
        :param best_invoice_date: Objeto com melhor data para próxima cobrança
        :param next_invoice_at: Data da próxima fatura.
        :param pro_rata: Indica se a cobrança é proporcional.
        :param customer: Detalhes do cliente.
        :param created_at: Data de criação da assinatura.
        :param updated_at: Data de última atualização da assinatura.
        :param exp_at: Data de expiração da assinatura.
        :param links: Lista de links referentes à assinatura.
        """
        # Validações e Atribuições
        if signature_id:
            if len(signature_id) > 41:
                raise ValueError("Signature ID cannot exceed 41 characters.")
        if reference_id:
            if len(reference_id) > 65:
                raise ValueError("Reference ID cannot exceed 65 characters.")

        self.signature_id = signature_id
        self.reference_id = reference_id
        self.amount = amount
        self.status = status
        self.plan = plan
        # Garantir que payment_method seja uma lista
        if signature_payment_method:
            if not isinstance(signature_payment_method, list):
                self.signature_payment_method = [signature_payment_method]
            else:
                self.signature_payment_method = signature_payment_method
        else:
            self.signature_payment_method = []
        self.next_invoice_at = next_invoice_at
        self.best_invoice_date = best_invoice_date
        self.pro_rata = pro_rata
        self.customer = customer
        self.created_at = created_at
        self.updated_at = updated_at
        self.exp_at = exp_at
        self.links = links if links else []

    def __repr__(self):
        return f"Signature(id={self.signature_id}, status={self.status}, amount={self.amount})"

    def to_dict(self):
        data = {
            #"id": self.signature_id,
            #"reference_id": self.reference_id,
            #"amount": self.amount.to_dict() if self.amount else None,
            #"status": self.status,
            #"plan": self.plan.to_dict() if self.plan else None,
            #"payment_method": [payment.to_dict() for payment in self.payment_method],
            #"next_invoice_at": self.next_invoice_at, # Parâmetro que aparece na resposta
            #"pro_rata": self.pro_rata,
            #"customer": self.customer.to_dict() if self.customer else None,
            #"created_at": self.created_at.isoformat() if self.created_at else None,
            #"updated_at": self.updated_at.isoformat() if self.updated_at else None,
            #"exp_at": self.exp_at.isoformat() if self.exp_at else None,
            #"links": [link.to_dict() for link in self.links]
        }

        if self.signature_id:
            data["id"] = self.signature_id
        if self.reference_id:
            data["reference_id"] = self.reference_id
        if self.amount:
            data["amount"] = self.amount.to_dict()
        if self.status:
            data["status"] = self.status
        if self.plan:
            data["plan"] = self.plan.to_dict()
        if self.signature_payment_method:
            data["payment_method"] = [payment.to_dict() for payment in self.signature_payment_method]
        if self.next_invoice_at:
            data["next_invoice_at"] = self.next_invoice_at
        if self.best_invoice_date:
            data["best_invoice_date"] = self.best_invoice_date.to_dict()
        if self.pro_rata:
            data["pro_rata"] = self.pro_rata
        if self.customer:
            data["customer"] = self.customer.to_dict()

        return data


# Exemplo de uso da classe Signature
def exemplo():
    # Exemplo de objetos relacionados
    plan_example = SignaturePlan(plan_id="PLAN_123", name="Plano Mensal")
    amount_example = Amount(value=100, currency="BRL")
    # Para um assinante já existente, basta fornecer apenas o id. Para um inexistente, deve fornecer os outros parâmetros de Subscriber
    customer_existente_example = Subscriber(subscriber_id="CUST_DAE9DC8D-542C-43F1-B6FA-DC923B3925C2") 
    customer_non_existente_example = Subscriber(name="João Silva", email="joao.silva@example.com") 
    
    # Exemplo de assinatura
    signature = Signature(signature_id="SUBS_123", reference_id="subscription-review-qa-a", amount=amount_example, status="OVERDUE", plan=plan_example, customer=customer_existente_example, created_at=datetime(2023, 1, 1, 10, 30, 0), updated_at=datetime(2023, 1, 2, 12, 0, 0), exp_at=datetime(2023, 7, 1))
    print(signature.to_dict())


# Exemplo de uso
if __name__ == "__main__":
    exemplo()