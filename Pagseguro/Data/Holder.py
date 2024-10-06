import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util  

class Holder:
    def __init__(self, name: str, tax_id: str):
        """
        Informações sobre o titular de um método de pagamento utilizado para pagar um determinado pedido.

        :param name: Nome do titular.
        :param tax_id: CPF ou CNPJ do titular (identificação fiscal).
        """
        self.name = name
        # Verificação da quantidade de dígitos para CPF ou CNPJ
        if len(tax_id) == 11:
            self.tax_id = Util.is_valid_cpf(tax_id)  # Valida CPF
        elif len(tax_id) == 14:
            self.tax_id = Util.is_valid_cnpj(tax_id)  # Valida CNPJ
        else:
            raise ValueError("tax_id deve conter 11 dígitos para CPF ou 14 dígitos para CNPJ.")
        

    def __repr__(self):
        return f"Holder(name={self.name}, tax_id={self.tax_id})"

# Função fora da Classe para testar a Classe
def exemplo():
    holder = Holder("João Silva", "92410172016")
    print(holder)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()