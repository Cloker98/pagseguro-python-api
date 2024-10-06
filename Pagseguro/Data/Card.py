from typing import Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Data.CardHolder import CardHolder
from Data.Phone import Phone

class Card:
    def __init__(self, last_digits: Optional[str] = None, first_digits: Optional[str] = None, brand: Optional[str] = None, token: Optional[str] = None, number: Optional[str] = None, security_code: Optional[int] = None, exp_year: Optional[str] = None, exp_month: Optional[str] = None, holder: Optional[CardHolder] = None, encrypted: Optional[str] = None):
        """
        Representa um cartão de crédito ou débito.

        :param number: Número do cartão (14-19 caracteres). Necessita Certificação PCI.
        :param security_code: Código de segurança do cartão (CVV).
        :param exp_year: Ano de expiração do cartão (2 ou 4 dígitos).
        :param exp_month: Mês de expiração do cartão (2 dígitos).
        :param holder: Objeto do portador do cartão.
        :param encrypted: Dados do cartão criptografados. Obrigatório se o integrador não possuir certificação PCI.
        """
        if encrypted:
            self.encrypted = encrypted
            self.number = None
            self.security_code = None
            self.exp_year = None
            self.exp_month = None
            self.holder = None
            self.token = None
            self.brand = None
            self.first_digits = None
            self.last_digits = None
        else:
            self.number = Util.validate_card_number(number)
            self.security_code = Util.validate_cvv(security_code)
            self.exp_year = Util.validate_exp_year(exp_year)
            self.exp_month = Util.validate_exp_month(exp_month)
            self.holder = holder
            self.token = token
            self.brand = brand
            self.first_digits = first_digits
            self.last_digits = last_digits
            self.encrypted = None

    def to_dict(self):
        if self.encrypted:
            return {"encrypted": self.encrypted}
        data = {
            #"number": self.number,
            #"security_code": self.security_code,
            #"exp_year": self.exp_year,
            #"exp_month": self.exp_month,
            #"holder": self.holder.to_dict() if self.holder else None
        }
        
        if self.holder:
            data["holder"] = self.holder.to_dict()
        if self.exp_year:
            data["exp_year"] = self.exp_year
        if self.exp_month:
            data["exp_month"] = self.exp_month
        if self.number:
            data["number"] = self.number
        if self.security_code:
            data["security_code"] = self.security_code
        if self.token:
            data["token"] = self.token
        if self.brand:
            data["brand"] = self.brand
        if self.first_digits:
            data["first_digits"] = self.first_digits
        if self.last_digits:
            data["last_digits"] = self.last_digits

        return data
    
    

# Exemplo de uso da classe Card
def exemplo_cartao():
    # Criando um objeto Phone para o portador do cartão
    phone = Phone(country="55", area="11", number="987654321", type="MOBILE")
    
    # Criando o objeto CardHolder (portador do cartão)
    card_holder = CardHolder(name="João Silva", birth_date="1985-04-20", tax_id="92410172016", phone=phone)

    # Criando um objeto Card com dados do cartão
    card = Card(
        number="1234567812345678",  # Número do cartão
        security_code=123,  # Código de segurança (CVV)
        exp_year="25",  # Ano de expiração do cartão
        exp_month="12",  # Mês de expiração do cartão
        holder=card_holder  # Portador do cartão
    )

    # Convertendo o objeto Card para dicionário para envio em uma requisição
    card_dict = card.to_dict()

    # Exibindo o dicionário
    print(card_dict)

# Exemplo de uso da classe Card com dados criptografados
def exemplo_cartao_criptografado():
    # Criando um objeto Card com os dados criptografados
    encrypted_card = Card(
        encrypted="ENCRYPTED_CARD_DATA"  # Dados criptografados do cartão
    )

    # Convertendo o objeto Card criptografado para dicionário
    encrypted_card_dict = encrypted_card.to_dict()

    # Exibindo o dicionário
    print(encrypted_card_dict)

if __name__ == "__main__":
    exemplo_cartao()
    exemplo_cartao_criptografado()