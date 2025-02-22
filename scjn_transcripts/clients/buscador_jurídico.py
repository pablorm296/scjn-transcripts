import requests
import ua_generator

from scjn_transcripts.config import CONFIG
from scjn_transcripts.models.collector.index import IndexEnum

class BuscadorJurídicoApiClient:
    session: requests.Session
    ua: str
    host = CONFIG.collector.host
    path_search = CONFIG.collector.path_search

    def __init__(self):
        self.__init_session()
        self.__set_ua()
        self.__set_origin_and_refer()

    def __init_session(self):
        self.session = requests.Session()

    def __set_ua(self):
        self.ua = ua_generator.generate().text
        self.session.headers.update({
            "User-Agent": self.ua
        })

    def __set_origin_and_refer(self):
        self.session.headers.update({
            "Origin": self.host,
            "Referer": self.host
        })

    def get_búsqueda(self, query: str, index: IndexEnum, page: int = 1, size: int = 10):
        
        request_params = {
            "q": query,
            "indice": index,
            "pagina": page,
            "size": size,
        }

        response = self.session.get(
            f"{self.host}{self.path_search}",
            params = request_params
        )

        return response