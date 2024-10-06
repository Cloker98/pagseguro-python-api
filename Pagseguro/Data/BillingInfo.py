from typing import Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util
from Data.Card import Card
from Data.Phone import Phone
from Data.CardHolder import CardHolder

class BillingInfo:
    def __init__(self, type: str, card: Optional[Card]):
        """
        Representa as informações de pagamento do assinante.

        :param type: Tipo do meio de cobrança (ex: CREDIT_CARD).
        :param card: Objeto de detalhes do cartão.
        """
        self.type = Util.non_blank(type)
        self.card = card

    def to_dict(self):
        return {
            "type": self.type,
            "card": self.card.to_dict() if self.card else None
        }

# Exemplo de uso
def exemplo_billing_info():
    phone = Phone(country="55", area="11", number="987654321")
    card_holder = CardHolder(name="João Silva", birth_date="1980-05-20", tax_id="92410172016", phone=phone)
    card = Card(number="5555666677778884",security_code=123,exp_year="2026",exp_month="12",holder=card_holder)
    
    billing_info = BillingInfo(type="CREDIT_CARD", card=card)
    print(billing_info.to_dict())

if __name__ == "__main__":
    exemplo_billing_info()