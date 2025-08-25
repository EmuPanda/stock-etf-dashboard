# 📊 Stock/ETF Dashboard

A comprehensive financial dashboard for tracking stocks, ETFs, and portfolio performance with advanced analytics and risk metrics.

## 🚀 Features

### Core Features
- **Real-time Stock Data**: Pull live data from Yahoo Finance API
- **Stock Screening**: Filter by sector, market cap, P/E ratio, dividend yield
- **Portfolio Simulator**: Create and manage virtual portfolios with $10K simulation
- **Risk Analytics**: Calculate volatility, Sharpe ratio, maximum drawdown
- **S&P 500 Benchmarking**: Compare portfolio performance against market indices
- **Interactive Charts**: Professional financial visualizations with Plotly

### Advanced Features
- **Technical Indicators**: SMA, RSI, volatility calculations
- **Sector Analysis**: Market breadth and sector rotation insights
- **Portfolio Optimization**: Risk-return analysis and rebalancing suggestions
- **Historical Data**: 1-year price charts with moving averages
- **Market Overview**: Real-time major index tracking

## 🏗️ Architecture

### Backend Services (Heavy Processing)
- **StockDataService**: Handles API calls, data processing, caching
- **PortfolioService**: Portfolio management, risk calculations, simulation
- **Database Layer**: Supabase integration for data persistence

### Frontend (Clean Interface)
- **Streamlit Dashboard**: Professional UI with minimal frontend processing
- **Interactive Components**: Charts, tables, and forms
- **Responsive Design**: Mobile-friendly interface

### Security Features
- **Environment Configuration**: Secure credential management
- **API Rate Limiting**: Intelligent caching and fallback systems
- **Data Validation**: Input sanitization and error handling

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Supabase account (free tier)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd stock-etf-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Supabase**
   - Create account at [supabase.com](https://supabase.com)
   - Create new project
   - Update `config.py` with your credentials

4. **Run the dashboard**
   ```bash
   streamlit run main_dashboard.py
   ```

## 📱 Usage

### Dashboard Navigation
1. **🏠 Dashboard**: Market overview, quick stock lookup, portfolio summary
2. **📈 Stock Browser**: Stock screening and filtering tools
3. **💼 Portfolio Simulator**: Create and manage virtual portfolios
4. **📊 Market Analysis**: Sector performance and market breadth analysis

### Creating a Portfolio
1. Navigate to Portfolio Simulator
2. Enter portfolio name and initial capital
3. Add stocks by ticker symbol
4. Run performance simulation
5. Compare against S&P 500 benchmark

### Stock Screening
1. Go to Stock Browser
2. Set filtering criteria (P/E, dividend yield, sector, market cap)
3. Click "Screen Stocks"
4. Review results and add to portfolio

## 🔧 Configuration

### Environment Variables
Update `config.py` with your settings:
```python
SUPABASE_URL = "your-supabase-url"
SUPABASE_ANON_KEY = "your-supabase-key"
YAHOO_FINANCE_CACHE_TTL = 300  # 5 minutes
```

### API Settings
- **Yahoo Finance**: Primary data source (free, no API key)
- **Alpha Vantage**: Backup source (optional, requires API key)
- **IEX Cloud**: Alternative source (optional, requires API key)

## 📊 Data Sources

### Stock Information
- Current price and volume
- P/E ratio and market cap
- Dividend yield and sector
- 52-week high/low
- Technical indicators

### Historical Data
- 1-year price charts
- Moving averages (20-day, 50-day)
- RSI and volatility metrics
- Daily returns and performance

## 🚀 Deployment

### Local Development
```bash
streamlit run main_dashboard.py --server.port 8501
```

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy automatically

### Other Platforms
- **Heroku**: Add `setup.sh` and `Procfile`
- **Railway**: Direct deployment from GitHub
- **Render**: Web service deployment

## 🔒 Security Considerations

- **API Keys**: Never commit credentials to version control
- **Rate Limiting**: Built-in caching to respect API limits
- **Data Validation**: Input sanitization and error handling
- **Secure Storage**: Environment-based configuration

## 📈 Performance Features

- **Smart Caching**: 5-minute cache for stock data
- **Rate Limit Management**: Intelligent API call queuing
- **Fallback Systems**: Multiple data sources for reliability
- **Optimized Calculations**: Efficient portfolio metrics computation

## 🎯 Resume Highlights

This project demonstrates:
- **Full-stack Development**: Python backend + Streamlit frontend
- **Financial Engineering**: Risk metrics, portfolio optimization
- **API Integration**: Multiple financial data sources
- **Data Visualization**: Professional financial charts
- **Real-time Systems**: Live market data and updates
- **Security Best Practices**: Secure credential management

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Create GitHub issue
- **Documentation**: Check README and code comments
- **Community**: Streamlit and Supabase communities

## 🔮 Future Enhancements

- **Real-time Updates**: WebSocket integration for live prices
- **Advanced Analytics**: Machine learning portfolio optimization
- **Mobile App**: React Native companion app
- **Social Features**: Portfolio sharing and community
- **Backtesting**: Historical strategy performance testing

---

**Built with ❤️ using Python, Streamlit, and Supabase**
