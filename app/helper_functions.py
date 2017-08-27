import uuid


def get_hash():
    return uuid.uuid4().hex[:10]
