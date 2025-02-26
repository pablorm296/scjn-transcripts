from requests.adapters import HTTPAdapter, Retry
import ua_generator
import requests

from scjn_transcripts.models.collector.index import IndexEnum
from scjn_transcripts.config import CONFIG

class BuscadorJurídicoApiClient:
    session: requests.Session
    ua: str
    host = CONFIG.collector.host
    path_search = CONFIG.collector.path_search
    path_document = CONFIG.collector.path_document
    path_print = CONFIG.collector.path_print

    def __init__(self):
        self.__init_session()
        self.__init_http_adapter()
        self.__set_ua()
        self.__set_origin_and_refer()

    def __init_session(self):
        self.session = requests.Session()

    def __init_http_adapter(self):
        retries = Retry(
            total = 3,
            connect = 0,
            backoff_factor = 0.1,
            status_forcelist = [500, 502, 503, 504]
        )

        self.session.mount("https://", HTTPAdapter(max_retries = retries))
        self.session.mount("http://", HTTPAdapter(max_retries = retries))

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
    
    def get_documento(self, id: str):
        response = self.session.get(
            f"{self.host}{self.path_document}/{id}"
        )

        return response
    
    def get_print(self, file_name: str):
        
        request_params = {
            "fileparams": f"filename:{file_name}"
        }

        response = self.session.get(
            f"{self.host}{self.path_print}",
            params = request_params
        )

        return response