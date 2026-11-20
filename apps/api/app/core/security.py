from dataclasses import dataclass
from functools import lru_cache
from typing import Any
import jwt
from fastapi import Depends, Header, HTTPException, status
from jwt import PyJWKClient
from app.core.config import settings

@dataclass(frozen=True)
class Principal:
    subject: str
    roles_by_org: dict[str, list[str]]
    is_dev: bool = False

@lru_cache
def _jwks_client() -> PyJWKClient:
    if not settings.oidc_jwks_url:
        raise RuntimeError("OIDC_JWKS_URL is required")
    return PyJWKClient(settings.oidc_jwks_url)

async def current_principal(
    authorization: str | None = Header(default=None),
    x_dev_user: str | None = Header(default=None),
    x_dev_org: str | None = Header(default=None),
    x_dev_roles: str | None = Header(default=None),
) -> Principal:
    # Explicitly opt-in local-only development identity. Never enable outside development.
    if settings.app_env == "development" and settings.dev_auth_enabled and x_dev_user and x_dev_org:
        return Principal(x_dev_user, {x_dev_org: [r.strip() for r in (x_dev_roles or "organization_owner").split(",")]}, True)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        signing_key = _jwks_client().get_signing_key_from_jwt(token).key
        claims: dict[str, Any] = jwt.decode(
            token, signing_key, algorithms=["RS256", "ES256"],
            audience=settings.oidc_audience, issuer=settings.oidc_issuer,
            options={"require": ["exp", "iat", "sub", "iss", "aud"]},
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    org_roles = claims.get(settings.oidc_org_roles_claim, {})
    if not isinstance(org_roles, dict):
        raise HTTPException(status_code=403, detail="Organization role claim must be an object")
    clean = {str(org): [str(role) for role in roles] for org, roles in org_roles.items() if isinstance(roles, list)}
    return Principal(subject=str(claims["sub"]), roles_by_org=clean)

def require_org_role(org_id: str, allowed: set[str], principal: Principal) -> None:
    roles = set(principal.roles_by_org.get(org_id, []))
    if not roles.intersection(allowed):
        raise HTTPException(status_code=403, detail="Insufficient organization permission")

def require_platform_admin(principal: Principal) -> None:
    if not any("platform_admin" in roles for roles in principal.roles_by_org.values()):
        raise HTTPException(status_code=403, detail="Platform administrator permission required")
