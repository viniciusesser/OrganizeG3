"""Supabase access-token verification using the project JWKS."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

from jose import JWTError, jwt  # type: ignore[import-untyped]

from organizeg3_api.application.identity.exceptions import (
    AuthenticationProviderUnavailableError,
    InvalidAccessTokenError,
    SupabaseAuthenticationConfigurationError,
)
from organizeg3_api.domain.identity.authentication import (
    TokenVerifier,
    VerifiedToken,
)

Jwk = dict[str, object]

_ALLOWED_ALGORITHMS = frozenset(
    {
        "RS256",
        "ES256",
    }
)

_ALLOWED_LOCAL_HOSTS = frozenset(
    {
        "localhost",
        "127.0.0.1",
    }
)


def _is_allowed_remote_url(
    url: str,
) -> bool:
    """Return whether a URL is safe for authentication metadata retrieval."""

    try:
        parsed_url = urllib.parse.urlsplit(
            url
        )
    except ValueError:
        return False

    if (
        parsed_url.username is not None
        or parsed_url.password is not None
        or not parsed_url.hostname
    ):
        return False

    if parsed_url.scheme == "https":
        return True

    return (
        parsed_url.scheme == "http"
        and parsed_url.hostname
        in _ALLOWED_LOCAL_HOSTS
    )


@dataclass(slots=True)
class RemoteJwksProvider:
    """Load and temporarily cache Supabase public signing keys."""

    jwks_url: str
    timeout_seconds: float = 5.0
    cache_ttl_seconds: float = 600.0

    _cached_keys: tuple[Jwk, ...] = field(
        default_factory=tuple,
        init=False,
        repr=False,
    )

    _expires_at: float = field(
        default=0.0,
        init=False,
        repr=False,
    )

    _lock: threading.Lock = field(
        default_factory=threading.Lock,
        init=False,
        repr=False,
    )

    def __post_init__(
        self,
    ) -> None:
        """Validate the configured JWKS endpoint."""

        normalized_url = (
            self.jwks_url.strip()
        )

        if not _is_allowed_remote_url(
            normalized_url
        ):
            raise (
                SupabaseAuthenticationConfigurationError
            )

        self.jwks_url = normalized_url

    def get_keys(
        self,
        *,
        force_refresh: bool = False,
    ) -> tuple[Jwk, ...]:
        """Return cached keys or refresh them from Supabase."""

        current_time = time.monotonic()

        if (
            not force_refresh
            and self._cached_keys
            and current_time
            < self._expires_at
        ):
            return self._cached_keys

        with self._lock:
            current_time = time.monotonic()

            if (
                not force_refresh
                and self._cached_keys
                and current_time
                < self._expires_at
            ):
                return self._cached_keys

            keys = self._fetch_keys()

            self._cached_keys = keys
            self._expires_at = (
                current_time
                + self.cache_ttl_seconds
            )

            return keys

    def _fetch_keys(
        self,
    ) -> tuple[Jwk, ...]:
        """Fetch and validate the remote JWKS document."""

        request = urllib.request.Request(  # noqa: S310
            self.jwks_url,
            headers={
                "Accept": "application/json",
            },
            method="GET",
        )

        try:
            with urllib.request.urlopen(  # noqa: S310
                request,
                timeout=self.timeout_seconds,
            ) as response:
                response_body = (
                    response.read()
                )
        except (
            OSError,
            TimeoutError,
            urllib.error.URLError,
        ) as exception:
            raise (
                AuthenticationProviderUnavailableError
            ) from exception

        try:
            payload: object = json.loads(
                response_body
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exception:
            raise (
                AuthenticationProviderUnavailableError
            ) from exception

        return self._parse_keys(
            payload
        )

    @staticmethod
    def _parse_keys(
        payload: object,
    ) -> tuple[Jwk, ...]:
        """Parse usable signing keys from a JWKS payload."""

        if not isinstance(
            payload,
            dict,
        ):
            raise (
                AuthenticationProviderUnavailableError
            )

        raw_keys = payload.get(
            "keys"
        )

        if not isinstance(
            raw_keys,
            list,
        ):
            raise (
                AuthenticationProviderUnavailableError
            )

        parsed_keys: list[Jwk] = []

        for raw_key in raw_keys:
            if not isinstance(
                raw_key,
                dict,
            ):
                continue

            parsed_key: Jwk = {
                key: value
                for key, value
                in raw_key.items()
                if isinstance(
                    key,
                    str,
                )
            }

            if parsed_key:
                parsed_keys.append(
                    parsed_key
                )

        if not parsed_keys:
            raise (
                AuthenticationProviderUnavailableError
            )

        return tuple(
            parsed_keys
        )


@dataclass(frozen=True, slots=True)
class SupabaseJwtVerifier(TokenVerifier):
    """Verify Supabase access tokens against public signing keys."""

    issuer: str
    jwks_provider: RemoteJwksProvider

    def verify(
        self,
        access_token: str,
    ) -> VerifiedToken:
        """Verify signature and required Supabase claims."""

        if not access_token.strip():
            raise InvalidAccessTokenError

        header = self._read_header(
            access_token
        )

        algorithm = header.get(
            "alg"
        )

        key_id = header.get(
            "kid"
        )

        if (
            not isinstance(
                algorithm,
                str,
            )
            or algorithm
            not in _ALLOWED_ALGORITHMS
            or not isinstance(
                key_id,
                str,
            )
            or not key_id.strip()
        ):
            raise InvalidAccessTokenError

        signing_key = (
            self._find_signing_key(
                key_id=key_id,
                algorithm=algorithm,
            )
        )

        try:
            claims = jwt.decode(
                access_token,
                signing_key,
                algorithms=[
                    algorithm,
                ],
                audience="authenticated",
                issuer=self.issuer,
            )
        except (
            JWTError,
            TypeError,
            ValueError,
        ) as exception:
            raise (
                InvalidAccessTokenError
            ) from exception

        if not isinstance(
            claims,
            dict,
        ):
            raise InvalidAccessTokenError

        role = claims.get(
            "role"
        )

        if role != "authenticated":
            raise InvalidAccessTokenError

        auth_user_id = (
            self._required_uuid_claim(
                claims,
                "sub",
            )
        )

        session_id = (
            self._optional_uuid_claim(
                claims,
                "session_id",
            )
        )

        raw_email = claims.get(
            "email"
        )

        email = (
            raw_email
            .strip()
            .lower()
            if isinstance(
                raw_email,
                str,
            )
            and raw_email.strip()
            else None
        )

        return VerifiedToken(
            auth_user_id=auth_user_id,
            role=role,
            email=email,
            session_id=session_id,
        )

    @staticmethod
    def _read_header(
        access_token: str,
    ) -> dict[str, object]:
        """Read the unverified JWT header used to select a public key."""

        try:
            raw_header = (
                jwt.get_unverified_header(
                    access_token
                )
            )
        except (
            JWTError,
            TypeError,
            ValueError,
        ) as exception:
            raise (
                InvalidAccessTokenError
            ) from exception

        if not isinstance(
            raw_header,
            dict,
        ):
            raise InvalidAccessTokenError

        return {
            key: value
            for key, value
            in raw_header.items()
            if isinstance(
                key,
                str,
            )
        }

    def _find_signing_key(
        self,
        *,
        key_id: str,
        algorithm: str,
    ) -> Jwk:
        """Find the signing key and refresh JWKS once when necessary."""

        signing_key = (
            self._search_signing_key(
                keys=(
                    self.jwks_provider
                    .get_keys()
                ),
                key_id=key_id,
                algorithm=algorithm,
            )
        )

        if signing_key is not None:
            return signing_key

        signing_key = (
            self._search_signing_key(
                keys=(
                    self.jwks_provider
                    .get_keys(
                        force_refresh=True
                    )
                ),
                key_id=key_id,
                algorithm=algorithm,
            )
        )

        if signing_key is None:
            raise InvalidAccessTokenError

        return signing_key

    @staticmethod
    def _search_signing_key(
        *,
        keys: tuple[Jwk, ...],
        key_id: str,
        algorithm: str,
    ) -> Jwk | None:
        """Search compatible JWKS entries."""

        for key in keys:
            current_key_id = key.get(
                "kid"
            )

            current_algorithm = key.get(
                "alg"
            )

            if (
                current_key_id
                == key_id
                and (
                    current_algorithm
                    is None
                    or current_algorithm
                    == algorithm
                )
            ):
                return key

        return None

    @staticmethod
    def _required_uuid_claim(
        claims: dict[object, object],
        claim_name: str,
    ) -> uuid.UUID:
        """Read one required non-null UUID claim."""

        raw_value = claims.get(
            claim_name
        )

        if not isinstance(
            raw_value,
            str,
        ):
            raise InvalidAccessTokenError

        try:
            parsed_value = uuid.UUID(
                raw_value
            )
        except ValueError as exception:
            raise (
                InvalidAccessTokenError
            ) from exception

        if parsed_value.int == 0:
            raise InvalidAccessTokenError

        return parsed_value

    @staticmethod
    def _optional_uuid_claim(
        claims: dict[object, object],
        claim_name: str,
    ) -> uuid.UUID | None:
        """Read one optional non-null UUID claim."""

        raw_value = claims.get(
            claim_name
        )

        if raw_value is None:
            return None

        if not isinstance(
            raw_value,
            str,
        ):
            raise InvalidAccessTokenError

        try:
            parsed_value = uuid.UUID(
                raw_value
            )
        except ValueError as exception:
            raise (
                InvalidAccessTokenError
            ) from exception

        if parsed_value.int == 0:
            raise InvalidAccessTokenError

        return parsed_value


def build_supabase_jwt_verifier(
    supabase_url: str,
) -> SupabaseJwtVerifier:
    """Build one verifier from the configured Supabase URL."""

    normalized_url = (
        supabase_url
        .strip()
        .rstrip("/")
    )

    if not _is_allowed_remote_url(
        normalized_url
    ):
        raise (
            SupabaseAuthenticationConfigurationError
        )

    try:
        parsed_url = urllib.parse.urlsplit(
            normalized_url
        )
    except ValueError as exception:
        raise (
            SupabaseAuthenticationConfigurationError
        ) from exception

    if (
        parsed_url.path
        not in {
            "",
            "/",
        }
        or parsed_url.query
        or parsed_url.fragment
    ):
        raise (
            SupabaseAuthenticationConfigurationError
        )

    issuer = (
        f"{normalized_url}/auth/v1"
    )

    provider = RemoteJwksProvider(
        jwks_url=(
            f"{issuer}/"
            ".well-known/jwks.json"
        ),
    )

    return SupabaseJwtVerifier(
        issuer=issuer,
        jwks_provider=provider,
    )
