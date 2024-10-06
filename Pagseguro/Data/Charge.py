from datetime import datetime
from typing import List, Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.Amount import Amount
from Data.Holder import Holder
from Data.PaymentMethod import PaymentMethod
from Service.Response.Link import Link
from Service.Response.PaymentResponse import PaymentResponse

class Status:
    AUTHORIZED = "AUTHORIZED"
    PAID = "PAID"
    IN_ANALYSIS = "IN_ANALYSIS"
    DECLINED = "DECLINED"
    CANCELED = "CANCELED"
    WAITING = "WAITING"

class Charge:
    def __init__(self, 
                 id: str, 
                 reference_id: str, 
                 status: str, 
                 created_at: datetime, 
                 paid_at: Optional[datetime], 
                 description: str, 
                 amount: Amount, 
                 payment_response: PaymentResponse, 
                 payment_method: PaymentMethod, 
                 links: Optional[List[Link]] = None):
        """
        Informações sobre a confirmação de pagamento de um pedido feito por um cliente.

        :param id: Identificador da cobrança.
        :param reference_id: ID de referência da cobrança.
        :param status: Situação do pagamento (exemplo: PAID).
        :param created_at: Data de criação da cobrança.
        :param paid_at: Data do pagamento da cobrança (opcional).
        :param description: Descrição da cobrança.
        :param amount: Valor da cobrança.
        :param payment_response: Resposta de pagamento.
        :param payment_method: Método de pagamento usado.
        :param links: Lista de links relacionados à cobrança (opcional).
        """
        self.id = id
        self.reference_id = reference_id
        self.status = status
        self.created_at = created_at
        self.paid_at = paid_at
        self.description = description
        self.amount = amount
        self.payment_response = payment_response
        self.payment_method = payment_method
        self.links = links or []

    def __repr__(self):
        return (f"Charge(id={self.id}, reference_id={self.reference_id}, status={self.status}, "
                f"created_at={self.created_at}, paid_at={self.paid_at}, description={self.description}, "
                f"amount={self.amount}, payment_response={self.payment_response}, "
                f"payment_method={self.payment_method}, links={self.links})")

# Função fora da Classe para testar a Classe
def exemplo():
    holder = Holder("John Doe", "12345678900")
    payment_method = PaymentMethod("PIX", holder)
    amount = Amount(1000)
    payment_response = PaymentResponse("200", "Payment confirmed", "XYZ123")
    links = [Link("self", "https://example.com/link1", "application/json", "GET"), Link("self","https://example.com/link2", "application/json", "GET")]

    charge = Charge(
        id="1",
        reference_id="REF123",
        status=Status.PAID,
        created_at=datetime.now(),
        paid_at=datetime.now(),
        description="Payment for order REF123",
        amount=amount,
        payment_response=payment_response,
        payment_method=payment_method,
        links=links
    )

    print(charge)

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()