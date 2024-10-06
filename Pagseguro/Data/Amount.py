from typing import Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.Summary import Summary

class Amount:
    value: int  # Valor em centavos, mínimo 100 centavos
    currency: str = "BRL"  # Código da moeda, padrão "BRL"
    summary: Optional[Summary] = None  # Resumo do pagamento, opcional

    # Constante da moeda padrão
    DEF_CURRENCY = "BRL"

    def __init__(self, value: int, currency: Optional[str] = None, summary: Optional[Summary] = None):
        self.value = value
        self.currency = currency if currency else self.DEF_CURRENCY
        self.summary = summary

    @staticmethod
    def zero() -> 'Amount':
        """Retorna um objeto Amount com valor zero."""
        return Amount(0)
    
    def __repr__(self):
        return (f'{{"value": "{self.value}", '
                f'"currency": "{self.currency}"}}')
    
    def to_dict(self):
        """
        Converte o objeto PaymentMethod para um dicionário.

        :return: Dicionário contendo a lista de métodos de pagamento.
        """
        return {
            "value": self.value,
            "currency": self.currency
        }

# Função fora da Classe para testar a Classe
def exemplo():
    amount_default = Amount(1000)  # Criando Amount com valor e moeda padrão
    amount_custom = Amount(5000, "USD")  # Criando Amount com valor e moeda customizada
    amount_zero = Amount.zero()  # Criando Amount com valor zero

    print(amount_default.to_dict())
    print(amount_custom)
    print(amount_zero)

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()