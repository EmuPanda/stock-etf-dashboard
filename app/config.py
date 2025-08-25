import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Cache Configuration
    YAHOO_FINANCE_CACHE_TTL = int(os.getenv('YAHOO_FINANCE_CACHE_TTL', 300))  # 5 minutes
    MAX_CACHE_SIZE = int(os.getenv('MAX_CACHE_SIZE', 1000))
    CACHE_EXPIRY = int(os.getenv('CACHE_EXPIRY', 3600))  # 1 hour
    
    # API Configuration
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    IEX_CLOUD_API_KEY = os.getenv('IEX_CLOUD_API_KEY', '')
    
    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', 8501))
