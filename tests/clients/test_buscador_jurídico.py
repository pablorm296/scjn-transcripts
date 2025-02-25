from requests import Response
from pytest import fixture
import random

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.models.collector.response.búsqueda import BúsquedaResponse
from scjn_transcripts.clients.buscador_jurídico import BuscadorJurídicoApiClient

@fixture
def client() -> BuscadorJurídicoApiClient:
    return BuscadorJurídicoApiClient()

@fixture
def get_búsqueda_response(client: BuscadorJurídicoApiClient) -> Response:
    query = "*"
    index = "vtaquigraficas"
    page = 1
    size = 10

    return client.get_búsqueda(query, index, page, size)

def test_get_búsqueda_response(get_búsqueda_response: Response):
    assert get_búsqueda_response.status_code == 200
    assert get_búsqueda_response.json() is not None

def test_get_búsqueda_response_validation(get_búsqueda_response: Response):
    response_json = get_búsqueda_response.json()
    response = BúsquedaResponse(**response_json)

    # Check that the parsed response is an instance of BúsquedaResponse
    assert isinstance(response, BúsquedaResponse)

def test_get_documento_response(get_búsqueda_response: Response, client: BuscadorJurídicoApiClient):
    response_json = get_búsqueda_response.json()
    response = BúsquedaResponse(**response_json)
    document_id = random.choice(response.resultados).id

    get_documento_response = client.get_documento(document_id)

    assert get_documento_response.status_code == 200
    assert get_documento_response.json() is not None

def test_get_documento_response_validation(get_búsqueda_response: Response, client: BuscadorJurídicoApiClient):
    response_json = get_búsqueda_response.json()
    response = BúsquedaResponse(**response_json)
    document_id = random.choice(response.resultados).id

    get_documento_response = client.get_documento(document_id)
    response_json = get_documento_response.json()
    response = DocumentDetailsResponse(**response_json)

    # Check that the parsed response is an instance of DocumentDetailsResponse
    assert isinstance(response, DocumentDetailsResponse)

def test_get_print(get_búsqueda_response: Response, client: BuscadorJurídicoApiClient):
    response_json = get_búsqueda_response.json()
    response = BúsquedaResponse(**response_json)
    document_id = random.choice(response.resultados).id

    get_documento_response = client.get_documento(document_id)
    response_json = get_documento_response.json()
    response = DocumentDetailsResponse(**response_json)

    print_response = client.get_print(response.archivo)

    assert print_response.status_code == 200
    assert print_response.content is not None