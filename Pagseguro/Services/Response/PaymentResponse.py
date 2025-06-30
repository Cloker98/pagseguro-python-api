class PaymentResponse:
    def __init__(self, code: int, message: str, reference: str):
        """
        Detalhes sobre uma resposta de confirmação de um pagamento de um pedido.

        :param code: Código de resposta do pagamento.
        :param message: Mensagem detalhando a resposta do pagamento.
        :param reference: Referência do pedido associada à resposta.
        """
        self.code = code
        self.message = message
        self.reference = reference

    def __repr__(self):
        return (f"PaymentResponse(code={self.code}, message={self.message}, "
                f"reference={self.reference})")
    
    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "reference": self.reference
        }


# Função fora da Classe para testar a Classe
def exemplo():
    payment_response = PaymentResponse(200, "Payment confirmed", "XYZ123")
    print(payment_response)


# Exemplo de uso
if __name__ == "__main__":
    exemplo()