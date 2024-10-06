import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.Address import Address

class Shipping:
    address: Address 

    def __init__(self, address: Address):
        self.address = address        

    @staticmethod
    def empty() -> 'Shipping':
        """Retorna um objeto Shipping com endereço vazio."""
        return Shipping(Address.empty())

# Função fora da Classe para testar a Classe
def exemplo():
    address = Address(
        street="Rua Exemplo",
        number="123",
        complement="Apto 45",
        locality="Centro",
        city="São Paulo",
        region_code="SP",
        country="BRA",
        postal_code="12345-678"
    )

    shipping_address = Shipping(address=address)
    print(shipping_address)

    shipping_empty = Shipping.empty()
    print(shipping_empty)

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()