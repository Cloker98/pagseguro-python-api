class Summary:
    total: int  # Valor total da transação
    paid: int  # Valor pago
    refunded: int  # Valor reembolsado

# Função fora da Classe para testar a Classe
def exemplo():
    summary_example = Summary(total=10000, paid=9500, refunded=500)
    print(summary_example)

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()