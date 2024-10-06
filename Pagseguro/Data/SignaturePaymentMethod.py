import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.Card import Card

class SignaturePaymentMethod:
    def __init__(self, type: Optional[str] = "CREDIT_CARD", card: Optional[Card] = None):
        self.type = type
        self.card = card

    def __repr__(self):
        return f"SignaturePaymentMethod(type={self.type}, card={self.card})"

    def to_dict(self):
        return {
            "type": self.type,
            "card": self.card.to_dict() if self.card else None
        }
    
# Função fora da Classe para testar a Classe
def exemplo():
    # Criando um exemplo de Card
    card_example = Card(security_code=435)
    # Criando um exemplo de SignaturePaymentMethod com o Card
    payment_method = SignaturePaymentMethod(type="CREDIT_CARD", card=card_example)
    
    # Imprimindo a representação da classe
    print(payment_method)
    
    # Imprimindo a versão em dicionário (para JSON)
    print(payment_method.to_dict())

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()