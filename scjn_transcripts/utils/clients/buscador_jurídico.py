from requests import Response
import base64
import string

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
    
def response_is_text(response: Response, threshold: float = 0.9) -> bool:
    """
    Check if a given HTTP response contains predominantly text content.

    Args:
        response (Response): The HTTP response to check.
        threshold (float, optional): The minimum ratio of printable characters to total characters
                                     in the response content to consider it as text. Defaults to 0.9.

    Returns:
        bool: True if the response contains predominantly text content, False otherwise.
    """
    content = response.content[:1024]
    text_chars = bytes(string.printable, 'utf-8')
    num_printable_chars = sum(c in text_chars for c in content)
    return num_printable_chars / len(content) >= threshold