"""
Configuration module for PDF Analyzer
"""

import os
from pathlib import Path
from typing import Dict, Any

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, UPLOADS_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Application settings
APP_CONFIG = {
    "name": "PDF Analyzer",
    "version": "1.0.0",
    "debug": os.getenv("DEBUG_MODE", "false").lower() == "true"
}

# File processing limits
FILE_CONFIG = {
    "max_file_size_mb": int(os.getenv("MAX_FILE_SIZE_MB", "50")),
    "max_pages": int(os.getenv("MAX_PAGES", "100")),
    "allowed_extensions": [".pdf"],
    "upload_dir": UPLOADS_DIR,
    "output_dir": OUTPUT_DIR
}

# Feature flags
FEATURES = {
    "ai_chat": os.getenv("ENABLE_AI_FEATURES", "false").lower() == "true",
    "advanced_analysis": os.getenv("ENABLE_ADVANCED_ANALYSIS", "true").lower() == "true",
    "export_functions": os.getenv("ENABLE_EXPORT", "true").lower() == "true",
    "semantic_search": os.getenv("ENABLE_SEMANTIC_SEARCH", "false").lower() == "true"
}

# Streamlit configuration
STREAMLIT_CONFIG = {
    "port": int(os.getenv("STREAMLIT_SERVER_PORT", "8504")),
    "host": os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost"),
    "page_title": "🧠 PDF Elemző és Chat",
    "page_icon": "🧠",
    "layout": "wide"
}

# AI Configuration (optional)
AI_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "model_name": os.getenv("AI_MODEL_NAME", "gpt-3.5-turbo"),
    "max_tokens": int(os.getenv("AI_MAX_TOKENS", "1000")),
    "temperature": float(os.getenv("AI_TEMPERATURE", "0.7"))
}

# Logging configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "file": LOGS_DIR / "app.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

def get_config() -> Dict[str, Any]:
    """Get complete configuration"""
    return {
        "app": APP_CONFIG,
        "files": FILE_CONFIG,
        "features": FEATURES,
        "streamlit": STREAMLIT_CONFIG,
        "ai": AI_CONFIG,
        "logging": LOGGING_CONFIG,
        "directories": {
            "base": BASE_DIR,
            "data": DATA_DIR,
            "uploads": UPLOADS_DIR,
            "output": OUTPUT_DIR,
            "logs": LOGS_DIR
        }
    }

def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURES.get(feature_name, False)

def get_upload_path(filename: str) -> Path:
    """Get full path for uploaded file"""
    return UPLOADS_DIR / filename

def get_output_path(filename: str) -> Path:
    """Get full path for output file"""
    return OUTPUT_DIR / filename 