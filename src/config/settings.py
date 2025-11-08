"""Application configuration settings."""
import os


class Config:
    """Application configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'black-sultan-secret-key-2024')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///database/app.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PayPal Configuration
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', 'demo_client_id')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', 'demo_client_secret')
    PAYPAL_BASE_URL = os.environ.get(
        'PAYPAL_BASE_URL',
        'https://api.sandbox.paypal.com'
    )
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # CORS Configuration
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '*')
    
    # Cache Configuration
    CACHE_DURATION = 30  # seconds
    
    # Trading Bot Configuration
    BOT_UPDATE_INTERVAL = 30  # seconds
    DAILY_RESET_CHECK_INTERVAL = 60  # seconds
