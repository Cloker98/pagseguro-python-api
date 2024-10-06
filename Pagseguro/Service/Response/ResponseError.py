from typing import List

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Service.Response.ErrorMessage import ErrorMessage

class ResponseError(Exception):
    def __init__(self, error_messages: List[ErrorMessage] = None):
        """
        Erro no processamento de uma requisição à API do PagSeguro.

        :param error_messages: Lista de mensagens de erro associadas ao erro de resposta.
        """
        super().__init__("Error occurred in PagSeguro API request")
        self.error_messages = error_messages if error_messages is not None else []

    def __repr__(self):
        return (f"ResponseError(error_messages={self.error_messages})")

# Função fora da Classe para testar a Classe
def exemplo():
    # Criando exemplos de mensagens de erro
    error_message1 = ErrorMessage(code="400", description="Bad Request", parameter_name="param1")
    error_message2 = ErrorMessage(code="401", description="Unauthorized", parameter_name="param2")
    
    # Criando uma instância de ResponseError
    response_error = ResponseError(error_messages=[error_message1, error_message2])
    print(response_error)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()