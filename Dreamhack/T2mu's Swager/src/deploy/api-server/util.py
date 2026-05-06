import hmac
import hashlib

def verify_hmac(message: str, signature: str) -> bool:
    ADMIN_SECRET_KEY = "admin"
    GUEST_SECRET_KEY = "guest"

    admin_computed_hmac = hmac.new(
        key=ADMIN_SECRET_KEY.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

    guest_computed_hmac = hmac.new(
        key=GUEST_SECRET_KEY.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

    if (hmac.compare_digest(admin_computed_hmac, signature) or hmac.compare_digest(guest_computed_hmac, signature)):
        return True

    return False

def generate_hmac(secret_key: str, message: str) -> str:
    return hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()