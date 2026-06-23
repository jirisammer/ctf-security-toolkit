import base64
import binascii


def encode_base64(text: str) -> str:
    """
    Converts normal text into Base64 format.
    Example:
        ahoj -> YWhvag==
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text_bytes = text.encode("utf-8")
    encoded_bytes = base64.b64encode(text_bytes)

    return encoded_bytes.decode("utf-8")


def decode_base64(encoded_text: str) -> str:
    """
    Converts Base64 text back into normal text.
    Example:
        YWhvag== -> ahoj
    """
    if not isinstance(encoded_text, str):
        raise TypeError("Input must be a string.")

    try:
        encoded_bytes = encoded_text.encode("utf-8")
        decoded_bytes = base64.b64decode(encoded_bytes, validate=True)

        return decoded_bytes.decode("utf-8")

    except binascii.Error:
        raise ValueError("Invalid Base64 input.")

    except UnicodeDecodeError:
        raise ValueError("Base64 was decoded, but the result is not valid UTF-8 text.")