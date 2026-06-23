def rot13(text: str) -> str:
    """
    Applies ROT13 transformation to text.

    ROT13 shifts letters by 13 positions.
    Applying ROT13 twice returns the original text.

    Example:
        hello -> uryyb
        uryyb -> hello
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    result = []

    for char in text:
        if "a" <= char <= "z":
            shifted = chr((ord(char) - ord("a") + 13) % 26 + ord("a"))
            result.append(shifted)

        elif "A" <= char <= "Z":
            shifted = chr((ord(char) - ord("A") + 13) % 26 + ord("A"))
            result.append(shifted)

        else:
            result.append(char)

    return "".join(result)