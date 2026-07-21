import base64
import time

import httpx
from cryptography.hazmat.primitives.asymmetric.ec import (
    SECP256R1,
    EllipticCurvePublicNumbers,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings

_bearer = HTTPBearer()


def _b64url_decode(data: str) -> bytes:
    rem = len(data) % 4
    if rem:
        data += "=" * (4 - rem)
    return base64.urlsafe_b64decode(data)


class JWKSCache:
    """JWKS를 fetch하여 EC(P-256) 공개키를 PEM으로 변환 후 캐싱."""

    def __init__(self) -> None:
        self._cache: dict[str, str] = {}  # kid -> PEM
        self._last_updated: float = 0

    async def get_public_key(self, kid: str) -> str | None:
        now = time.time()
        if kid in self._cache and (now - self._last_updated) < settings.JWKS_CACHE_TTL:
            return self._cache[kid]

        # Cache miss or expired — refresh
        jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(jwks_url)
                resp.raise_for_status()
                jwks = resp.json()
        except Exception:
            return self._cache.get(kid)  # fallback to stale cache

        new_cache: dict[str, str] = {}
        for key in jwks.get("keys", []):
            if key.get("kty") != "EC" or key.get("crv") != "P-256":
                continue
            k_id = key.get("kid", "")
            x_bytes = _b64url_decode(key["x"])
            y_bytes = _b64url_decode(key["y"])
            pub_numbers = EllipticCurvePublicNumbers(
                x=int.from_bytes(x_bytes, "big"),
                y=int.from_bytes(y_bytes, "big"),
                curve=SECP256R1(),
            )
            pem = (
                pub_numbers.public_key()
                .public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
                .decode()
            )
            new_cache[k_id] = pem

        self._cache = new_cache
        self._last_updated = time.time()
        return self._cache.get(kid)


_jwks = JWKSCache()


async def get_current_user(
    auth: HTTPAuthorizationCredentials = Security(_bearer),
) -> str:
    token = auth.credentials

    try:
        header = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token format")

    alg = header.get("alg")
    kid = header.get("kid")

    # Path 1: ES256 (ECC P-256) — new default
    if alg == "ES256" and kid:
        pem = await _jwks.get_public_key(kid)
        if pem:
            try:
                payload = jwt.decode(
                    token, pem, algorithms=["ES256"], audience="authenticated"
                )
                user_id = payload.get("sub")
                if not user_id:
                    raise HTTPException(
                        status_code=401, detail="Invalid token payload"
                    )
                return user_id
            except JWTError:
                pass  # fall through to HS256 during migration

    # Path 2: HS256 (legacy fallback)
    if settings.SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=401, detail="Invalid token payload"
                )
            return user_id
        except JWTError:
            pass

    raise HTTPException(status_code=401, detail="Could not validate credentials")
