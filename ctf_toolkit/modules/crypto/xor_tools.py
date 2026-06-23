def _clean_hex(hex_text: str) -> str:
    """
    Cleans common hex formats.

    Supports:
        68656c6c6f
        68 65 6c 6c 6f
        0x68 0x65 0x6c 0x6c 0x6f
        \\x68\\x65\\x6c\\x6c\\x6f
    """
    if not isinstance(hex_text, str):
        raise TypeError("Hex text must be a string.")

    cleaned = (
        hex_text
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace("0x", "")
        .replace("0X", "")
        .replace("\\x", "")
        .replace("\\X", "")
    )

    if cleaned == "":
        raise ValueError("Hex input cannot be empty.")

    if len(cleaned) % 2 != 0:
        raise ValueError("Invalid hex input. Hex string must have an even number of characters.")

    return cleaned


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """
    XORs bytes with a repeating key.
    """
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes.")

    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes.")

    if len(key) == 0:
        raise ValueError("Key cannot be empty.")

    result = bytearray()

    for index, byte in enumerate(data):
        key_byte = key[index % len(key)]
        result.append(byte ^ key_byte)

    return bytes(result)


def xor_text_with_key_to_hex(text: str, key: str) -> str:
    """
    XORs normal text with a key and returns hexadecimal output.

    Example:
        text: hello
        key:  key
        output: 030015070a
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    if not isinstance(key, str):
        raise TypeError("Key must be a string.")

    if key == "":
        raise ValueError("Key cannot be empty.")

    data_bytes = text.encode("utf-8")
    key_bytes = key.encode("utf-8")

    encrypted_bytes = xor_bytes(data_bytes, key_bytes)

    return encrypted_bytes.hex()


def xor_hex_with_key_to_text(hex_text: str, key: str) -> str:
    """
    XORs hexadecimal input with a key and tries to return readable text.
    """
    if not isinstance(hex_text, str):
        raise TypeError("Hex text must be a string.")

    if not isinstance(key, str):
        raise TypeError("Key must be a string.")

    if key == "":
        raise ValueError("Key cannot be empty.")

    cleaned_hex = _clean_hex(hex_text)

    try:
        data_bytes = bytes.fromhex(cleaned_hex)

    except ValueError:
        raise ValueError("Invalid hex input.")

    key_bytes = key.encode("utf-8")
    decrypted_bytes = xor_bytes(data_bytes, key_bytes)

    try:
        return decrypted_bytes.decode("utf-8")

    except UnicodeDecodeError:
        raise ValueError("XOR result is not valid UTF-8 text.")


def _score_english_text(text: str) -> int:
    """
    Gives a simple score to text that looks readable.
    Higher score = more likely readable English/CTF text.
    """
    common_chars = " etaoinshrdluETAOINSHRDLU"
    useful_ctf_chars = "{}_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    score = 0

    for char in text:
        if char in common_chars:
            score += 3
        elif char in useful_ctf_chars:
            score += 2
        elif char.isprintable():
            score += 1
        else:
            score -= 5

    return score


def brute_force_single_byte_xor(hex_text: str, limit: int = 10) -> list[tuple[int, str, int]]:
    """
    Tries all single-byte XOR keys from 0 to 255.

    Returns best candidates:
        key number
        decoded text
        score
    """
    if not isinstance(hex_text, str):
        raise TypeError("Hex text must be a string.")

    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer.")

    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    cleaned_hex = _clean_hex(hex_text)

    try:
        data_bytes = bytes.fromhex(cleaned_hex)

    except ValueError:
        raise ValueError("Invalid hex input.")

    candidates = []

    for key in range(256):
        key_bytes = bytes([key])
        decoded_bytes = xor_bytes(data_bytes, key_bytes)
        decoded_text = decoded_bytes.decode("utf-8", errors="replace")
        score = _score_english_text(decoded_text)

        candidates.append((key, decoded_text, score))

    candidates.sort(key=lambda item: item[2], reverse=True)

    return candidates[:limit]