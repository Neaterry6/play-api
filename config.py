import os

class Config:
    """Base configuration settings"""
    SECRET_KEY = os.getenv("SESSION_SECRET", "default-secret-key")  # Security key for session handling
    DEBUG = os.getenv("DEBUG", True)  # Enable debugging mode

    # 🔗 PostgreSQL Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///streamme.db")  # Default to SQLite if missing
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Improve performance

    # 📜 Lyrics API Configuration
    LYRICS_API_URL = "https://api.lyrics.ovh/v1/{artist}/{song}"  # Default Lyrics API

    # 🔗 YouTube Netscape Cookies Path
    COOKIES_PATH = os.getenv("COOKIES_PATH", "cookies.txt")

class ProductionConfig(Config):
    """Production settings for deploying with PostgreSQL"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_gX98vslEYZNe@ep-tiny-rain-a50izhgg.us-east-2.aws.neon.tech/neondb?sslmode=require")

class DevelopmentConfig(Config):
    """Development settings"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///streamme.db")

class TestingConfig(Config):
    """Testing settings"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db
