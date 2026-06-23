def encrypt_caesar(text: str, shift: int) -> str:
    """
    Encrypts text using Caesar cipher.

    Example:
        hello, shift 3 -> khoor
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    if not isinstance(shift, int):
        raise TypeError("Shift must be an integer.")

    result = []

    for char in text:
        if "a" <= char <= "z":
            shifted = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            result.append(shifted)

        elif "A" <= char <= "Z":
            shifted = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            result.append(shifted)

        else:
            result.append(char)

    return "".join(result)


def decrypt_caesar(text: str, shift: int) -> str:
    """
    Decrypts text encrypted by Caesar cipher.

    Example:
        khoor, shift 3 -> hello
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    if not isinstance(shift, int):
        raise TypeError("Shift must be an integer.")

    return encrypt_caesar(text, -shift)


def brute_force_caesar(text: str) -> dict[int, str]:
    """
    Tries all Caesar cipher shifts from 0 to 25.

    Useful for CTF tasks when the shift is unknown.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    results = {}

    for shift in range(26):
        results[shift] = decrypt_caesar(text, shift)

    return results