from urllib.parse import quote, unquote


def encode_url(text: str) -> str:
    """
    Converts normal text into URL encoded format.
    Example:
        flag{hello world} -> flag%7Bhello%20world%7D
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    return quote(text, safe="")


def decode_url(encoded_text: str) -> str:
    """
    Converts URL encoded text back into normal text.
    Example:
        flag%7Bhello%20world%7D -> flag{hello world}
    """
    if not isinstance(encoded_text, str):
        raise TypeError("Input must be a string.")

    return unquote(encoded_text)