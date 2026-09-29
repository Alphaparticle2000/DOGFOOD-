from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
import base64

_private_key = Ed25519PrivateKey.generate()


def sign_scorecard_hash(scorecard_hash: str) -> str:
    signature = _private_key.sign(scorecard_hash.encode("utf-8"))
    return base64.b64encode(signature).decode("ascii")


def verify_scorecard_hash(scorecard_hash: str, signature: str) -> bool:
    try:
        public_key = _private_key.public_key()
        public_key.verify(
            base64.b64decode(signature),
            scorecard_hash.encode("utf-8"),
        )
        return True
    except Exception:
        return False