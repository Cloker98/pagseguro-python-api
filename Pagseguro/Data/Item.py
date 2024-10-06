class Item:
    def __init__(self, name: str, unit_amount: int, quantity: int = 1, reference_id: str = None):
        """
        Item de uma venda/pedido.

        :param name: Nome (descrição) do item.
        :param unit_amount: Valor unitário em centavos, sendo o valor mínimo 100 centavos (R$ 1,00).
        :param quantity: Quantidade do item no pedido (padrão é 1).
        :param reference_id: ID de referência opcional.
        """
        self.name = name
        self.unit_amount = unit_amount
        self.quantity = quantity
        self.reference_id = reference_id

    def __repr__(self):
        return f"Item(name={self.name}, unit_amount={self.unit_amount}, quantity={self.quantity}, reference_id={self.reference_id})"
    
    def to_dict(self):
        return {
            "name": self.name,
            "unit_amount": self.unit_amount,
            "quantity": self.quantity
        }

def exemplo():
    item1 = Item("Produto A", 1500)  # Cria um item com quantidade 1 e sem reference_id
    item2 = Item("Produto B", 2000, 2)  # Cria um item com quantidade 2 e sem reference_id
    item3 = Item("Produto C", 2500, 3, "REF123")  # Cria um item com quantidade 3 e reference_id "REF123"

    print(item1)
    print(item2)
    print(item3)

# Exemplo de uso
if __name__ == "__main__":
    exemplo()