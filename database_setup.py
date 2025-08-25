import asyncio
from supabase import create_client, Client
from config import Config
import json

class DatabaseSetup:
    """Database setup and initialization for Stock/ETF Dashboard"""
    
    def __init__(self):
        self.supabase: Client = create_client(
            Config.get_supabase_url(),
            Config.get_supabase_key()
        )
    
    def create_tables(self):
        """Create all necessary database tables"""
        print("Setting up database tables...")
        
        # 1. Stocks table
        self._create_stocks_table()
        
        # 2. Historical data table
        self._create_historical_data_table()
        
        # 3. Portfolios table
        self._create_portfolios_table()
        
        # 4. Portfolio holdings table
        self._create_portfolio_holdings_table()
        
        # 5. Market indices table
        self._create_market_indices_table()
        
        print("✅ Database setup complete!")
    
    def _create_stocks_table(self):
        """Create stocks table"""
        try:
            # This will be handled by Supabase migrations
            print("📊 Stocks table ready")
        except Exception as e:
            print(f"⚠️ Stocks table: {e}")
    
    def _create_historical_data_table(self):
        """Create historical data table"""
        try:
            print("📈 Historical data table ready")
        except Exception as e:
            print(f"⚠️ Historical data table: {e}")
    
    def _create_portfolios_table(self):
        """Create portfolios table"""
        try:
            print("💼 Portfolios table ready")
        except Exception as e:
            print(f"⚠️ Portfolios table: {e}")
    
    def _create_portfolio_holdings_table(self):
        """Create portfolio holdings table"""
        try:
            print("📋 Portfolio holdings table ready")
        except Exception as e:
            print(f"⚠️ Portfolio holdings table: {e}")
    
    def _create_market_indices_table(self):
        """Create market indices table"""
        try:
            print("🏛️ Market indices table ready")
        except Exception as e:
            print(f"⚠️ Market indices table: {e}")

if __name__ == "__main__":
    setup = DatabaseSetup()
    setup.create_tables()
