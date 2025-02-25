from requests import Response
import base64

def text_is_base64(text: str) -> bool:
    """
    Check if a given text is a valid Base64 encoded string.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text is a valid Base64 encoded string, False otherwise.
    """
    try:
        return base64.b64encode(base64.b64decode(text)) == text
    except Exception:
        return False
    
def response_is_text(response: Response) -> bool:
    """
    Check if a given HTTP response contains text content.

    Args:
        response (Response): The HTTP response to check.

    Returns:
        bool: True if the response contains text content, False otherwise.
    """
    try:
        response.text
        return True
    except Exception:
        return False