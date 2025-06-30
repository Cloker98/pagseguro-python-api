from enum import Enum

class HTTPMethod(Enum):
   GET = 0
   POST = 1
   DELETE = 2
   PUT = 3

class Link:
    def __init__(self, rel: str, href: str, media: str, type: str):
        """
        Representa um link associado a um QRCode ou outra entidade.

        :param rel: Relacionamento do link (por exemplo, "self").
        :param href: URL do link.
        :param media: Tipo de mídia associada ao link, ou conteúdo do link ((por exemplo, "application/json").)
        :param type: Método HTTP em uso. ("GET, POST, DELETE, PUT")
        """
        self.rel = rel
        self.href = href
        self.media = media
        self.type = type

    def __repr__(self):
        return (f"Link(rel={self.rel}, href={self.href}, media={self.media}, "
                f"type={self.type})")
    
    def to_dict(self):
        return {
            "rel": self.rel,
            "href": self.href,
            "media": self.media,
            "type": self.type
        }

# Função fora da Classe para testar a Classe
def exemplo():
    httpMethod = HTTPMethod(0).name
    print(httpMethod)
    link = Link("self", "https://example.com", "application/json", "GET")
    print(link)
    print(link.to_dict())

# Exemplo de uso
if __name__ == "__main__":
    exemplo()
