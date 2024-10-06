from typing import List, Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util  
from Data.Phone import Phone 

class Customer:
    def __init__(self, name: str, email: str, tax_id: str, phones: Optional[List[Phone]] = None):
        """
        Cliente para quem está sendo feita uma venda.

        :param name: Nome do cliente.
        :param email: Email do cliente.
        :param tax_id: CPF/CNPJ do cliente.
        :param phones: Lista de objetos Phone do cliente. Se None, será inicializada como lista vazia.
        """
        self.name = name
        self.email = Util.is_valid_email(email)
        # Verificação da quantidade de dígitos para CPF ou CNPJ
        if len(tax_id) == 11:
            self.tax_id = Util.is_valid_cpf(tax_id)  # Valida CPF
        elif len(tax_id) == 14:
            self.tax_id = Util.is_valid_cnpj(tax_id)  # Valida CNPJ
        else:
            raise ValueError("tax_id deve conter 11 dígitos para CPF ou 14 dígitos para CNPJ.")
        
        self.phones = Util.get_list(phones if phones is not None else [])

    def __repr__(self):
        return f"Customer(name={self.name}, email={self.email}, tax_id={self.tax_id}, phones={self.phones})"
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "tax_id": self.tax_id,
            "phones": [phone.to_dict() for phone in self.phones]
        }

def exemplo():
        phone_example1 = Phone("55", "11", "123456789", "MOBILE")  # Supondo que exista uma implementação da classe Phone
        phone_example2 = Phone("55", "21", "987654321", "MOBILE")  # Supondo que exista uma implementação da classe Phone
        phones = [phone_example1, phone_example2]
        customer = Customer("João Silva", "joao.silva@example.com", "92410172016", phones)
        print(customer)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()