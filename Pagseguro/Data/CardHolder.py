import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Data.Phone import Phone

class CardHolder:
    def __init__(self, name: str, birth_date: str, tax_id: str, phone: Phone):
        """
        Representa o portador do cartão.

        :param name: Nome completo do portador do cartão.
        :param birth_date: Data de nascimento do portador.
        :param tax_id: CPF ou CNPJ do portador.
        :param phone: Objeto com detalhes do telefone do portador do cartão.
        """
        self.name = Util.non_blank(name)
        self.birth_date = Util.validate_date(birth_date)
        self.tax_id = Util.validate_tax_id(tax_id)
        self.phone = phone

    def to_dict(self):
        return {
            "name": self.name,
            "birth_date": self.birth_date,
            "tax_id": self.tax_id,
            "phone": self.phone.to_dict()
        }
    
# Exemplo de uso da classe CardHolder
def exemplo():
    # Criando um objeto Phone para o portador do cartão
    phone = Phone(country="55", area="11", number="987654321", type="MOBILE")

    # Criando o objeto CardHolder com nome, data de nascimento, CPF e telefone
    card_holder = CardHolder(
        name="João Silva",
        birth_date="1990-05-15",  # Data de nascimento no formato AAAA-MM-DD
        tax_id="92410172016",  # CPF com 11 dígitos
        phone=phone
    )

    # Convertendo o objeto para um dicionário para enviar em uma requisição ou exibir
    card_holder_dict = card_holder.to_dict()

    # Exibindo o dicionário
    print(card_holder_dict)

if __name__ == "__main__":
    exemplo()