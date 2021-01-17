import hashlib


def sha256(value: str) -> str:
    """Creates sha256 hash of value represented as hex string"""
    return hashlib.sha256(value.encode('utf-8')).hexdigest()