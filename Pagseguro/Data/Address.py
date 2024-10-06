import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Util import Util

class Address:
    street: str
    number: str
    complement: str
    locality: str  # Bairro
    city: str
    region_code: str  # UF
    country: str  # Código do país (3 letras)
    postal_code: str  # CEP no formato 99999999

    def __init__(self, street: str, number: str, complement: str, locality: str, city: str, region_code: str, country: str, postal_code: str):
        complement = Util.remove_spaces(complement)  # Remove espaços
        postal_code = Util.get_only_numbers(postal_code)
        # Validações
        if len(street) > 150:
            raise ValueError("Street cannot exceed 150 characters.")
        if len(number) > 8:
            raise ValueError("Number cannot exceed 8 characters.")
        if len(complement) > 40:
            raise ValueError("Complement cannot exceed 40 characters.")
        if len(locality) > 60:
            raise ValueError("Locality cannot exceed 60 characters.")
        if len(city) > 60:
            raise ValueError("City cannot exceed 60 characters.")
        if len(region_code) != 2:
            raise ValueError("Region code must be exactly 2 characters.")
        if len(postal_code) != 8 or not postal_code.isdigit():
            raise ValueError("Postal code must be exactly 8 numeric characters.")
        if country != "BRA":
            raise ValueError("Country must be 'BRA'.")
        
        # Atribuições
        self.street = street
        self.number = number
        self.complement = Util.remove_spaces(complement)
        self.locality = locality
        self.city = city
        self.region_code = region_code
        self.country = country
        self.postal_code = Util.get_only_numbers(postal_code)

    @staticmethod
    def empty() -> 'Address':
        """Cria um objeto Address vazio."""
        return Address("", "", "", "", "", "", "", "")
    
    def __repr__(self):
        return (f"Address(street={self.street}, number={self.number}, complement={self.complement}, "
                f"locality={self.locality}, city={self.city}, region_code={self.region_code}, "
                f"country={self.country}, postal_code={self.postal_code})")
    
    def to_dict(self):
        return {
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "locality": self.locality,
            "city": self.city,
            "region_code": self.region_code,
            "country": self.country,
            "postal_code": self.postal_code
        }
    
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
    
    print(address.postal_code)
    print(address.to_dict())

if __name__ == "__main__":
    # Exemplo de uso
    exemplo()