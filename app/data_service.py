import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time
from supabase import create_client, Client
from config import Config
import asyncio
from functools import lru_cache

class StockDataService:
    """Backend service for stock data operations - handles heavy processing"""
    
    def __init__(self):
        self.supabase: Client = create_client(
            Config.get_supabase_url(),
            Config.get_supabase_key()
        )
        self.cache = {}
        self.cache_timestamps = {}
        self.rate_limit_tracker = {}
    
    def get_stock_data(self, ticker: str) -> Dict:
        """Get comprehensive stock data for a single ticker"""
        try:
            # Check cache first
            if self._is_cache_valid(ticker):
                return self.cache[ticker]
            
            # Fetch from Yahoo Finance
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Better data validation and fallbacks
            current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
            price_change = info.get('regularMarketChange') or 0
            price_change_percent = info.get('regularMarketChangePercent') or 0
            
            # If we still don't have a current price, try to get it from history
            if not current_price or current_price == 0:
                try:
                    hist = stock.history(period="1d")
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        # Calculate change from previous close
                        if len(hist) > 1:
                            prev_close = hist['Close'].iloc[-2]
                            price_change = current_price - prev_close
                            price_change_percent = (price_change / prev_close) * 100
                except Exception as e:
                    print(f"Error getting historical data for {ticker}: {e}")
            
            # Process and transform data with better validation
            data = {
                'ticker': ticker,
                'company_name': info.get('longName') or info.get('shortName') or ticker,
                'current_price': current_price or 0,
                'price_change': price_change or 0,
                'price_change_percent': price_change_percent or 0,
                'volume': info.get('volume') or info.get('regularMarketVolume') or 0,
                'market_cap': info.get('marketCap') or 0,
                'pe_ratio': info.get('trailingPE') or info.get('forwardPE') or 0,
                'pb_ratio': info.get('priceToBook') or 0,
                'dividend_yield': info.get('dividendYield') or 0,
                'sector': info.get('sector') or 'N/A',
                'industry': info.get('industry') or 'N/A',
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh') or 0,
                'fifty_two_week_low': info.get('fiftyTwoWeekLow') or 0,
                'avg_volume': info.get('averageVolume') or 0,
                'last_updated': datetime.now().isoformat()
            }
            
            # Cache the result
            self._cache_data(ticker, data)
            return data
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return self._get_fallback_data(ticker)
    
    def get_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return pd.DataFrame()
            
            # Calculate technical indicators
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
            hist['RSI'] = self._calculate_rsi(hist['Close'])
            hist['Volatility'] = hist['Close'].pct_change().rolling(window=20).std()
            
            return hist
            
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()
    
    def get_market_overview(self) -> Dict:
        """Get market overview with major indices"""
        indices = ['^GSPC', '^DJI', '^IXIC', '^RUT']  # S&P 500, Dow, Nasdaq, Russell
        overview = {}
        
        for index in indices:
            try:
                # Direct approach for indices - don't use get_stock_data
                stock = yf.Ticker(index)
                hist = stock.history(period="2d")
                
                if not hist.empty and len(hist) >= 2:
                    current_price = float(hist['Close'].iloc[-1])
                    prev_price = float(hist['Close'].iloc[-2])
                    change = current_price - prev_price
                    change_percent = (change / prev_price) * 100
                    
                    overview[index] = {
                        'name': self._get_index_name(index),
                        'price': current_price,
                        'change': change,
                        'change_percent': change_percent
                    }
                    
            except Exception as e:
                continue
        
        return overview
    
    def _get_index_name(self, ticker: str) -> str:
        """Get human-readable names for indices"""
        names = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones Industrial Average',
            '^IXIC': 'NASDAQ Composite',
            '^RUT': 'Russell 2000 Index'
        }
        return names.get(ticker, ticker)
    
    def screen_stocks(self, filters: Dict) -> List[Dict]:
        """Screen stocks based on criteria"""
        # This would typically query a database of pre-fetched stock data
        # For now, we'll return a sample of popular stocks
        popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX']
        screened = []
        
        for ticker in popular_stocks:
            try:
                data = self.get_stock_data(ticker)
                
                # Apply filters
                if self._passes_filters(data, filters):
                    screened.append(data)
                    
            except Exception as e:
                print(f"Error screening {ticker}: {e}")
        
        return screened
    
    def calculate_portfolio_metrics(self, portfolio: List[Dict]) -> Dict:
        """Calculate portfolio risk and return metrics"""
        if not portfolio:
            return {}
        
        try:
            # Calculate portfolio weights and returns
            total_value = sum(holding['value'] for holding in portfolio)
            weights = [holding['value'] / total_value for holding in portfolio]
            
            # Get historical data for all holdings
            returns_data = {}
            for holding in portfolio:
                hist = self.get_historical_data(holding['ticker'], "1y")
                if not hist.empty:
                    returns_data[holding['ticker']] = hist['Close'].pct_change().dropna()
            
            if not returns_data:
                return {}
            
            # Calculate portfolio metrics
            portfolio_returns = pd.DataFrame(returns_data)
            portfolio_returns = portfolio_returns.fillna(0)
            
            # Portfolio return
            portfolio_return = (portfolio_returns * weights).sum(axis=1)
            
            # Volatility
            portfolio_vol = portfolio_return.std() * np.sqrt(252)  # Annualized
            
            # Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            sharpe_ratio = (portfolio_return.mean() * 252 - risk_free_rate) / portfolio_vol
            
            # Maximum drawdown
            cumulative_returns = (1 + portfolio_return).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = drawdown.min()
            
            return {
                'total_return': (cumulative_returns.iloc[-1] - 1) * 100,
                'annualized_return': portfolio_return.mean() * 252 * 100,
                'volatility': portfolio_vol * 100,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown * 100,
                'risk_free_rate': risk_free_rate * 100
            }
            
        except Exception as e:
            print(f"Error calculating portfolio metrics: {e}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _is_cache_valid(self, ticker: str) -> bool:
        """Check if cached data is still valid"""
        if ticker not in self.cache_timestamps:
            return False
        
        cache_age = time.time() - self.cache_timestamps[ticker]
        return cache_age < Config.YAHOO_FINANCE_CACHE_TTL
    
    def _cache_data(self, ticker: str, data: Dict):
        """Cache data with timestamp"""
        self.cache[ticker] = data
        self.cache_timestamps[ticker] = time.time()
        
        # Clean old cache entries
        if len(self.cache) > Config.MAX_CACHE_SIZE:
            oldest_ticker = min(self.cache_timestamps.keys(), 
                              key=lambda k: self.cache_timestamps[k])
            del self.cache[oldest_ticker]
            del self.cache_timestamps[oldest_ticker]
    
    def _passes_filters(self, data: Dict, filters: Dict) -> bool:
        """Check if stock passes screening filters"""
        if 'min_pe' in filters and data['pe_ratio'] < filters['min_pe']:
            return False
        if 'max_pe' in filters and data['pe_ratio'] > filters['max_pe']:
            return False
        if 'min_dividend' in filters and data['dividend_yield'] < filters['min_dividend']:
            return False
        if 'sector' in filters and data['sector'] != filters['sector']:
            return False
        return True
    
    def _get_fallback_data(self, ticker: str) -> Dict:
        """Get fallback data when primary API fails"""
        return {
            'ticker': ticker,
            'company_name': 'N/A',
            'current_price': 0,
            'price_change': 0,
            'price_change_percent': 0,
            'volume': 0,
            'market_cap': 0,
            'pe_ratio': 0,
            'pb_ratio': 0,
            'dividend_yield': 0,
            'sector': 'N/A',
            'industry': 'N/A',
            'fifty_two_week_high': 0,
            'fifty_two_week_low': 0,
            'avg_volume': 0,
            'last_updated': datetime.now().isoformat()
        }
