from requests import Response
from pytest import fixture

from scjn_transcripts.clients.buscador_jurídico import BuscadorJurídicoApiClient
from scjn_transcripts.models.collector.response import BúsquedaResponse

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
