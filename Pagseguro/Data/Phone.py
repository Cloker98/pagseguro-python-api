import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util

class Phone:
    country: str
    area: str
    number: str
    type: str

    def __init__(self, country: int = "55", area: int = "", number: int = "", type: str = "MOBILE"):
        self.country = Util.get_only_numbers(country)
        self.area = Util.get_only_numbers(area)
        self.number = Util.get_only_numbers(number)
        self.type = type
    '''
    @classmethod
    def with_area_number(cls, area: str, number: str, type: str):
        """Construtor com DDI padrão '55'."""
        return cls("55", area, number, type)

    @classmethod
    def mobile_phone(cls, area: str, number: str):
        """Construtor para telefone celular com DDI padrão '55' e tipo 'MOBILE'."""
        return cls("55", area, number, "MOBILE")
    '''
    
    def __repr__(self):
        return (f'{{"country": "{self.country}", '
                f'"area": "{self.area}", '
                f'"number": "{self.number}"}}')
    
    def to_dict(self):
        return {
            "country": self.country,
            "area": self.area,
            "number": self.number
        }

# Função fora da Classe para testar a Classe
def exemplo():
    #phone1 = Phone.with_area_number("11", "987654321", "LANDLINE")
    #phone2 = Phone.mobile_phone("21", "912345678")
    phone3 = Phone(area="21", number="912345678")

    #print(phone1)
    #print(phone2)
    print(phone3)

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()