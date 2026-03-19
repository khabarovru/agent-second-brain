"""Application configuration using Pydantic Settings."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    telegram_bot_token: str = Field(description="Telegram Bot API token")
    deepgram_api_key: str = Field(description="Deepgram API key for transcription")
    todoist_api_key: str = Field(default="", description="Todoist API key for tasks")
    vault_path: Path = Field(
        default=Path("./vault"),
        description="Path to Obsidian vault directory (relative to agent-second-brain root)",
    )
    allowed_user_ids: list[int] = Field(
        default_factory=list,
        description="List of Telegram user IDs allowed to use the bot",
    )
    allow_all_users: bool = Field(
        default=False,
        description="Whether to allow access to all users (security risk!)",
    )

    @property
    def daily_path(self) -> Path:
        """Path to daily notes directory (80 Ежедневные)."""
        return self.vault_path / "80 Ежедневные"

    @property
    def weekly_path(self) -> Path:
        """Path to weekly summaries directory (85 Сводки)."""
        return self.vault_path / "85 Сводки"

    @property
    def tasks_path(self) -> Path:
        """Path to tasks directory (50 Задачи)."""
        return self.vault_path / "50 Задачи"

    @property
    def goals_path(self) -> Path:
        """Path to goals directory (60 Цели)."""
        return self.vault_path / "60 Цели"

    @property
    def attachments_path(self) -> Path:
        """Path to attachments directory."""
        return self.vault_path / "attachments"

    @property
    def thoughts_path(self) -> Path:
        """Path to thoughts directory."""
        return self.vault_path / "thoughts"

    @property
    def skills_path(self) -> Path:
        """Path to Skills directory in vault (99 _Сервис/Skills)."""
        return self.vault_path / "99 _Сервис" / "Skills"


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()
