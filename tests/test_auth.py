import time
from unittest.mock import AsyncMock, patch

import pytest
from cryptography.hazmat.primitives.asymmetric.ec import (
    SECP256R1,
    generate_private_key,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

# Generate a test EC P-256 key pair
_ec_private = generate_private_key(SECP256R1())
_ec_private_pem = _ec_private.private_bytes(
    Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
).decode()
_ec_public_pem = (
    _ec_private.public_key()
    .public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    .decode()
)

HS256_SECRET = "test-hs256-secret"


def _make_auth(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def _es256_token(payload: dict, kid: str = "test-kid") -> str:
    return jwt.encode(
        payload,
        _ec_private_pem,
        algorithm="ES256",
        headers={"kid": kid},
    )


def _hs256_token(payload: dict) -> str:
    return jwt.encode(payload, HS256_SECRET, algorithm="HS256")


@pytest.mark.asyncio
@patch("app.core.security.settings")
@patch("app.core.security._jwks")
async def test_es256_valid_token(mock_jwks, mock_settings):
    """ES256 토큰이 JWKS 공개키로 정상 검증된다."""
    mock_jwks.get_public_key = AsyncMock(return_value=_ec_public_pem)
    mock_settings.SUPABASE_JWT_SECRET = ""

    from app.core.security import get_current_user

    token = _es256_token({"sub": "user-abc", "aud": "authenticated"})
    user_id = await get_current_user(_make_auth(token))
    assert user_id == "user-abc"


@pytest.mark.asyncio
@patch("app.core.security.settings")
async def test_hs256_legacy_fallback(mock_settings):
    """HS256 레거시 토큰이 SUPABASE_JWT_SECRET으로 검증된다."""
    mock_settings.SUPABASE_JWT_SECRET = HS256_SECRET
    mock_settings.SUPABASE_URL = ""
    mock_settings.JWKS_CACHE_TTL = 86400

    from app.core.security import get_current_user

    token = _hs256_token({"sub": "user-legacy", "aud": "authenticated"})
    user_id = await get_current_user(_make_auth(token))
    assert user_id == "user-legacy"


@pytest.mark.asyncio
@patch("app.core.security.settings")
async def test_expired_token_returns_401(mock_settings):
    """만료된 토큰은 401을 반환한다."""
    mock_settings.SUPABASE_JWT_SECRET = HS256_SECRET
    mock_settings.SUPABASE_URL = ""
    mock_settings.JWKS_CACHE_TTL = 86400

    from app.core.security import get_current_user

    token = _hs256_token(
        {"sub": "user-exp", "aud": "authenticated", "exp": time.time() - 3600}
    )
    with pytest.raises(HTTPException) as exc:
        await get_current_user(_make_auth(token))
    assert exc.value.status_code == 401


@pytest.mark.asyncio
@patch("app.core.security.settings")
async def test_invalid_signature_returns_401(mock_settings):
    """잘못된 서명의 토큰은 401을 반환한다."""
    mock_settings.SUPABASE_JWT_SECRET = HS256_SECRET
    mock_settings.SUPABASE_URL = ""
    mock_settings.JWKS_CACHE_TTL = 86400

    from app.core.security import get_current_user

    token = jwt.encode(
        {"sub": "user-bad", "aud": "authenticated"}, "wrong-secret", algorithm="HS256"
    )
    with pytest.raises(HTTPException) as exc:
        await get_current_user(_make_auth(token))
    assert exc.value.status_code == 401


@pytest.mark.asyncio
@patch("app.core.security.settings")
async def test_missing_sub_returns_401(mock_settings):
    """sub 클레임이 없는 토큰은 401을 반환한다."""
    mock_settings.SUPABASE_JWT_SECRET = HS256_SECRET
    mock_settings.SUPABASE_URL = ""
    mock_settings.JWKS_CACHE_TTL = 86400

    from app.core.security import get_current_user

    token = _hs256_token({"aud": "authenticated"})
    with pytest.raises(HTTPException) as exc:
        await get_current_user(_make_auth(token))
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token_format():
    """잘못된 형식의 토큰은 401을 반환한다."""
    from app.core.security import get_current_user

    with pytest.raises(HTTPException) as exc:
        await get_current_user(_make_auth("not.a.valid.jwt"))
    assert exc.value.status_code == 401
