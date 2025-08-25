import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from data_service import StockDataService
import json

class PortfolioService:
    """Service for portfolio management and simulation"""
    
    def __init__(self):
        self.data_service = StockDataService()
        self.portfolios = {}  # In-memory storage for demo
    
    def create_portfolio(self, name: str, initial_capital: float = 10000) -> str:
        """Create a new portfolio"""
        portfolio_id = f"portfolio_{len(self.portfolios) + 1}"
        
        self.portfolios[portfolio_id] = {
            'id': portfolio_id,
            'name': name,
            'initial_capital': initial_capital,
            'current_capital': initial_capital,
            'holdings': [],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        return portfolio_id
    
    def add_holding(self, portfolio_id: str, ticker: str, shares: float, 
                    purchase_price: Optional[float] = None) -> bool:
        """Add a holding to a portfolio"""
        if portfolio_id not in self.portfolios:
            return False
        
        # Get current stock data
        stock_data = self.data_service.get_stock_data(ticker)
        if not stock_data or stock_data['current_price'] == 0:
            return False
        
        current_price = stock_data['current_price']
        purchase_price = purchase_price or current_price
        
        # Calculate holding value
        holding_value = shares * current_price
        
        # Check if we have enough capital
        portfolio = self.portfolios[portfolio_id]
        if holding_value > portfolio['current_capital']:
            return False
        
        # Add holding
        holding = {
            'ticker': ticker,
            'shares': shares,
            'purchase_price': purchase_price,
            'current_price': current_price,
            'value': holding_value,
            'unrealized_pnl': (current_price - purchase_price) * shares,
            'unrealized_pnl_percent': ((current_price - purchase_price) / purchase_price) * 100,
            'added_at': datetime.now().isoformat()
        }
        
        portfolio['holdings'].append(holding)
        portfolio['current_capital'] -= holding_value
        portfolio['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def remove_holding(self, portfolio_id: str, ticker: str) -> bool:
        """Remove a holding from a portfolio"""
        if portfolio_id not in self.portfolios:
            return False
        
        portfolio = self.portfolios[portfolio_id]
        
        # Find and remove holding
        for i, holding in enumerate(portfolio['holdings']):
            if holding['ticker'] == ticker:
                # Return capital
                portfolio['current_capital'] += holding['value']
                portfolio['holdings'].pop(i)
                portfolio['last_updated'] = datetime.now().isoformat()
                return True
        
        return False
    
    def update_portfolio_values(self, portfolio_id: str) -> bool:
        """Update all holding values with current prices"""
        if portfolio_id not in self.portfolios:
            return False
        
        portfolio = self.portfolios[portfolio_id]
        total_value = portfolio['current_capital']
        
        for holding in portfolio['holdings']:
            # Get current price
            stock_data = self.data_service.get_stock_data(holding['ticker'])
            if stock_data and stock_data['current_price'] > 0:
                current_price = stock_data['current_price']
                holding['current_price'] = current_price
                holding['value'] = holding['shares'] * current_price
                holding['unrealized_pnl'] = (current_price - holding['purchase_price']) * holding['shares']
                holding['unrealized_pnl_percent'] = ((current_price - holding['purchase_price']) / holding['purchase_price']) * 100
            
            total_value += holding['value']
        
        portfolio['total_value'] = total_value
        portfolio['total_return'] = ((total_value - portfolio['initial_capital']) / portfolio['initial_capital']) * 100
        portfolio['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def get_portfolio_summary(self, portfolio_id: str) -> Dict:
        """Get portfolio summary with metrics"""
        if portfolio_id not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_id]
        
        # Update values first
        self.update_portfolio_values(portfolio_id)
        
        # Calculate metrics
        total_value = portfolio.get('total_value', portfolio['initial_capital'])
        total_return = portfolio.get('total_return', 0)
        
        # Calculate sector allocation
        sector_allocation = {}
        for holding in portfolio['holdings']:
            stock_data = self.data_service.get_stock_data(holding['ticker'])
            sector = stock_data.get('sector', 'Unknown')
            sector_allocation[sector] = sector_allocation.get(sector, 0) + holding['value']
        
        # Calculate portfolio risk metrics
        risk_metrics = self.data_service.calculate_portfolio_metrics(portfolio['holdings'])
        
        return {
            'id': portfolio_id,
            'name': portfolio['name'],
            'initial_capital': portfolio['initial_capital'],
            'total_value': total_value,
            'current_capital': portfolio['current_capital'],
            'total_return': total_return,
            'holdings_count': len(portfolio['holdings']),
            'sector_allocation': sector_allocation,
            'risk_metrics': risk_metrics,
            'last_updated': portfolio['last_updated']
        }
    
    def simulate_portfolio(self, portfolio_id: str, months: int = 12) -> Dict:
        """Simulate portfolio performance over time"""
        if portfolio_id not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_id]
        
        # Get historical data for all holdings
        simulation_data = {}
        start_date = datetime.now() - timedelta(days=months * 30)
        
        for holding in portfolio['holdings']:
            hist = self.data_service.get_historical_data(holding['ticker'], f"{months}m")
            if not hist.empty:
                # Filter to simulation period
                hist = hist[hist.index >= start_date]
                if not hist.empty:
                    simulation_data[holding['ticker']] = hist['Close']
        
        if not simulation_data:
            return {}
        
        # Create portfolio simulation
        portfolio_df = pd.DataFrame(simulation_data)
        
        # Calculate daily returns
        returns = portfolio_df.pct_change().fillna(0)
        
        # Apply portfolio weights
        weights = [holding['value'] / sum(h['value'] for h in portfolio['holdings']) 
                  for holding in portfolio['holdings']]
        
        portfolio_returns = (returns * weights).sum(axis=1)
        
        # Calculate cumulative returns
        cumulative_returns = (1 + portfolio_returns).cumprod()
        
        # Calculate metrics
        total_return = (cumulative_returns.iloc[-1] - 1) * 100
        volatility = portfolio_returns.std() * np.sqrt(252) * 100
        sharpe_ratio = (portfolio_returns.mean() * 252) / portfolio_returns.std() if portfolio_returns.std() > 0 else 0
        
        # Calculate drawdown
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        return {
            'total_return': total_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'cumulative_returns': cumulative_returns.tolist(),
            'dates': cumulative_returns.index.strftime('%Y-%m-%d').tolist(),
            'simulation_period': f"{months} months"
        }
    
    def compare_with_sp500(self, portfolio_id: str) -> Dict:
        """Compare portfolio performance with S&P 500"""
        portfolio_sim = self.simulate_portfolio(portfolio_id)
        if not portfolio_sim:
            return {}
        
        # Get S&P 500 data
        sp500_hist = self.data_service.get_historical_data('^GSPC', '1y')
        if sp500_hist.empty:
            return {}
        
        # Calculate S&P 500 returns
        sp500_returns = sp500_hist['Close'].pct_change().fillna(0)
        sp500_cumulative = (1 + sp500_returns).cumprod()
        
        sp500_total_return = (sp500_cumulative.iloc[-1] - 1) * 100
        sp500_volatility = sp500_returns.std() * np.sqrt(252) * 100
        
        return {
            'portfolio': {
                'total_return': portfolio_sim['total_return'],
                'volatility': portfolio_sim['volatility'],
                'sharpe_ratio': portfolio_sim['sharpe_ratio']
            },
            'sp500': {
                'total_return': sp500_total_return,
                'volatility': sp500_volatility,
                'sharpe_ratio': (sp500_returns.mean() * 252) / sp500_returns.std() if sp500_returns.std() > 0 else 0
            },
            'outperformance': portfolio_sim['total_return'] - sp500_total_return,
            'risk_adjusted_outperformance': portfolio_sim['sharpe_ratio'] - ((sp500_returns.mean() * 252) / sp500_returns.std() if sp500_returns.std() > 0 else 0)
        }
    
    def get_all_portfolios(self) -> List[Dict]:
        """Get list of all portfolios"""
        return [self.get_portfolio_summary(pid) for pid in self.portfolios.keys()]
    
    def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete a portfolio"""
        if portfolio_id in self.portfolios:
            del self.portfolios[portfolio_id]
            return True
        return False
