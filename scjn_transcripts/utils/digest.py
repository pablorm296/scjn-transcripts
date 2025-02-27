import hashlib

def get_digest(data: dict) -> str:
    hash_object = hashlib.sha256()
    for key in sorted(data.keys()):
        hash_object.update(f"{key}={data[key]}".encode("utf-8"))
    return hash_object.hexdigest()

def check_digest(data: dict, digest: str) -> bool:
    return digest == get_digest(data)