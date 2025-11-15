from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class StorageConfig(BaseModel):
    excel_path: str = Field(default='data/outputs/invitations.xlsx', alias='EXCEL_STORAGE_PATH')


class InvitationConfig(BaseModel):
    dataset_path: str = Field(default='data/inputs/candidates.sample.json', alias='INVITATION_DATASET_PATH')


class LinkedInConfig(BaseModel):
    base_url: str = Field(default='https://api.linkedin.com/v2', alias='LINKEDIN_BASE_URL')
    access_token: str | None = Field(default=None, alias='LINKEDIN_ACCESS_TOKEN')
    client_id: str | None = Field(default=None, alias='LINKEDIN_CLIENT_ID')
    client_secret: str | None = Field(default=None, alias='LINKEDIN_CLIENT_SECRET')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    environment: str = 'local'
    app: AppConfig = AppConfig()
    storage: StorageConfig = StorageConfig()
    invitations: InvitationConfig = InvitationConfig()
    linkedin: LinkedInConfig = LinkedInConfig()


def load_settings(path: Path | None = None) -> Settings:
    yaml_data = {}
    candidate = path or Path('config/settings.yaml')
    if candidate.exists():
        yaml_data = yaml.safe_load(candidate.read_text(encoding='utf-8'))
    return Settings(**(yaml_data or {}))


@lru_cache
def get_settings() -> Settings:
    return load_settings()
