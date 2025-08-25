import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Stock/ETF Dashboard"""
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
    
    # API Configuration
    YAHOO_FINANCE_CACHE_TTL = int(os.getenv('YAHOO_FINANCE_CACHE_TTL', 300))  # 5 minutes
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    IEX_CLOUD_API_KEY = os.getenv('IEX_CLOUD_API_KEY', '')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8501))
    
    # Database Configuration
    MAX_CACHE_SIZE = int(os.getenv('MAX_CACHE_SIZE', 1000))
    CACHE_EXPIRY = int(os.getenv('CACHE_EXPIRY', 3600))  # 1 hour
    
    @classmethod
    def get_supabase_url(cls) -> str:
        return cls.SUPABASE_URL
    
    @classmethod
    def get_supabase_key(cls) -> str:
        return cls.SUPABASE_ANON_KEY
