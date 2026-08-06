"""Central configuration for the OrganizeG3 Platform API.

All environment-dependent settings must be declared and validated here.
Application modules must not read environment variables directly.
"""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from typing import Annotated, Final

from pydantic import (
    AnyHttpUrl,
    BeforeValidator,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_APP_NAME: Final[str] = "OrganizeG3 Platform API"
DEFAULT_APP_VERSION: Final[str] = "0.1.0"
DEFAULT_TIMEZONE: Final[str] = "America/Sao_Paulo"


class Environment(StrEnum):
    """Supported execution environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Supported application log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def parse_comma_separated_list(value: object) -> object:
    """Convert comma-separated environment values into lists.

    Pydantic already accepts JSON lists. This validator additionally allows:

    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
    """

    if isinstance(value, str):
        stripped_value = value.strip()

        if not stripped_value:
            return []

        if stripped_value.startswith("["):
            return value

        return [item.strip() for item in stripped_value.split(",") if item.strip()]

    return value


StringList = Annotated[
    list[str],
    BeforeValidator(parse_comma_separated_list),
]


class Settings(BaseSettings):
    """Validated runtime settings for the OrganizeG3 API.

    Settings are loaded from environment variables and, during local
    development, from the project root `.env` file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
        env_ignore_empty=True,
    )

    # -------------------------------------------------------------------------
    # APPLICATION
    # -------------------------------------------------------------------------

    app_name: str = Field(
        default=DEFAULT_APP_NAME,
        alias="APP_NAME",
        min_length=1,
        max_length=150,
    )

    app_version: str = Field(
        default=DEFAULT_APP_VERSION,
        alias="APP_VERSION",
        min_length=1,
        max_length=50,
    )

    app_environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        alias="APP_ENVIRONMENT",
    )

    app_debug: bool = Field(
        default=False,
        alias="APP_DEBUG",
    )

    app_timezone: str = Field(
        default=DEFAULT_TIMEZONE,
        alias="APP_TIMEZONE",
        min_length=1,
        max_length=100,
    )

    api_prefix: str = Field(
        default="/api/v1",
        alias="API_PREFIX",
    )

    docs_enabled: bool = Field(
        default=True,
        alias="DOCS_ENABLED",
    )

    # -------------------------------------------------------------------------
    # SERVER
    # -------------------------------------------------------------------------

    server_host: str = Field(
        default="127.0.0.1",
        alias="SERVER_HOST",
    )

    server_port: int = Field(
        default=8000,
        alias="SERVER_PORT",
        ge=1,
        le=65535,
    )

    # -------------------------------------------------------------------------
    # DATABASE
    # -------------------------------------------------------------------------

    database_url: SecretStr | None = Field(
        default=None,
        alias="DATABASE_URL",
    )

    database_echo: bool = Field(
        default=False,
        alias="DATABASE_ECHO",
    )

    database_pool_size: int = Field(
        default=5,
        alias="DATABASE_POOL_SIZE",
        ge=1,
        le=100,
    )

    database_max_overflow: int = Field(
        default=10,
        alias="DATABASE_MAX_OVERFLOW",
        ge=0,
        le=200,
    )

    database_pool_timeout_seconds: int = Field(
        default=30,
        alias="DATABASE_POOL_TIMEOUT_SECONDS",
        ge=1,
        le=300,
    )

    database_pool_recycle_seconds: int = Field(
        default=1800,
        alias="DATABASE_POOL_RECYCLE_SECONDS",
        ge=60,
    )

    # -------------------------------------------------------------------------
    # SUPABASE
    # -------------------------------------------------------------------------

    supabase_url: AnyHttpUrl | None = Field(
        default=None,
        alias="SUPABASE_URL",
    )

    supabase_anon_key: SecretStr | None = Field(
        default=None,
        alias="SUPABASE_ANON_KEY",
    )

    supabase_service_role_key: SecretStr | None = Field(
        default=None,
        alias="SUPABASE_SERVICE_ROLE_KEY",
    )

    supabase_jwt_secret: SecretStr | None = Field(
        default=None,
        alias="SUPABASE_JWT_SECRET",
    )

    supabase_storage_bucket: str = Field(
        default="organizeg3-documents",
        alias="SUPABASE_STORAGE_BUCKET",
        min_length=1,
        max_length=100,
    )

    # -------------------------------------------------------------------------
    # AUTHENTICATION
    # -------------------------------------------------------------------------

    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
    )

    access_token_expire_minutes: int = Field(
        default=60,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
        ge=5,
        le=1440,
    )

    refresh_token_expire_days: int = Field(
        default=30,
        alias="REFRESH_TOKEN_EXPIRE_DAYS",
        ge=1,
        le=365,
    )

    # -------------------------------------------------------------------------
    # CORS
    # -------------------------------------------------------------------------

    cors_allowed_origins: StringList = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ALLOWED_ORIGINS",
    )

    cors_allow_credentials: bool = Field(
        default=True,
        alias="CORS_ALLOW_CREDENTIALS",
    )

    cors_allowed_methods: StringList = Field(
        default_factory=lambda: [
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
        ],
        alias="CORS_ALLOWED_METHODS",
    )

    cors_allowed_headers: StringList = Field(
        default_factory=lambda: [
            "Authorization",
            "Content-Type",
            "Idempotency-Key",
            "X-Correlation-ID",
            "X-Device-ID",
            "X-Tenant-ID",
        ],
        alias="CORS_ALLOWED_HEADERS",
    )

    # -------------------------------------------------------------------------
    # LOGGING
    # -------------------------------------------------------------------------

    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        alias="LOG_LEVEL",
    )

    log_json: bool = Field(
        default=False,
        alias="LOG_JSON",
    )

    log_include_source: bool = Field(
        default=True,
        alias="LOG_INCLUDE_SOURCE",
    )

    # -------------------------------------------------------------------------
    # STORAGE AND UPLOADS
    # -------------------------------------------------------------------------

    maximum_upload_size_mb: int = Field(
        default=25,
        alias="MAXIMUM_UPLOAD_SIZE_MB",
        ge=1,
        le=500,
    )

    allowed_upload_extensions: StringList = Field(
        default_factory=lambda: [
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".docx",
            ".xlsx",
            ".csv",
            ".txt",
            ".md",
        ],
        alias="ALLOWED_UPLOAD_EXTENSIONS",
    )

    blocked_upload_extensions: StringList = Field(
        default_factory=lambda: [
            ".skp",
            ".dwg",
            ".dxf",
            ".rvt",
            ".exe",
            ".msi",
            ".bat",
            ".cmd",
            ".ps1",
        ],
        alias="BLOCKED_UPLOAD_EXTENSIONS",
    )

    # -------------------------------------------------------------------------
    # FEATURES
    # -------------------------------------------------------------------------

    feature_ai_enabled: bool = Field(
        default=False,
        alias="FEATURE_AI_ENABLED",
    )

    feature_realtime_enabled: bool = Field(
        default=True,
        alias="FEATURE_REALTIME_ENABLED",
    )

    feature_offline_sync_enabled: bool = Field(
        default=True,
        alias="FEATURE_OFFLINE_SYNC_ENABLED",
    )

    feature_push_notifications_enabled: bool = Field(
        default=False,
        alias="FEATURE_PUSH_NOTIFICATIONS_ENABLED",
    )

    # -------------------------------------------------------------------------
    # VALIDATION
    # -------------------------------------------------------------------------

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        """Normalize and validate the API route prefix."""

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("API_PREFIX não pode estar vazio.")

        if not normalized_value.startswith("/"):
            normalized_value = f"/{normalized_value}"

        if normalized_value != "/":
            normalized_value = normalized_value.rstrip("/")

        return normalized_value

    @field_validator("allowed_upload_extensions", "blocked_upload_extensions")
    @classmethod
    def normalize_extensions(cls, values: list[str]) -> list[str]:
        """Normalize file extensions to lowercase values beginning with a dot."""

        normalized_extensions: list[str] = []

        for extension in values:
            normalized_extension = extension.strip().lower()

            if not normalized_extension:
                continue

            if not normalized_extension.startswith("."):
                normalized_extension = f".{normalized_extension}"

            if normalized_extension not in normalized_extensions:
                normalized_extensions.append(normalized_extension)

        return normalized_extensions

    @field_validator("cors_allowed_origins")
    @classmethod
    def normalize_cors_origins(cls, values: list[str]) -> list[str]:
        """Remove duplicate and empty CORS origins."""

        normalized_origins: list[str] = []

        for origin in values:
            normalized_origin = origin.strip().rstrip("/")

            if normalized_origin and normalized_origin not in normalized_origins:
                normalized_origins.append(normalized_origin)

        return normalized_origins

    @model_validator(mode="after")
    def validate_environment_requirements(self) -> Settings:
        """Apply stricter requirements outside local development."""

        if self.is_production:
            missing_settings: list[str] = []

            if self.database_url is None:
                missing_settings.append("DATABASE_URL")

            if self.supabase_url is None:
                missing_settings.append("SUPABASE_URL")

            if self.supabase_service_role_key is None:
                missing_settings.append("SUPABASE_SERVICE_ROLE_KEY")

            if self.supabase_jwt_secret is None:
                missing_settings.append("SUPABASE_JWT_SECRET")

            if missing_settings:
                joined_settings = ", ".join(missing_settings)

                raise ValueError(
                    f"Configurações obrigatórias ausentes para produção: {joined_settings}."
                )

            if self.app_debug:
                raise ValueError("APP_DEBUG não pode estar ativado em produção.")

            if "*" in self.cors_allowed_origins:
                raise ValueError("CORS_ALLOWED_ORIGINS não pode conter '*' em produção.")

        overlap = set(self.allowed_upload_extensions).intersection(self.blocked_upload_extensions)

        if overlap:
            conflicting_extensions = ", ".join(sorted(overlap))

            raise ValueError(
                "Extensões não podem estar simultaneamente permitidas "
                f"e bloqueadas: {conflicting_extensions}."
            )

        return self

    # -------------------------------------------------------------------------
    # COMPUTED PROPERTIES
    # -------------------------------------------------------------------------

    @property
    def is_development(self) -> bool:
        """Return whether the current environment is development."""

        return self.app_environment is Environment.DEVELOPMENT

    @property
    def is_test(self) -> bool:
        """Return whether the current environment is test."""

        return self.app_environment is Environment.TEST

    @property
    def is_staging(self) -> bool:
        """Return whether the current environment is staging."""

        return self.app_environment is Environment.STAGING

    @property
    def is_production(self) -> bool:
        """Return whether the current environment is production."""

        return self.app_environment is Environment.PRODUCTION

    @property
    def effective_docs_url(self) -> str | None:
        """Return the Swagger documentation URL for the current environment."""

        return "/docs" if self.docs_enabled else None

    @property
    def effective_redoc_url(self) -> str | None:
        """Return the ReDoc documentation URL for the current environment."""

        return "/redoc" if self.docs_enabled else None

    @property
    def maximum_upload_size_bytes(self) -> int:
        """Return the upload size limit converted to bytes."""

        return self.maximum_upload_size_mb * 1024 * 1024

    def require_database_url(self) -> str:
        """Return the database URL or fail with a clear configuration error."""

        if self.database_url is None:
            raise RuntimeError("DATABASE_URL não foi configurada para este ambiente.")

        return self.database_url.get_secret_value()

    def require_supabase_service_role_key(self) -> str:
        """Return the Supabase service key or fail clearly."""

        if self.supabase_service_role_key is None:
            raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY não foi configurada.")

        return self.supabase_service_role_key.get_secret_value()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached validated application settings."""

    return Settings()
