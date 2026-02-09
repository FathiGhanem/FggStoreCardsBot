"""Application settings and configuration."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Bot configuration
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    AUTHORIZED_USER_ID: Optional[int] = (
        int(os.getenv("AUTHORIZED_USER_ID")) if os.getenv("AUTHORIZED_USER_ID") else None
    )

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    ASSETS_DIR: Path = BASE_DIR / "assets"
    FONTS_DIR: Path = ASSETS_DIR / "fonts"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    TEMP_DIR: Path = BASE_DIR / "temp"

    # Font settings
    FONT_NAME: str = "tahoma.ttf"
    FONT_PATH: Path = FONTS_DIR / FONT_NAME
    BASE_FONT_SIZE: int = int(40 * 3.125)
    SMALL_FONT_SIZE: int = int(16 * 3.125)
    CODE_MAX_FONT_SIZE: int = int(60 * 3.125)
    CODE_MIN_FONT_SIZE: int = int(10 * 3.125)

    # Image settings
    TEMPLATE_IMAGE: str = "card.png"
    TEMPLATE_PATH: Path = TEMPLATES_DIR / TEMPLATE_IMAGE
    SCALE_FACTOR: float = 3.125

    # Timezone offset (UTC+3 for Saudi Arabia)
    TIMEZONE_OFFSET_HOURS: int = 3

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def validate(cls) -> None:
        """Validate required settings."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        if cls.AUTHORIZED_USER_ID is None:
            raise ValueError("AUTHORIZED_USER_ID environment variable is required")
        if not cls.TEMPLATE_PATH.exists():
            raise FileNotFoundError(f"Template image not found: {cls.TEMPLATE_PATH}")
        if not cls.FONT_PATH.exists():
            raise FileNotFoundError(f"Font file not found: {cls.FONT_PATH}")

    @classmethod
    def setup_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.TEMP_DIR.mkdir(exist_ok=True, parents=True)


# Create a singleton instance
settings = Settings()
