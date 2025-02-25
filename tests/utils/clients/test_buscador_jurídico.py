import requests

from scjn_transcripts.utils.clients.buscador_jurídico import response_is_text, text_is_base64

def test_response_is_not_text():
    URL_WITH_A_BINARY_FILE = "https://github.com/Qix-/test-binary-file/raw/refs/heads/master/blah.bin"
    response = requests.get(URL_WITH_A_BINARY_FILE)
    assert not response_is_text(response)

def test_scjn_pdf_is_not_text():
    URL_WITH_A_PDF_FILE = "https://www.scjn.gob.mx/sites/default/files/versiones-taquigraficas/documento/2025-02-24/24%20de%20febrero%20de%202025%20-%20Versi%C3%B3n%20definitiva.pdf"
    response = requests.get(URL_WITH_A_PDF_FILE)
    assert not response_is_text(response)

def test_text_is_text():
    assert response_is_text(requests.get("https://www.google.com"))

def test_text_is_base64():
    BASE_64_STRING = "SGVsbG8sIFdvcmxkIQ=="
    assert text_is_base64(BASE_64_STRING)

def test_text_is_not_base64():
    assert not text_is_base64("Hello, world!")
