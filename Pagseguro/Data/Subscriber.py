from typing import List, Optional
import os
import sys 
from datetime import date, datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util  
from Data.Phone import Phone 
from Data.Address import Address
from Data.BillingInfo import BillingInfo
from Data.CardHolder import CardHolder
from Data.Card import Card
from Service.Response.Link import Link

class Subscriber:
    def __init__(self, name: Optional[str] = None, email: Optional[str] = None, phones: Optional[List[Phone]] = None, tax_id: Optional[str] = None, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, reference_id: Optional[str] = None, subscriber_id: Optional[str] = None, birth_date: Optional[date] = None, links: Optional[List[Link]] = None, address: Optional[Address] = None, billing_info: Optional[List[BillingInfo]] = None):
        """
        Cliente para quem está sendo feita uma venda.

        :param name: Nome do cliente. (Obrigatório para quando for criar um assinante, opcional para quando alterar dados pessoais.)
        :param email: Email do cliente.
        :param tax_id: CPF/CNPJ do cliente.
        :param phones: Lista de objetos Phone do cliente. Se None, será inicializada como lista vazia.
        """
        # Validações e Atribuições
        if subscriber_id: 
            if len(subscriber_id) > 41:
                raise ValueError("Subscriber_id cannot exceed 41 characters.")
        if name: 
            if len(name) > 150:
                raise ValueError("Name cannot exceed 150 characters.")
        if reference_id:
            if len(reference_id) > 65:
                raise ValueError("Reference_id cannot exceed 65 characters.")
        if email:
            if len(email) > 60:
                raise ValueError("Email cannot exceed 60 characters.")

        # Atribuições
        self.subscriber_id = subscriber_id # Vem no retorno da resposta
        self.name = Util.non_blank(name) if name else None
        self.reference_id = reference_id if reference_id else None
        self.email = Util.is_valid_email(email) if email else None
        self.tax_id = Util.validate_tax_id(tax_id) if tax_id else None  # Garantir que o atributo seja sempre atribuído
        
        self.phones = Util.get_list(phones if phones else [])

        #if not phones:
            #raise ValueError("O assinante deve conter pelo menos um telefone.")
        
        self.birth_date = birth_date
        self.address = address
        self.billing_info = Util.get_list(billing_info if billing_info else [])
        self.created_at = created_at
        self.updated_at = updated_at
        self.links = links or []

    def __repr__(self):
        return f"Customer(name={self.name}, email={self.email}, tax_id={self.tax_id}, phones={self.phones})"
    
    def to_dict(self):
        data = {
            #"name": self.name, # Obrigatório para criar um assinante
            #"email": self.email, # Obrigatório para criar um assinante
            #"tax_id": self.tax_id, # Obrigatório para criar um assinante, porém não pode ser alterado depois que criado, portanto deve ser inicializado como opcional.
            #"phones": [phone.to_dict() for phone in self.phones],
            #"reference_id": self.reference_id,
            #"birth_date": self.birth_date.strftime("%Y-%m-%d") if self.birth_date else None,
            #"address": self.address.to_dict() if self.address else None,
            #"billing_info": [billing.to_dict() for billing in self.billing_info] if self.billing_info else None
        }
        if self.subscriber_id:
            data["id"] = self.subscriber_id
        if self.reference_id:
            data["reference_id"] = self.reference_id
        if self.name:
            data["name"] = self.name
        if self.email:
            data["email"] = self.email
        if self.tax_id: # Obrigatório para criar um assinante, porém não pode ser alterado depois que criado, portanto deve ser inicializado como opcional.
            data["tax_id"] = self.tax_id
        if self.phones:
            data["phones"] = [phone.to_dict() for phone in self.phones]
        if self.birth_date:
            data["birth_date"] = self.birth_date.strftime("%Y-%m-%d")
        if self.address:
            data["address"] = self.address.to_dict()
        if self.billing_info:
            data["billing_info"] = [billing.to_dict() for billing in self.billing_info]
    
        return data

def exemplo():
    phone_example = Phone("55", "11", "123456789", "MOBILE")
     # Exemplo de BillingInfo
    card_holder = CardHolder(name="João Silva", birth_date="1985-04-20", tax_id="92410172016", phone=phone_example)
    card = Card(number="5555666677778884", security_code=123, exp_year="2026", exp_month="12", holder=card_holder)
    billing_info = BillingInfo(type="CREDIT_CARD", card=card) 
    subscriber = Subscriber(name="João Silva", email="joao.silva@example.com", tax_id="01234567890", phones=[phone_example], reference_id="ex-00001", birth_date=date(2000, 12, 20), billing_info=[billing_info])
    print(subscriber.to_dict())

# Exemplo de uso
if __name__ == "__main__":
    exemplo()