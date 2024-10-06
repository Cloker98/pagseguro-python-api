from datetime import datetime, timedelta, timezone
from typing import List, Optional

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Service.Response.Link import Link
from Data.Splits import Splits

class QrCode:
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

    id: Optional[str]
    text: Optional[str]
    amount: int
    expiration_date: datetime
    splits: Optional[Splits] = None  # Campo Splits opcional
    arrangements: Optional[List[str]] = None
    links: Optional[List[Link]] = None

    def __init__(self, amount: int, expiration_date: datetime, id: Optional[str] = None, text: Optional[str] = None, splits: Optional[Splits] = None, links: Optional[List[Link]] = None, arrangements: Optional[List[str]] = None):
        self.id = self.non_blank(id)
        self.text = self.non_blank(text)
        self.amount = amount
        self.expiration_date = self.add_timezone(expiration_date)
        self.arrangements = arrangements or []
        self.links = links or []
        self.splits = splits  # Atribuindo Splits

    @staticmethod
    def non_blank(value: Optional[str]) -> Optional[str]:
        """Retorna None se o valor for nulo ou vazio, senão retorna o valor."""
        return None if value is None or value.strip() == '' else value
    
    @staticmethod
    def add_timezone(dt: datetime) -> datetime:
        """Adiciona o fuso horário ao objeto datetime, se não tiver."""
        if dt.tzinfo is None:
            # Adiciona o fuso horário padrão (-03:00)
            return dt.replace(tzinfo=timezone(timedelta(hours=-3)))
        return dt
    
    def __repr__(self):
        # Usando isoformat para incluir milissegundos e fuso horário
        return (f'{{"amount": {self.amount}, "expiration_date": "{self.expiration_date.isoformat(timespec="milliseconds")}"}}')
    
    
    def to_dict(self):
        data = {
            "amount": {
                "value": self.amount
            },
            "expiration_date": self.expiration_date.isoformat(timespec="milliseconds"),
        }
        if self.splits:
            data["splits"] = self.splits.to_dict()  # Inclui splits no dicionário, se existir
        return data

# Função fora da Classe para testar a Classe
def exemplo():
    expiration_date = datetime.now() + timedelta(days=3)  # Data de expiração futura (3 dias no futuro)
    qr_code = QrCode(amount=500, expiration_date=expiration_date)  # Passando expiration_date como objeto datetime
    print(qr_code)
    print(f"QR Code: {qr_code.id}, Texto: {qr_code.text}, Valor: {qr_code.amount}, Expiração: {qr_code.expiration_date}")
    print(qr_code.to_dict())
if __name__ == "__main__":
    # Exemplo de uso
    exemplo()