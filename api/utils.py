import jwt


def verify_telegram_signature(received_hash: str, secret: str) -> dict | int:
    """Verify the received hash to check the signature."""

    try:
        payload = jwt.decode(jwt=received_hash, key=secret, algorithms=['HS256'])
        del payload["exp"]
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2

    return payload