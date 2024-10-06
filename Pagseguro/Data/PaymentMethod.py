import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.Holder import Holder
from typing import Optional

class PaymentMethod:
    def __init__(self, type: str, holder: Optional[Holder]):
        """
        Informações sobre o método de pagamento que um cliente usou para pagar um pedido.

        :param type: Tipo do método de pagamento (como PIX).
        :param holder: Titular do método de pagamento (como dono do cartão ou da conta bancária).
        """
        self.type = type
        self.holder = holder

    def __repr__(self):
        return f"PaymentMethod(type={self.type}, holder={self.holder})"

# Função fora da Classe para testar a Classe
def exemplo():
    holder_example = Holder("João Silva", "92410172016")  # Supondo que exista uma implementação da classe Holder
    payment_method = PaymentMethod("PIX", holder_example)
    print(payment_method)

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()
