from typing import List, Optional, TypeVar
import re
import os
from datetime import datetime
import unidecode #pip install unidecode

T = TypeVar('T')  # Define um tipo genérico para listas

EMPTY_VALUES = (None, '', [], (), {})

class PagSeguroValidationError(Exception):
    pass

class Util:

    @staticmethod
    def non_blank(value: Optional[str]) -> Optional[str]:
        """Retorna None se o valor for nulo ou vazio, senão retorna o valor."""
        #return None if value is None or value.strip() == '' else value
        """Retorna None se o valor for nulo, vazio ou conter caracteres especiais, senão retorna o valor sanitizado."""
        if value is None or value.strip() == '':
            return None
        # Remove caracteres especiais, deixando apenas letras e espaços
        sanitized_value = unidecode.unidecode(value)
        return sanitized_value if sanitized_value.strip() != '' else None

    @staticmethod
    def find_dotenv_file():
        """
        Procura o arquivo .env no diretório atual ou em subdiretórios.
        Retorna o caminho completo para o arquivo .env se encontrado.
        Se o arquivo não for encontrado, retorna None.
        """
        current_dir = os.path.abspath(os.path.dirname(__file__))

        # Caminha pelos diretórios pais até encontrar o .env
        for root, dirs, files in os.walk(current_dir):
            if '.env' in files:
                return os.path.join(root, '.env')

        # Se não encontrar o arquivo .env
        return None

    @staticmethod
    def DV_maker(v):
        if v >= 2:
            return 11 - v
        return 0
    
    @staticmethod
    def validate_tax_id(value: str) -> str:
        """Valida se o CPF ou CNPJ é correto."""
        if len(value) == 11:
            return Util.is_valid_cpf(value)  # Valida CPF
        elif len(value) == 14:
            return Util.is_valid_cnpj(value)  # Valida CNPJ
        else:
            raise ValueError("tax_id deve conter 11 dígitos para CPF ou 14 dígitos para CNPJ.")


    @staticmethod
    def is_valid_cpf(value):
        error_messages = {
            'invalid': u"CPF Inválido",
            'max_digits': (u"CPF possui 11 dígitos (somente números) ou 14"
                        u" (com pontos e hífen)"),
            'digits_only': (u"Digite um CPF com apenas números ou com ponto e "
                            u"hífen"),
        }

        if value in EMPTY_VALUES:
            return u''
        orig_value = value[:]
        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        try:
            int(value)
        except ValueError:
            raise PagSeguroValidationError(error_messages['digits_only'])
        if len(value) != 11:
            raise PagSeguroValidationError(error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -
                                                                        1))])
        new_1dv = Util.DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -
                                                                        1))])
        new_2dv = Util.DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise PagSeguroValidationError(error_messages['invalid'])

        return orig_value

    @staticmethod
    def is_valid_cnpj(value):

        error_messages = {
            'invalid': u"CNPJ Inválido",
            'max_digits': (u"CNPJ possui 14 dígitos (somente números) ou 14"
                        u" (com pontos e hífen)"),
            'digits_only': (
                u"Digite um CNPJ com apenas números ou com ponto, barra "
                u"hífen"),
        }

        if value in EMPTY_VALUES:
            return u''
        if not value.isdigit():
            value = re.sub("[-/\.]", "", value)
        orig_value = value[:]
        try:
            int(value)
        except ValueError:
            raise PagSeguroValidationError(error_messages['digits_only'])
        if len(value) != 14:
            raise PagSeguroValidationError(error_messages['max_digits'])

        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(
            5, 1, -1)) + list(range(9, 1, -1)))])
        new_1dv = Util.DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(
            6, 1, -1)) + list(range(9, 1, -1)))])
        new_2dv = Util.DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise PagSeguroValidationError(error_messages['invalid'])

        return orig_value

    @staticmethod
    def is_valid_email(value):
        user_regex = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013'
            r"""\014\016-\177])*"$)""", re.IGNORECASE)
        domain_regex = re.compile(
            r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|'
            r'[A-Z0-9-]{2,})$|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|'
            r'2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE)
        domain_whitelist = ['localhost']

        if not value or '@' not in value:
            raise PagSeguroValidationError(u'Email inválido')

        user_part, domain_part = value.rsplit('@', 1)

        if not user_regex.match(user_part):
            raise PagSeguroValidationError(u'Email inválido')

        if (domain_part not in domain_whitelist and
                not domain_regex.match(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
                if not domain_regex.match(domain_part):
                    raise PagSeguroValidationError(u'Email inválido')
                else:
                    return value
            except UnicodeError:
                pass
            raise PagSeguroValidationError(u'Email inválido')
        return value

    @staticmethod
    def get_only_numbers(value: str) -> str:
        """Remove todos os caracteres não numéricos de uma string."""
        return ''.join(filter(str.isdigit, value))
    
    @staticmethod
    def remove_spaces(text: str) -> str:
        """Remove all spaces from the string."""
        return text.replace(" ", "")
    
    @staticmethod
    def get_list(lst: Optional[List[T]]) -> List[T]:
        """Retorna uma lista ou uma lista vazia se a entrada for None."""
        return lst if lst is not None else []
    
    @staticmethod
    def validate_url(uri: str) -> str:
        """Remove barras duplas de uma URI, exceto :// do protocolo."""
        result = []
        i = 0
        while i < len(uri):
            # Verifica se a sequência é '://' e pula para não remover essas barras duplas
            if uri[i:i+3] == "://":
                result.append(uri[i:i+3])
                i += 3
            # Remove barras duplas extras fora do '://'
            elif uri[i:i+2] == "//":
                result.append("/")
                i += 2
            else:
                result.append(uri[i])
                i += 1
        return ''.join(result)
    
    @staticmethod
    def validate_date(date_str: str) -> str:
        """
        Valida se a data está no formato 'AAAA-MM-DD'. Retorna a própria data se for válida.
        :param date_str: Data no formato 'AAAA-MM-DD'.
        :return: A própria data se válida.
        :raises ValueError: Se a data estiver em um formato inválido ou for uma data inexistente.
        """
        try:
            # Tenta converter a string para uma data válida no formato 'AAAA-MM-DD'
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Data inválida: {date_str}. Use o formato 'AAAA-MM-DD'.")
        return date_str
    
    @staticmethod
    def validate_card_number(number: Optional[str]) -> Optional[str]:
        """
        Valida se o número do cartão contém entre 14 e 19 dígitos.
        :param number: Número do cartão.
        :return: O próprio número se for válido, ou None se o número for None.
        :raises ValueError: Se o número estiver em um formato inválido.
        """
        if number is None:
            return None
        if not re.fullmatch(r"\d{14,19}", number):
            raise ValueError("O número do cartão deve conter entre 14 e 19 dígitos.")
        return number
    '''
    @staticmethod
    def validate_cvv(cvv: str) -> str:
        """
        Valida se o CVV contém 3 ou 4 dígitos.
        :param cvv: Código de segurança do cartão (CVV).
        :return: O próprio CVV se for válido.
        :raises ValueError: Se o CVV estiver em um formato inválido.
        """
        if not re.fullmatch(r"\d{3,4}", cvv):
            raise ValueError("O CVV deve conter 3 ou 4 dígitos.")
        return cvv
    '''
        
    @staticmethod
    def validate_cvv(cvv: Optional[int]) -> Optional[int]:
        """
        Valida se o CVV contém 3 ou 4 dígitos.
        :param cvv: Código de segurança do cartão (CVV).
        :return: O próprio CVV se for válido, ou None se o CVV for None.
        :raises ValueError: Se o CVV estiver em um formato inválido.
        """
        if cvv is None:
            return None
        if not 100 <= cvv <= 9999:
            raise ValueError("O CVV deve conter 3 ou 4 dígitos.")
        return cvv

    @staticmethod
    def validate_exp_year(exp_year: Optional[str]) -> Optional[str]:
        """
        Valida o ano de expiração do cartão.
        :param exp_year: Ano de expiração (2 ou 4 dígitos).
        :return: O próprio ano se for válido, ou None se o ano for None.
        :raises ValueError: Se o ano estiver em um formato inválido ou for inválido.
        """
        if exp_year is None:
            return None
        current_year = datetime.now().year
        if len(exp_year) == 2:
            exp_year = "20" + exp_year  # Converte "23" para "2023"
        elif len(exp_year) != 4:
            raise ValueError("O ano de expiração deve conter 2 ou 4 dígitos.")
        
        exp_year_int = int(exp_year)
        if exp_year_int < current_year:
            raise ValueError("O ano de expiração deve ser no futuro.")
        
        return exp_year

    @staticmethod
    def validate_exp_month(exp_month: Optional[str]) -> Optional[str]:
        """
        Valida o mês de expiração do cartão.
        :param exp_month: Mês de expiração (dois dígitos entre 01 e 12).
        :return: O próprio mês se for válido, ou None se o mês for None.
        :raises ValueError: Se o mês estiver fora do intervalo válido.
        """
        if exp_month is None:
            return None
        if not re.fullmatch(r"0[1-9]|1[0-2]", exp_month):
            raise ValueError("O mês de expiração deve ser um valor entre 01 e 12.")
        return exp_month
    ''''
    @staticmethod
    def format_error(error: str, description: str, parameter_name: str) -> dict:
        """
        Formata a mensagem de erro de acordo com o padrão especificado.

        :param message: A mensagem de erro.
        :param location: A localização do erro (por exemplo, o campo que causou o erro).
        :return: Um dicionário contendo a mensagem de erro formatada.
        """
        #"message": message,
        #"location": location
        return {
            "error": error,
            "description": description,
            "parameter_name": parameter_name
        }

    @staticmethod
    def create_error_response(errors: list) -> dict:
        """
        Cria a resposta de erro em formato JSON seguindo o padrão especificado.

        :param errors: Lista de erros.
        :return: Um dicionário contendo a resposta de erro formatada.
        """
        return {
            "errors_messages": errors
        }
    '''

# Função fora da Classe para testar a Classe
def exemplo():
    print(Util.get_only_numbers("123abc456"))  # Saída: 123456
    print(Util.validate_url("http://example.com//path"))  # Saída: http://example.com/path
    print(Util.get_list([1, 2, 3]))  # Saída: [1, 2, 3]
    print(Util.get_list(None))  # Saída: []
    print(Util.is_valid_email("elizeugsn@hotmail.com")) # email correto
    #print(Util.is_valid_email("elizeugsnotmail.com")) # email com erro

    
if __name__ == "__main__":
    exemplo()