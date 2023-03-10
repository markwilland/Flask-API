import secrets

def generate_key():
    key = secrets.token_urlsafe(16)
    return key

