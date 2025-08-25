# Stock/ETF Dashboard

A real-time financial dashboard built with Python  for tracking stocks, analyzing portfolios, and monitoring market performance.

## Features

- **Real-time Market Data** - Live stock prices from Yahoo Finance API
- **Portfolio Simulation** - Create and analyze investment scenarios
- **Market Analysis** - Sector performance and market breadth indicators
- **Stock Screening** - Filter stocks by P/E, dividends, market cap
- **Interactive Charts** - Price history with technical indicators

## Tech Stack

- **Python 3.9+**
- **Streamlit** - Web framework
- **yfinance** - Stock data API
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/EmuPanda/stock-etf-dashboard
cd stock-etf-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the dashboard**
```bash
cd app
python3 -m streamlit run main.py --server.port 8501
```


## Usage

- **Dashboard**: Market overview and top movers
- **Stock Browser**: Screen stocks by criteria
- **Portfolio**: Simulate investment strategies
- **Market Analysis**: Sector performance insights

## Project Structure

```
app/
├── main.py              # Main entry point
├── pages/               # Dashboard pages
├── utils/               # Styling and utilities
└── requirements.txt     # Dependencies
```

## Screenshots

*Add screenshots of your dashboard here*

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request




