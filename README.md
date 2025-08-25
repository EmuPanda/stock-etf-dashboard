# 📈 Stock/ETF Dashboard

A professional, real-time financial dashboard built with Python and Streamlit, featuring live market data, portfolio analysis, and market insights.

## 🚀 **Live Demo**

**Your dashboard is running at: http://localhost:8501**

## ✨ **Features**

### 🏠 **Dashboard**
- **Real-time market overview** (S&P 500, NASDAQ)
- **Top market movers** (69 carefully selected stocks)
- **Quick stock lookup** with detailed analytics
- **Market breadth indicators**

### 🔍 **Stock Browser**
- **Advanced stock screening** by P/E, dividends, market cap
- **Sector-based filtering**
- **Export results to CSV**
- **Real-time data from Yahoo Finance**

### 💼 **Portfolio Simulator**
- **Create investment scenarios** with any stocks
- **Historical performance analysis** (6m, 1y, 2y, 5y)
- **Risk metrics**: Sharpe ratio, beta, correlation, max drawdown
- **S&P 500 benchmark comparison**
- **Export analysis reports**

### 📊 **Market Analysis**
- **Sector performance analysis** across 5 major sectors
- **Market breadth indicators** (advancing vs declining stocks)
- **Market sentiment interpretation**
- **Top movers tracking**

## 🏗️ **Project Structure**

```
stock etf dashboard/
├── .env                 # 🔒 Environment variables (not in git)
├── .env.example         # 📋 Template for environment setup
├── config.py            # ⚙️ Configuration management
├── data_service.py      # 📊 Stock data service (Yahoo Finance)
├── portfolio_service.py # 💼 Portfolio management & analysis
├── requirements.txt     # 📦 Python dependencies
├── README.md            # 📖 This file
└── app/                 # 🆕 Modular dashboard application
    ├── main.py          # 🚀 Main entry point with navigation
    ├── pages/           # 📱 Individual dashboard pages
    │   ├── dashboard.py     # Main dashboard view
    │   ├── stock_browser.py # Stock screening
    │   ├── portfolio.py     # Portfolio simulation
    │   └── market_analysis.py # Market insights
    ├── utils/           # ✨ Utilities & styling
    │   └── styles.py        # Custom CSS
    └── requirements.txt # 📦 App-specific dependencies
```

## 🚀 **Quick Start**

### 1. **Clone & Setup**
```bash
git clone <your-repo-url>
cd stock-etf-dashboard
```

### 2. **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run Dashboard**
```bash
cd app
python3 -m streamlit run main.py --server.port 8501
```

**Access at: http://localhost:8501**

## ⚙️ **Configuration**

### **Required Environment Variables**
```bash
# Supabase (for portfolio storage)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key

# Optional API Keys (for backup data sources)
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
IEX_CLOUD_API_KEY=your-iex-cloud-key

# Cache Settings
YAHOO_FINANCE_CACHE_TTL=300  # 5 minutes
MAX_CACHE_SIZE=1000
CACHE_EXPIRY=3600  # 1 hour
```

## 📊 **Data Sources**

- **Primary**: Yahoo Finance (free, no API key required)
- **Backup**: Alpha Vantage (optional, requires API key)
- **Alternative**: IEX Cloud (optional, requires API key)

## 🔒 **Security Features**

- ✅ **No hardcoded credentials** in source code
- ✅ **Environment-based configuration**
- ✅ **Secure credential management**
- ✅ **Git ignores sensitive files**

## 🎯 **Stock Universe (69 Stocks)**

The dashboard monitors a carefully curated selection of major stocks across 7 sectors:

- **Technology** (10): AAPL, MSFT, GOOGL, TSLA, NVDA, META, AMZN, NFLX, AMD, INTC
- **Financial Services** (10): JPM, BAC, WFC, GS, MS, C, AXP, BLK, SCHW, USB
- **Healthcare** (10): JNJ, PFE, UNH, ABBV, MRK, TMO, DHR, LLY, BMY, AMGN
- **Consumer Goods** (10): PG, KO, PEP, WMT, HD, MCD, SBUX, NKE, DIS, CMCSA
- **Energy** (10): XOM, CVX, COP, EOG, SLB, KMI, PSX, VLO, MPC, OXY
- **Industrial** (10): BA, CAT, MMM, GE, HON, UPS, FDX, LMT, RTX, NOC
- **Materials** (9): LIN, APD, FCX, NEM, DOW, DD, ECL, ALB, NUE

**Why This Selection?**
- Represents ~40% of total US market cap
- Covers all major economic sectors
- High liquidity and real-time data availability
- Industry standard approach

## 🛠️ **Development**

### **Adding New Pages**
1. Create new file in `app/pages/`
2. Import in `app/main.py`
3. Add to navigation tabs

### **Adding New Components**
1. Create in `app/components/`
2. Import where needed
3. Follow existing patterns

### **Styling**
- All CSS in `app/utils/styles.py`
- Use CSS classes for consistent design
- Follow existing color scheme (#00D4AA primary)

## 📦 **Dependencies**

- **Streamlit** (1.28.0+) - Web framework
- **Pandas** (2.0.0+) - Data manipulation
- **NumPy** (1.24.0+) - Numerical computing
- **Plotly** (5.15.0+) - Interactive charts
- **yfinance** (0.2.18+) - Stock data
- **python-dotenv** (1.0.0+) - Environment variables
- **Supabase** (2.0.0+) - Backend services

## 🚀 **Deployment**

### **Streamlit Cloud (Recommended)**
1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy automatically

### **Local Development**
```bash
cd app
python3 -m streamlit run main.py --server.port 8501
```

### **Production Server**
```bash
cd app
python3 -m streamlit run main.py --server.port 8501 --server.headless true
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

## 📄 **License**

MIT License - see LICENSE file for details

## 🆘 **Support**

- **Issues**: Create GitHub issue
- **Documentation**: Check README and code comments
- **Community**: Streamlit and Supabase communities

## 🔮 **Future Enhancements**

- **Real-time updates** with WebSocket integration
- **Advanced analytics** with machine learning
- **Mobile app** companion
- **Social features** for portfolio sharing
- **Backtesting** for strategy validation

---

**Built with ❤️ using Python, Streamlit, and Supabase**

**Version**: 2.0.0 (Modular Structure)
**Last Updated**: August 2024
