import os
from typing import Optional

class Config:
    """Configuration class for the Stock/ETF Dashboard"""
    
    # Supabase Configuration
    SUPABASE_URL = "https://bsbsrgxswpvpqnnnsjte.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJzYnNyZ3hzd3B2cHFubm5zanRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYwMDU0OTQsImV4cCI6MjA3MTU4MTQ5NH0.YbNlNGAEprgkSDqIE8DtlJ6Js599-HBZN88dhmo3l4s"
    
    # API Configuration
    YAHOO_FINANCE_CACHE_TTL = 300  # 5 minutes
    ALPHA_VANTAGE_API_KEY = ""
    IEX_CLOUD_API_KEY = ""
    
    # Application Settings
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 8501
    
    # Database Configuration
    MAX_CACHE_SIZE = 1000
    CACHE_EXPIRY = 3600  # 1 hour
    
    @classmethod
    def get_supabase_url(cls) -> str:
        return cls.SUPABASE_URL
    
    @classmethod
    def get_supabase_key(cls) -> str:
        return cls.SUPABASE_ANON_KEY
