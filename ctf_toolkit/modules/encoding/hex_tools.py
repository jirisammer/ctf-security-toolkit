def encode_hex(text: str) -> str:
    """
    Converts normal text into hexadecimal format.
    Example:
        hello -> 68656c6c6f
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text_bytes = text.encode("utf-8")
    return text_bytes.hex()


def decode_hex(hex_text: str) -> str:
    """
    Converts hexadecimal text back into normal text.
    Supports formats like:
        68656c6c6f
        68 65 6c 6c 6f
        0x68 0x65 0x6c 0x6c 0x6f
        \\x68\\x65\\x6c\\x6c\\x6f
    """
    if not isinstance(hex_text, str):
        raise TypeError("Input must be a string.")

    cleaned_hex = (
        hex_text
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace("0x", "")
        .replace("0X", "")
        .replace("\\x", "")
        .replace("\\X", "")
    )

    if cleaned_hex == "":
        raise ValueError("Hex input cannot be empty.")

    if len(cleaned_hex) % 2 != 0:
        raise ValueError("Invalid hex input. Hex string must have an even number of characters.")

    try:
        decoded_bytes = bytes.fromhex(cleaned_hex)
        return decoded_bytes.decode("utf-8")

    except ValueError:
        raise ValueError("Invalid hex input.")

    except UnicodeDecodeError:
        raise ValueError("Hex was decoded, but the result is not valid UTF-8 text.")