from typing import List, Optional
from datetime import datetime

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.QrCode import QrCode
from Service.Response.Link import Link
from Data.Charge import Charge
from Data.Customer import Customer
from Data.Item import Item
from Data.Shipping import Shipping

class PixOrder:
    def __init__(self, reference_id: str, customer: Customer, qrcode: Optional[QrCode] = None, notification_url: Optional[str] = None, items: Optional[List[Item]] = None):
        #self.id = None
        self.reference_id = reference_id
        #self.created_at = None
        self.customer = customer
        self.items = items if items is not None else []
        self.qr_codes = [qrcode] if qrcode else []
        self.shipping = None
        #self.links = []
        self.notification_urls = [notification_url] if notification_url else []
        #self.charges = []

    @staticmethod
    def get_single_list(value: Optional[str]) -> List[str]:
        if not value or not value.strip():
            return []
        return [value]
    
    '''
    def __repr__(self):
        return (f"PixOrder(id={self.id}, reference_id={self.reference_id}, created_at={self.created_at}, "
                f"customer={self.customer}, items={self.items}, qr_codes={self.qr_codes}, "
                f"shipping={self.shipping}, links={self.links}, notification_urls={self.notification_urls}, "
                f"charges={self.charges})")
    '''
    def __repr__(self):
        return (f"PixOrder(reference_id={self.reference_id},"
                f"customer={self.customer}, items={self.items}, qr_codes={self.qr_codes}, "
                f"shipping={self.shipping}, notification_urls={self.notification_urls})")
    
    def to_dict(self):
        return {
            "reference_id": self.reference_id,
            "customer": self.customer.to_dict(),
            "qr_codes": [qr_code.to_dict() for qr_code in self.qr_codes],
            "notification_url": self.notification_urls,
            "items": [item.to_dict() for item in self.items]
        }
    

# Função fora da Classe para testar a Classe
def exemplo():
    # Criando instâncias de teste
    customer = Customer(name="John Doe", email="john@example.com", tax_id="92410172016")
    item = Item(name="Test Item", unit_amount=1000, quantity=2)
    expiration_date = datetime.strptime("2021-08-29T20:15:59-03:00", QrCode.DATE_TIME_FORMAT)
    qrcode = QrCode(id="123", text="Copia e Cola", amount=500, expiration_date=expiration_date)
    pix_order = PixOrder(reference_id="ref123", customer=customer, qrcode=qrcode, notification_url="http://example.com/notify", items=[item])

    print(pix_order.to_dict())

# Exemplo de uso
if __name__ == "__main__":
    exemplo()