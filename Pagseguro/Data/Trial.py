import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Trial:
    def __init__(self, days: int, enabled: bool, hold_setup_fee: bool):
        """
        Representa os detalhes sobre o período de teste (trial) de um plano.

        :param days: Número de dias do período de teste/trial do plano. Exemplo: 1.
        :param enabled: Indica se o período de teste/trial está ativado. Exemplo: True.
        :param hold_setup_fee: Indica se a taxa de configuração é retida durante o período de teste. Exemplo: False.
        """
        self.days = days
        self.enabled = enabled
        self.hold_setup_fee = hold_setup_fee

    def __repr__(self):
        """
        Retorna uma representação em string do objeto Trial, contendo os dias, se o trial está ativado e se a taxa de configuração é retida.

        :return: String representativa do objeto Trial.
        """
        return f"Trial(days={self.days}, enabled={self.enabled}, hold_setup_fee={self.hold_setup_fee})"
    
    def to_dict(self):
        """
        Converte o objeto Trial para um dicionário, contendo os atributos 'days', 'enabled' e 'hold_setup_fee'.

        :return: Dicionário com as chaves 'days' (número de dias do teste), 'enabled' (ativação do teste) e 'hold_setup_fee' (retenção da taxa de configuração).
        """
        return {
            "days": self.days,  # Exemplo: 1
            "enabled": self.enabled,  # Exemplo: True
            "hold_setup_fee": self.hold_setup_fee  # Exemplo: False
        }

def exemplo_trial():
    """
    Exemplo de uso da classe Trial. Cria e imprime detalhes sobre períodos de teste/trial com diferentes configurações.

    :return: None
    """
    trial_ativo = Trial(7, True, True) # Padrão para o Brasil segundo a lei 
    trial_desativado = Trial(0, False, True)

    print(trial_ativo.to_dict())
    print(trial_desativado.to_dict())

# Exemplo de uso
if __name__ == "__main__":
    exemplo_trial()