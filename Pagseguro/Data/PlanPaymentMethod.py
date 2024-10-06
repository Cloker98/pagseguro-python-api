from typing import List

class PlanPaymentMethod:
    def __init__(self, methods: List[str]):
        """
        Representa os métodos de pagamento aceitos para um plano.

        :param methods: Lista de métodos de pagamento. Exemplo: ["credit_card", "boleto"].
        """
        self.methods = methods

    def __repr__(self):
        """
        Retorna uma representação em string do objeto PaymentMethod.

        :return: String representativa do objeto PaymentMethod.
        """
        return f"PaymentMethod(methods={self.methods})"
    
    def to_dict(self):
        """
        Converte o objeto PaymentMethod para um dicionário.

        :return: Dicionário contendo a lista de métodos de pagamento.
        """
        return {
            "payment_method": self.methods
        }

# Exemplo de uso
def exemplo():
    # Criando um exemplo de métodos de pagamento
    methods = ["CREDIT_CARD", "BOLETO", "PIX"]
    payment_method = PlanPaymentMethod(methods=methods)

    # Imprimindo a representação e o dicionário
    print(payment_method)
    print(payment_method.to_dict())

if __name__ == "__main__":
    exemplo()