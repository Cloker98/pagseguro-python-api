import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Interval:
    def __init__(self, length: int, unit: str):
        """
        Representa um intervalo de tempo para definir a duração e unidade de medida de um período específico.

        :param length: Duração do intervalo de cobrança. O valor padrão é 1, mas pode variar de -2147483648 a 2147483647.
        :param unit: Unidade de medida do intervalo de cobrança. Opções válidas são "DAY", "MONTH", "YEAR", com o valor padrão sendo "MONTH".
        """
        self.length = length
        self.unit = unit

    def __repr__(self):
        """
        Retorna uma representação em string do objeto Interval, contendo a unidade e a duração do intervalo.

        :return: String representativa do objeto Interval.
        """
        return f"Interval(unit={self.unit}, length={self.length})"
    
    def to_dict(self):
        """
        Converte o objeto Interval para um dicionário, contendo os atributos 'unit' e 'length'.

        :return: Dicionário com as chaves 'unit' (unidade de medida) e 'length' (duração do intervalo).
        """
        return {
            "unit": self.unit, #"DAY", "MONTH", "YEAR"
            "length": self.length
        }

def exemplo():
    """
    Exemplo de uso da classe Interval. Cria e imprime intervalos de tempo mensais, semestrais e anuais.

    :return: None
    """
    mensal = Interval(1, "MONTH")  
    semestral = Interval(6,  "MONTH")  
    anual = Interval(1, "YEAR")  

    print(mensal.to_dict())
    print(semestral.to_dict())
    print(anual.to_dict())

# Exemplo de uso
if __name__ == "__main__":
    exemplo()