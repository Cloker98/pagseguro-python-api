class ErrorMessage:
    def __init__(self, code: str, description: str, parameter_name: str):
        """
        Mensagem de erro enviada como resposta de uma requisição.

        :param code: Código do erro.
        :param description: Descrição do erro.
        :param parameter_name: Nome do parâmetro associado ao erro.
        """
        self.code = code
        self.description = description
        self.parameter_name = parameter_name

    def __repr__(self):
        return (f"ErrorMessage(code={self.code}, description={self.description}, "
                f"parameter_name={self.parameter_name})")

# Função fora da Classe para testar a Classe
def exemplo():
    error_message = ErrorMessage("404", "Not Found", "url")
    print(error_message)
    
# Exemplo de uso
if __name__ == "__main__":
    exemplo()