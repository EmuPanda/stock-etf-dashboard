import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from data_service import StockDataService
from portfolio_service import PortfolioService
from app.utils.styles import get_custom_css

# Initialize services
def get_services():
    return StockDataService(), PortfolioService()

def show_dashboard():
    """Main dashboard view with improved design"""
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    st.header("🎯 Market Overview")
    
    # Load market data first
    with st.spinner("🔄 Fetching market data..."):
        try:
            # Force fresh data by clearing any potential cache
            data_service, portfolio_service = get_services()
            if hasattr(data_service, 'cache'):
                data_service.cache.clear()
            if hasattr(data_service, 'cache_timestamps'):
                data_service.cache_timestamps.clear()
            
            market_overview = data_service.get_market_overview()
            
            # Validate the data silently
            if not market_overview:
                st.error("No market data received")
                
        except Exception as e:
            st.error(f"Error fetching market data: {e}")
            market_overview = None
    
    # Top row: S&P 500 and NASDAQ with real data
    col1, col2 = st.columns(2)
    
    with col1:
        if market_overview and '^GSPC' in market_overview:
            sp500_data = market_overview['^GSPC']
            st.metric(
                label="📊 S&P 500",
                value=f"${sp500_data['price']:,.2f}",
                delta=f"{sp500_data['change']:+.2f} ({sp500_data['change_percent']:+.2f}%)"
            )
        else:
            st.metric(
                label="📊 S&P 500",
                value="Loading...",
                delta="Fetching data..."
            )
    
    with col2:
        if market_overview and '^IXIC' in market_overview:
            nasdaq_data = market_overview['^IXIC']
            st.metric(
                label="📈 NASDAQ",
                value=f"${nasdaq_data['price']:,.2f}",
                delta=f"{nasdaq_data['change']:+.2f} ({nasdaq_data['change_percent']:+.2f}%)"
            )
        else:
            st.metric(
                label="📈 NASDAQ",
                value="Loading...",
                delta="Fetching data..."
            )
    
    st.markdown("---")
    
    # Interesting Movers Section
    st.header("🚀 Top Market Movers")
    st.markdown("*Shows stocks with the biggest price movements today (>1% change)*")
    
    # Explain the stock universe
    with st.expander("ℹ️ **About the Stock Universe (69 stocks)**"):
        st.markdown("""
        **Why These 69 Stocks?**
        
        We monitor a carefully selected universe of major stocks across 7 key sectors to give you a comprehensive view of market movement:
        
        **Technology (10 stocks)**: AAPL, MSFT, GOOGL, TSLA, NVDA, META, AMZN, NFLX, AMD, INTC
        
        **Financial Services (10 stocks)**: JPM, BAC, WFC, GS, MS, C, AXP, BLK, SCHW, USB
        
        **Healthcare (10 stocks)**: JNJ, PFE, UNH, ABBV, MRK, TMO, DHR, LLY, BMY, AMGN
        
        **Consumer Goods (10 stocks)**: PG, KO, PEP, WMT, HD, MCD, SBUX, NKE, DIS, CMCSA
        
        **Energy (10 stocks)**: XOM, CVX, COP, EOG, SLB, KMI, PSX, VLO, MPC, OXY
        
        **Industrial (10 stocks)**: BA, CAT, MMM, GE, HON, UPS, FDX, LMT, RTX, NOC
        
        **Materials (9 stocks)**: LIN, APD, FCX, NEM, DOW, DD, ECL, ALB, NUE
        
        **Why This Selection?**
        - **Market Coverage**: Represents ~40% of total US market cap
        - **Sector Diversity**: Covers all major economic sectors
        - **Liquidity**: All stocks have high trading volume
        - **Market Leaders**: Most are S&P 500 components
        - **Real-time Data**: Live prices from Yahoo Finance API
        """)
    
    # Get a broader list of stocks to find real movers
    with st.spinner("🔄 Finding today's top movers..."):
        # Expanded list of stocks across different sectors
        stock_universe = [
            # Tech
            'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'META', 'AMZN', 'NFLX', 'AMD', 'INTC',
            # Finance
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'BLK', 'SCHW', 'USB',
            # Healthcare
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'DHR', 'LLY', 'BMY', 'AMGN',
            # Consumer
            'PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'SBUX', 'NKE', 'DIS', 'CMCSA',
            # Energy
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'KMI', 'PSX', 'VLO', 'MPC', 'OXY',
            # Industrial
            'BA', 'CAT', 'MMM', 'GE', 'HON', 'UPS', 'FDX', 'LMT', 'RTX', 'NOC',
            # Materials
            'LIN', 'APD', 'FCX', 'NEM', 'DOW', 'DD', 'ECL', 'ALB', 'NUE'
        ]
        
        movers_data = []
        for ticker in stock_universe:
            try:
                stock_data = data_service.get_stock_data(ticker)
                if stock_data and stock_data.get('current_price', 0) > 0 and stock_data.get('price_change_percent'):
                    # Only include stocks with meaningful price changes
                    if abs(stock_data['price_change_percent']) > 1.0:  # Filter for >1% moves
                        movers_data.append(stock_data)
            except Exception as e:
                continue
        
        if movers_data:
            # Sort by absolute percentage change to find biggest movers
            movers_data.sort(key=lambda x: abs(x.get('price_change_percent', 0)), reverse=True)
            
            # Display top movers in a grid
            cols = st.columns(4)
            for i, stock in enumerate(movers_data[:8]):  # Show top 8 movers
                with cols[i % 4]:
                    change_color = "positive-change" if stock.get('price_change_percent', 0) >= 0 else "negative-change"
                    change_icon = "📈" if stock.get('price_change_percent', 0) >= 0 else "📉"
                    
                    st.markdown(f"""
                    <div class="mover-card">
                        <h4>{change_icon} {stock['ticker']}</h4>
                        <div style="font-size: 1.2rem; font-weight: bold; color: #FFFFFF;">
                            ${stock.get('current_price', 0):,.2f}
                        </div>
                        <div class="{change_color}">
                            {stock.get('price_change', 0):+.2f} ({stock.get('price_change_percent', 0):+.2f}%)
                        </div>
                        <div style="color: #888888; font-size: 0.9rem;">
                            {stock.get('sector', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show summary of movers
            st.markdown("---")
            st.markdown("**📊 Market Breadth Summary**")
            st.markdown("*Shows how many stocks moved significantly today (>1% change)*")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                advancing = len([s for s in movers_data if s.get('price_change_percent', 0) > 0])
                st.metric("📈 Stocks Up Today", advancing, delta=f"+{advancing}")
            
            with col2:
                declining = len([s for s in movers_data if s.get('price_change_percent', 0) < 0])
                st.metric("📉 Stocks Down Today", declining, delta=f"-{declining}")
            
            with col3:
                st.metric("🔍 Total Stocks Monitored", len(stock_universe))
        
        else:
            st.info("📊 No significant movers found. Market might be quiet today!")
    
    st.markdown("---")
    
    # Quick Stock Lookup with improved design
    st.header("🔍 Quick Stock Lookup")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input("Enter stock ticker:", placeholder="AAPL, MSFT, GOOGL...", key="quick_lookup")
    
    with col2:
        if st.button("🔍 Lookup", type="primary", key="quick_lookup_btn"):
            if ticker:
                with st.spinner(f"🔄 Fetching data for {ticker.upper()}..."):
                    stock_data = data_service.get_stock_data(ticker.upper())
                    
                    if stock_data and stock_data.get('current_price', 0) > 0:
                        st.success(f"✅ Found {stock_data['company_name']}")
                        
                        # Beautiful stock data presentation
                        st.markdown(f"""
                        <div class="stock-lookup-card">
                            <h2 style="color: #00D4AA; text-align: center; margin-bottom: 2rem;">
                                📊 {stock_data['ticker']} - {stock_data['company_name']}
                            </h2>
                            
                            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem;">
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">Current Price</h4>
                                    <div style="font-size: 1.5rem; font-weight: bold; color: #FFFFFF;">
                                        ${stock_data['current_price']:,.2f}
                                    </div>
                                </div>
                                
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">Price Change</h4>
                                    <div class="{"positive-change" if stock_data.get('price_change', 0) >= 0 else "negative-change"}">
                                        {stock_data.get('price_change', 0):+.2f} ({stock_data.get('price_change_percent', 0):+.2f}%)
                                    </div>
                                </div>
                                
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">Volume</h4>
                                    <div style="font-size: 1.2rem; color: #FFFFFF;">
                                        {stock_data.get('volume', 0):,}
                                    </div>
                                </div>
                                
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">Market Cap</h4>
                                    <div style="font-size: 1.2rem; color: #FFFFFF;">
                                        ${stock_data.get('market_cap', 0)/1e9:.2f}B
                                    </div>
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">P/E Ratio</h4>
                                    <div style="font-size: 1.2rem; color: #FFFFFF;">
                                        {stock_data.get('pe_ratio', 'N/A') if stock_data.get('pe_ratio') else 'N/A'}
                                    </div>
                                </div>
                                
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">Dividend Yield</h4>
                                    <div style="font-size: 1.2rem; color: #FFFFFF;">
                                        {f"{stock_data.get('dividend_yield', 0)*100:.2f}%" if stock_data.get('dividend_yield') else 'N/A'}
                                    </div>
                                </div>
                                
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">Sector</h4>
                                    <div style="font-size: 1.2rem; color: #FFFFFF;">
                                        {stock_data.get('sector', 'N/A')}
                                    </div>
                                </div>
                                
                                <div class="stock-metric">
                                    <h4 style="color: #888888; margin: 0;">52W High</h4>
                                    <div style="font-size: 1.2rem; color: #FFFFFF;">
                                        ${stock_data.get('fifty_two_week_high', 'N/A') if stock_data.get('fifty_two_week_high') else 'N/A'}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show price chart
                        st.subheader("📈 Price Chart")
                        hist_data = data_service.get_historical_data(ticker.upper(), "1y")
                        
                        if not hist_data.empty:
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatter(
                                x=hist_data.index,
                                y=hist_data['Close'],
                                mode='lines',
                                name='Close Price',
                                line=dict(color='#00D4AA', width=3)
                            ))
                            
                            if 'SMA_20' in hist_data.columns:
                                fig.add_trace(go.Scatter(
                                    x=hist_data.index,
                                    y=hist_data['SMA_20'],
                                    mode='lines',
                                    name='20-Day SMA',
                                    line=dict(color='#FFD93D', width=2, dash='dash')
                                ))
                            
                            if 'SMA_50' in hist_data.columns:
                                fig.add_trace(go.Scatter(
                                    x=hist_data.index,
                                    y=hist_data['SMA_50'],
                                    mode='lines',
                                    name='50-Day SMA',
                                    line=dict(color='#6BCF7F', width=2, dash='dash')
                                ))
                            
                            fig.update_layout(
                                title=f"{ticker.upper()} - 1 Year Price Chart",
                                xaxis_title="Date",
                                yaxis_title="Price ($)",
                                height=500,
                                showlegend=True,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#FFFFFF'),
                                xaxis=dict(gridcolor='#333333'),
                                yaxis=dict(gridcolor='#333333')
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"❌ Could not find data for {ticker.upper()}")
    
    st.markdown("---")
    
    # Recent portfolios
    st.header("💼 Recent Portfolios")
    portfolios = portfolio_service.get_all_portfolios()
    
    if portfolios:
        for portfolio in portfolios:
            with st.expander(f"📁 {portfolio['name']} - ${portfolio.get('total_value', 0):,.2f}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Return", f"{portfolio.get('total_return', 0):+.2f}%")
                
                with col2:
                    st.metric("Holdings", portfolio['holdings_count'])
                
                with col3:
                    st.metric("Last Updated", portfolio['last_updated'][:10])
                
                if portfolio.get('risk_metrics'):
                    st.write("**Risk Metrics:**")
                    risk_cols = st.columns(4)
                    
                    with risk_cols[0]:
                        st.metric("Volatility", f"{portfolio['risk_metrics'].get('volatility', 0):.2f}%")
                    
                    with risk_cols[1]:
                        st.metric("Sharpe Ratio", f"{portfolio['risk_metrics'].get('sharpe_ratio', 0):.2f}")
                    
                    with risk_cols[2]:
                        st.metric("Max Drawdown", f"{portfolio['risk_metrics'].get('max_drawdown', 0):.2f}%")
                    
                    with risk_cols[3]:
                        st.metric("Risk-Free Rate", f"{portfolio['risk_metrics'].get('risk_free_rate', 0):.2f}%")
    else:
        st.info("💡 No portfolios created yet. Create one in the Portfolio Simulator!")
