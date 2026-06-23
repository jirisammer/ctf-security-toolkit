import hashlib


SUPPORTED_HASH_ALGORITHMS = (
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
)


def list_supported_hashes() -> list[str]:
    """
    Returns a list of supported hash algorithms.
    """
    return list(SUPPORTED_HASH_ALGORITHMS)


def normalize_algorithm(algorithm: str) -> str:
    """
    Normalizes algorithm names.

    Examples:
        SHA256  -> sha256
        sha-256 -> sha256
        sha_256 -> sha256
    """
    if not isinstance(algorithm, str):
        raise TypeError("Algorithm must be a string.")

    normalized = (
        algorithm
        .lower()
        .replace("-", "")
        .replace("_", "")
        .strip()
    )

    if normalized not in SUPPORTED_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    return normalized


def generate_hash(text: str, algorithm: str) -> str:
    """
    Generates a hash from text using the selected algorithm.

    Example:
        generate_hash("hello", "sha256")
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    normalized_algorithm = normalize_algorithm(algorithm)

    hash_object = hashlib.new(normalized_algorithm)
    hash_object.update(text.encode("utf-8"))

    return hash_object.hexdigest()


def verify_hash(text: str, expected_hash: str, algorithm: str) -> bool:
    """
    Checks whether text matches the expected hash.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    if not isinstance(expected_hash, str):
        raise TypeError("Expected hash must be a string.")

    generated_hash = generate_hash(text, algorithm)

    return generated_hash.lower() == expected_hash.lower().strip()