# Stock/ETF Dashboard - New Modular Structure

## 🏗️ **Project Structure**

```
app/
├── main.py              # Main entry point with navigation
├── pages/               # Individual dashboard pages
│   ├── dashboard.py     # Main dashboard view
│   ├── stock_browser.py # Stock screening & browsing
│   ├── portfolio.py     # Portfolio simulation & analysis
│   └── market_analysis.py # Market insights & sector analysis
├── components/          # Reusable UI components (future)
├── utils/               # Utility functions & styles
│   └── styles.py        # Custom CSS styling
└── requirements.txt     # Python dependencies
```

## 🚀 **Running the Dashboard**

### Option 1: Direct Streamlit Run
```bash
cd app
streamlit run main.py --server.port 8501
```

### Option 2: Using the Launcher Script
```bash
python3 run_dashboard.py
```

## 📱 **Features by Page**

### 🏠 **Dashboard**
- Market overview (S&P 500, NASDAQ)
- Top market movers
- Quick stock lookup
- Recent portfolios

### 🔍 **Stock Browser**
- Stock screening by criteria
- P/E ratio, dividend yield, market cap filters
- Export results to CSV

### 💼 **Portfolio Simulator**
- Create investment scenarios
- Historical performance analysis
- Risk metrics (Sharpe ratio, beta, correlation)
- S&P 500 benchmark comparison

### 📊 **Market Analysis**
- Sector performance analysis
- Market breadth indicators
- Market sentiment interpretation
- Top movers tracking

## 🔧 **Development**

### Adding New Pages
1. Create new file in `app/pages/`
2. Import in `app/main.py`
3. Add to navigation tabs

### Adding New Components
1. Create in `app/components/`
2. Import where needed
3. Follow existing patterns

### Styling
- All CSS in `app/utils/styles.py`
- Use CSS classes for consistent design
- Follow existing color scheme (#00D4AA primary)

## 📦 **Dependencies**

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts
- **yfinance**: Stock data
- **python-dotenv**: Environment variables

## 🔒 **Security**

- All credentials in `.env` file
- Environment variables loaded in `config.py`
- No hardcoded secrets in source code
