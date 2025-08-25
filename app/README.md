# Stock/ETF Dashboard - App Structure

## 🏗️ Project Structure

```
app/
├── main.py              # Main entry point with navigation
├── pages/               # Individual dashboard pages
│   ├── dashboard.py     # Main dashboard view
│   ├── stock_browser.py # Stock screening & browsing
│   ├── portfolio.py     # Portfolio simulation & analysis
│   └── market_analysis.py # Market insights & sector analysis
├── utils/               # Utility functions & styles
│   └── styles.py        # Custom CSS styling
└── requirements.txt     # Python dependencies
```

## 🚀 Running the Dashboard

```bash
cd app
python3 -m streamlit run main.py --server.port 8501
```

## 📱 Features by Page

- **🏠 Dashboard**: Market overview, top movers, quick lookup
- **🔍 Stock Browser**: Stock screening by criteria
- **💼 Portfolio**: Create scenarios, historical analysis
- **📊 Market Analysis**: Sector performance, market breadth

## 🔧 Development

- All CSS in `app/utils/styles.py`
- Follow existing patterns for new pages
- Use environment variables for configuration
