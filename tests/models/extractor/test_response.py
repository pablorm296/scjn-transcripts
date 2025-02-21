from pydantic import ValidationError
from pytest import fixture, raises
import json

from scjn_transcripts.models.extractor.response import BúsquedaResponse

@fixture
def búsqueda_test_data():
    # Load test data from file
    with open("tests/data/extractor/test-response.json", "r") as file:
        data: dict = json.load(file)
    
    return data

def test_búsqueda_response_model(búsqueda_test_data: dict):
    # Test that the model can be created from the test data
    parsed_response = BúsquedaResponse(**búsqueda_test_data)
    
    # Check that the parsed response is an instance of BúsquedaResponse
    assert isinstance(parsed_response, BúsquedaResponse)

def test_faulty_response():
    faulty_response = {
        "invalid_key": "invalid_value"
    }

    with raises(ValidationError):
        BúsquedaResponse(**faulty_response)
