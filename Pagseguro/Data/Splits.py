from typing import List, Optional
from enum import Enum

class SplitMethod(Enum):
   FIXED = 0
   PERCENTAGE = 1

class Amount:
    def __init__(self, value: int):
        """
        Contém informações dos valores dos recebedores participantes da divisão.

        :param value: Valor destinado ao recebedor (em centavos ou percentual, dependendo do método FIXED/PERCENTAGE).
        """
        if value <= 0:
            raise ValueError("O valor deve ser um número inteiro positivo.")
        self.value = value

    def __repr__(self):
        return f"Amount(value={self.value})"

    def to_dict(self):
        return {
            "value": self.value
        }

class Account:
    def __init__(self, id: str):
        """
        Contém informações da conta do recebedor participante.

        :param id: Identificador único da conta PagBank (máximo 41 caracteres).
        """
        if len(id) > 41:
            raise ValueError("O ID da conta não pode exceder 41 caracteres.")
        self.id = id

    def __repr__(self):
        return f"Account(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id
        }

class Custody:
    def __init__(self, apply: bool, chargeback: Optional[int] = None):
        """
        Contém informações das configurações de custódia.

        :param apply: Define se a transação terá custódia.
        :param chargeback: Porcentagem do valor do chargeback repassado ao recebedor (default: 100%).
        """
        self.apply = apply
        self.chargeback = chargeback if chargeback is not None else 100

    def __repr__(self):
        return f"Custody(apply={self.apply}, chargeback={self.chargeback})"

    def to_dict(self):
        return {
            "apply": self.apply,
            "chargeback": self.chargeback
        }

class Receiver:
    def __init__(self, amount: Amount, account: Account, custody: Optional[Custody] = None, reason: Optional[str] = None):
        """
        Contém as informações do recebedor participante da divisão de pagamento.

        :param amount: Valor destinado ao recebedor.
        :param account: Conta do recebedor.
        :param custody: Configurações de custódia.
        :param reason: Descrição opcional para cada recebedor.
        """
        self.amount = amount
        self.account = account
        self.custody = custody
        self.reason = reason

    def __repr__(self):
        return f"Receiver(amount={self.amount}, account={self.account}, custody={self.custody}, reason={self.reason})"

    def to_dict(self):
        return {
            "amount": self.amount.to_dict(),
            "account": self.account.to_dict(),
            "custody": self.custody.to_dict() if self.custody else None,
            "reason": self.reason
        }

class Splits:
    def __init__(self, method: str, receivers: List[Receiver]):
        """
        Contém informações da divisão de pagamento.

        :param method: Define se os valores da divisão serão informados em valores FIXED ou PERCENTAGE.
        :param receivers: Lista de recebedores participantes da divisão.
        """
        if method not in ["FIXED", "PERCENTAGE"]:
            raise ValueError("O método deve ser 'FIXED' ou 'PERCENTAGE'.")
        self.method = method
        self.receivers = receivers

    def __repr__(self):
        return f"Splits(method={self.method}, receivers={self.receivers})"

    def to_dict(self):
        return {
            "method": self.method,
            "receivers": [receiver.to_dict() for receiver in self.receivers]
        }

def exemplo():
    amount = Amount(150099)
    account = Account("12345678901234567890123456789012345678901")
    custody = Custody(apply=True, chargeback=100)
    receiver = Receiver(amount=amount, account=account, custody=custody, reason="Divisão do pagamento")
    method = SplitMethod(0).name
    #print(method)
    splits = Splits(method=method, receivers=[receiver])
    print(splits)


# Exemplo de uso
if __name__ == "__main__":
    exemplo()