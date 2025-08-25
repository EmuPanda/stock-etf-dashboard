import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# Import our services
from data_service import StockDataService
from portfolio_service import PortfolioService

# Page configuration
st.set_page_config(
    page_title="Stock/ETF Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize services
def get_services():
    return StockDataService(), PortfolioService()

data_service, portfolio_service = get_services()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00D4AA;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .metric-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #333333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    .positive-change {
        color: #00FF88;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .negative-change {
        color: #FF6B6B;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stock-lookup-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #333333;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        margin: 1rem 0;
    }
    .stock-metric {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00D4AA;
        margin: 0.5rem 0;
    }
    .mover-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #333333;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.5rem;
    }
    .mover-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        border-color: #00D4AA;
    }

    .portfolio-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #333333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    
    .portfolio-summary {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #333333;
        margin: 0.5rem 0;
    }
    
    .portfolio-holdings {
        background: rgba(255,255,255,0.02);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #444444;
        margin: 1rem 0;
    }
    
    .performance-comparison {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #333333;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00D4AA 0%, #00B894 100%);
        color: #000000;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,212,170,0.4);
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        border: 1px solid #333333;
        color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00D4AA;
        box-shadow: 0 0 0 2px rgba(0,212,170,0.2);
    }
</style>


""", unsafe_allow_html=True)

def main():
    # Header with better icon
    st.markdown('<h1 class="main-header">📈 Stock/ETF Dashboard</h1>', unsafe_allow_html=True)
    
    # Horizontal navigation tabs at the top
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "🔍 Stock Browser", "💼 Portfolio Simulator", "📊 Market Analysis"])
    
    # Display the selected page
    with tab1:
        show_dashboard()
    with tab2:
        show_stock_browser()
    with tab3:
        show_portfolio_simulator()
    with tab4:
        show_market_analysis()

def show_dashboard():
    """Main dashboard view with improved design"""
    st.header("🎯 Market Overview")
    
    # Load market data first
    with st.spinner("🔄 Fetching market data..."):
        try:
            # Force fresh data by clearing any potential cache
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

def show_stock_browser():
    """Stock browser and screening with improved design"""
    st.header("🔍 Stock Browser & Screening")
    
    # Screening filters
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 Screening Criteria</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        min_pe = st.number_input("Min P/E Ratio", min_value=0.0, value=0.0, step=0.1)
        max_pe = st.number_input("Max P/E Ratio", min_value=0.0, value=100.0, step=0.1)
    
    with col2:
        min_dividend = st.number_input("Min Dividend Yield (%)", min_value=0.0, value=0.0, step=0.1) / 100
        sector = st.selectbox("Sector", ["All", "Technology", "Healthcare", "Financial", "Consumer", "Industrial"])
    
    with col3:
        min_market_cap = st.number_input("Min Market Cap ($B)", min_value=0.0, value=0.0, step=0.1) * 1e9
        max_market_cap = st.number_input("Max Market Cap ($B)", min_value=0.0, value=1000.0, step=0.1) * 1e9
    
    with col4:
        if st.button("🔍 Screen Stocks", type="primary"):
            filters = {}
            if min_pe > 0:
                filters['min_pe'] = min_pe
            if max_pe < 100:
                filters['max_pe'] = max_pe
            if min_dividend > 0:
                filters['min_dividend'] = min_dividend
            if sector != "All":
                filters['sector'] = sector
            if min_market_cap > 0:
                filters['min_market_cap'] = min_market_cap
            if max_market_cap < 1000e9:
                filters['max_market_cap'] = max_market_cap
            
            with st.spinner("🔍 Screening stocks..."):
                screened_stocks = data_service.screen_stocks(filters)
                
                if screened_stocks:
                    st.success(f"✅ Found {len(screened_stocks)} stocks matching criteria")
                    
                    # Convert to DataFrame for display
                    df = pd.DataFrame(screened_stocks)
                    
                    # Format columns
                    df['current_price'] = df['current_price'].apply(lambda x: f"${x:,.2f}" if x else "N/A")
                    df['price_change_percent'] = df['price_change_percent'].apply(lambda x: f"{x:+.2f}%" if x else "N/A")
                    df['market_cap'] = df['market_cap'].apply(lambda x: f"${x/1e9:.2f}B" if x else "N/A")
                    df['pe_ratio'] = df['pe_ratio'].apply(lambda x: f"{x:.2f}" if x else "N/A")
                    df['dividend_yield'] = df['dividend_yield'].apply(lambda x: f"{x*100:.2f}%" if x else "N/A")
                    
                    # Display results in full width below the filters
                    st.markdown("---")
                    st.subheader("📊 Screening Results")
                    
                    # Show results in a full-width table
                    st.dataframe(
                        df[['ticker', 'company_name', 'current_price', 'price_change_percent', 
                            'market_cap', 'pe_ratio', 'dividend_yield', 'sector']],
                        use_container_width=True,
                        height=400
                    )
                    
                    # Add download button for results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"stock_screening_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No stocks found matching the criteria")

def show_portfolio_simulator():
    """Real portfolio analysis tool with historical performance simulation"""
    st.header("💼 Portfolio Analysis & Simulation")
    st.markdown("Simulate historical performance and analyze investment strategies with real market data.")
    
    # Initialize session state for portfolios
    if 'portfolios' not in st.session_state:
        st.session_state.portfolios = {}
    
    # Portfolio creation section
    st.subheader("📝 Create Investment Scenario")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        portfolio_name = st.text_input("Scenario Name:", placeholder="e.g., Tech Growth Strategy, Dividend Portfolio...")
    
    with col2:
        initial_capital = st.number_input("Initial Investment ($):", min_value=1000, value=10000, step=1000)
    
    with col3:
        if st.button("➕ Create Scenario", type="primary"):
            if portfolio_name and portfolio_name not in st.session_state.portfolios:
                st.session_state.portfolios[portfolio_name] = {
                    'stocks': {},
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'initial_capital': initial_capital,
                    'analysis_period': '1y'  # Default to 1 year
                }
                st.success(f"✅ Investment scenario '{portfolio_name}' created!")
                st.rerun()
            elif portfolio_name in st.session_state.portfolios:
                st.error("❌ Scenario name already exists!")
    
    st.markdown("---")
    
    # Portfolio management section
    if st.session_state.portfolios:
        st.subheader("📊 Analyze Investment Scenarios")
        
        # Portfolio selector
        selected_portfolio = st.selectbox(
            "Select Scenario:",
            list(st.session_state.portfolios.keys())
        )
        
        if selected_portfolio:
            portfolio = st.session_state.portfolios[selected_portfolio]
            
            # Analysis period selector
            col1, col2 = st.columns([1, 3])
            with col1:
                analysis_period = st.selectbox(
                    "Analysis Period:",
                    ['6m', '1y', '2y', '5y'],
                    index=1,
                    key=f"period_{selected_portfolio}"
                )
                portfolio['analysis_period'] = analysis_period
            
            with col2:
                st.markdown(f"**Initial Investment: ${portfolio['initial_capital']:,.0f}**")
            
            # Add stocks section
            st.markdown("**Add Stocks to Your Scenario**")
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                ticker = st.text_input("Stock Ticker:", placeholder="Insert ticker here", key=f"ticker_{selected_portfolio}")
            
            with col2:
                allocation_percent = st.number_input("Allocation %:", min_value=1.0, max_value=100.0, value=25.0, step=1.0, key=f"alloc_{selected_portfolio}")
            
            with col3:
                shares = st.number_input("Shares:", min_value=1, value=100, step=1, key=f"shares_{selected_portfolio}")
            
            with col4:
                if st.button("➕ Add Stock", key=f"add_{selected_portfolio}"):
                    if ticker and allocation_percent > 0 and shares > 0:
                        ticker = ticker.upper()
                        try:
                            # Get current stock data
                            stock_data = data_service.get_stock_data(ticker)
                            if stock_data and stock_data.get('current_price', 0) > 0:
                                current_price = stock_data['current_price']
                                portfolio['stocks'][ticker] = {
                                    'shares': shares,
                                    'allocation_percent': allocation_percent,
                                    'current_price': current_price,
                                    'company_name': stock_data.get('company_name', ticker),
                                    'added_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                                }
                                st.success(f"✅ Added {ticker} ({allocation_percent}% allocation)")
                                st.rerun()
                            else:
                                st.error(f"❌ Could not fetch data for {ticker}")
                        except Exception as e:
                            st.error(f"❌ Error adding {ticker}: {e}")
            
            st.markdown("---")
            
            # Portfolio analysis
            if portfolio['stocks']:
                st.markdown("**📈 Historical Performance Analysis**")
                
                # Run portfolio simulation
                with st.spinner("🔄 Analyzing historical performance..."):
                    try:
                        # Get historical data for all stocks
                        portfolio_returns = {}
                        stock_weights = {}
                        total_allocation = sum(stock['allocation_percent'] for stock in portfolio['stocks'].values())
                        
                        for ticker, holding in portfolio['stocks'].items():
                            # Get historical data
                            hist_data = data_service.get_historical_data(ticker, portfolio['analysis_period'])
                            if not hist_data.empty:
                                # Calculate returns
                                returns = hist_data['Close'].pct_change().dropna()
                                portfolio_returns[ticker] = returns
                                stock_weights[ticker] = holding['allocation_percent'] / total_allocation
                        
                        if portfolio_returns:
                            # Calculate portfolio performance
                            portfolio_df = pd.DataFrame(portfolio_returns)
                            portfolio_df = portfolio_df.fillna(0)
                            
                            # Weighted portfolio returns
                            weighted_returns = (portfolio_df * pd.Series(stock_weights)).sum(axis=1)
                            
                            # Calculate metrics
                            total_return = ((1 + weighted_returns).prod() - 1) * 100
                            annualized_return = ((1 + total_return/100) ** (252/len(weighted_returns)) - 1) * 100
                            volatility = weighted_returns.std() * np.sqrt(252) * 100
                            sharpe_ratio = (annualized_return / 100) / (volatility / 100) if volatility > 0 else 0
                            
                            # Calculate max drawdown
                            cumulative_returns = (1 + weighted_returns).cumprod()
                            running_max = cumulative_returns.expanding().max()
                            drawdown = (cumulative_returns - running_max) / running_max
                            max_drawdown = drawdown.min() * 100
                            
                            # Final portfolio value
                            final_value = portfolio['initial_capital'] * (1 + total_return/100)
                            absolute_gain = final_value - portfolio['initial_capital']
                            
                            # Display results
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("💰 Final Value", f"${final_value:,.0f}", f"${absolute_gain:+,.0f}")
                            
                            with col2:
                                st.metric("📊 Total Return", f"{total_return:+.1f}%", f"{annualized_return:+.1f}% annualized")
                            
                            with col3:
                                st.metric("📈 Volatility", f"{volatility:.1f}%", "Annualized")
                            
                            with col4:
                                st.metric("⚡ Sharpe Ratio", f"{sharpe_ratio:.2f}", "Risk-adjusted return")
                            
                            # Performance chart
                            st.markdown("**Performance Over Time**")
                            fig = go.Figure()
                            
                            # Portfolio performance
                            fig.add_trace(go.Scatter(
                                x=cumulative_returns.index,
                                y=cumulative_returns.values * portfolio['initial_capital'],
                                mode='lines',
                                name='Your Portfolio',
                                line=dict(color='#00D4AA', width=3)
                            ))
                            
                            # S&P 500 comparison
                            try:
                                sp500_data = data_service.get_historical_data('^GSPC', portfolio['analysis_period'])
                                if not sp500_data.empty:
                                    sp500_returns = sp500_data['Close'].pct_change().dropna()
                                    sp500_cumulative = (1 + sp500_returns).cumprod()
                                    sp500_final_value = portfolio['initial_capital'] * sp500_cumulative.iloc[-1]
                                    
                                    fig.add_trace(go.Scatter(
                                        x=sp500_cumulative.index,
                                        y=sp500_cumulative.values * portfolio['initial_capital'],
                                        mode='lines',
                                        name='S&P 500',
                                        line=dict(color='#FF6B6B', width=2, dash='dash')
                                    ))
                                    
                                    # S&P 500 metrics
                                    sp500_return = ((sp500_cumulative.iloc[-1] - 1) * 100)
                                    sp500_vol = sp500_returns.std() * np.sqrt(252) * 100
                                    
                                    st.markdown("**📊 vs S&P 500 Benchmark**")
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        st.metric("📈 S&P 500 Return", f"{sp500_return:+.1f}%")
                                    
                                    with col2:
                                        st.metric("📊 S&P 500 Volatility", f"{sp500_vol:.1f}%")
                                    
                                    with col3:
                                        outperformance = total_return - sp500_return
                                        if outperformance > 0:
                                            st.success(f"🎉 Outperforming by {outperformance:+.1f}%!")
                                        else:
                                            st.warning(f"📉 Underperforming by {abs(outperformance):+.1f}%")
                                    
                            except Exception as e:
                                st.warning("Could not load S&P 500 comparison data")
                            
                            fig.update_layout(
                                title=f"{selected_portfolio} - {portfolio['analysis_period']} Performance",
                                xaxis_title="Date",
                                yaxis_title="Portfolio Value ($)",
                                height=500,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#FFFFFF'),
                                xaxis=dict(gridcolor='#333333'),
                                yaxis=dict(gridcolor='#333333')
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Stock breakdown
                            st.markdown("**📋 Individual Stock Performance**")
                            stock_breakdown = []
                            
                            for ticker, holding in portfolio['stocks'].items():
                                if ticker in portfolio_returns:
                                    stock_return = ((1 + portfolio_returns[ticker]).prod() - 1) * 100
                                    stock_value = portfolio['initial_capital'] * (stock_weights[ticker])
                                    stock_final_value = stock_value * (1 + stock_return/100)
                                    
                                    stock_breakdown.append({
                                        'Stock': ticker,
                                        'Company': holding['company_name'],
                                        'Allocation': f"{holding['allocation_percent']:.1f}%",
                                        'Initial Value': f"${stock_value:,.0f}",
                                        'Final Value': f"${stock_final_value:,.0f}",
                                        'Return': f"{stock_return:+.1f}%",
                                        'Contribution': f"${stock_final_value - stock_value:+,.0f}"
                                    })
                            
                            if stock_breakdown:
                                breakdown_df = pd.DataFrame(stock_breakdown)
                                st.dataframe(breakdown_df, use_container_width=True)
                            
                            # Risk metrics
                            st.markdown("**⚠️ Risk Analysis**")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("📉 Max Drawdown", f"{max_drawdown:.1f}%")
                            
                            with col2:
                                # Calculate beta vs S&P 500
                                try:
                                    if '^GSPC' in portfolio_returns:
                                        sp500_returns = portfolio_returns['^GSPC']
                                    else:
                                        sp500_data = data_service.get_historical_data('^GSPC', portfolio['analysis_period'])
                                        sp500_returns = sp500_data['Close'].pct_change().dropna()
                                    
                                    # Align dates
                                    aligned_data = pd.concat([weighted_returns, sp500_returns], axis=1).dropna()
                                    if len(aligned_data) > 1:
                                        covariance = aligned_data.iloc[:, 0].cov(aligned_data.iloc[:, 1])
                                        sp500_variance = aligned_data.iloc[:, 1].var()
                                        beta = covariance / sp500_variance if sp500_variance > 0 else 1
                                        st.metric("📊 Beta", f"{beta:.2f}")
                                    else:
                                        st.metric("📊 Beta", "N/A")
                                except:
                                    st.metric("📊 Beta", "N/A")
                            
                            with col3:
                                # Calculate correlation
                                try:
                                    if len(aligned_data) > 1:
                                        correlation = aligned_data.iloc[:, 0].corr(aligned_data.iloc[:, 1])
                                        st.metric("🔗 Correlation", f"{correlation:.2f}")
                                    else:
                                        st.metric("🔗 Correlation", "N/A")
                                except:
                                    st.metric("🔗 Correlation", "N/A")
                            
                            # Export functionality
                            st.markdown("---")
                            st.subheader("📤 Export Analysis")
                            
                            if st.button("💾 Download Analysis as CSV"):
                                # Create comprehensive export
                                export_data = {
                                    'Metric': ['Initial Investment', 'Final Value', 'Total Return', 'Annualized Return', 
                                             'Volatility', 'Sharpe Ratio', 'Max Drawdown', 'Beta', 'Correlation'],
                                    'Value': [portfolio['initial_capital'], final_value, f"{total_return:.2f}%", 
                                             f"{annualized_return:.2f}%", f"{volatility:.2f}%", f"{sharpe_ratio:.2f}", 
                                             f"{max_drawdown:.2f}%", f"{beta:.2f}" if 'beta' in locals() else "N/A", 
                                             f"{correlation:.2f}" if 'correlation' in locals() else "N/A"]
                                }
                                
                                export_df = pd.DataFrame(export_data)
                                csv = export_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV",
                                    data=csv,
                                    file_name=f"{selected_portfolio}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                        
                        else:
                            st.error("❌ Could not fetch historical data for portfolio analysis")
                    
                    except Exception as e:
                        st.error(f"❌ Error analyzing portfolio: {e}")
                        st.info("💡 Try adding stocks and selecting a different time period")
                
                # Portfolio management
                st.markdown("---")
                st.subheader("🗂️ Portfolio Management")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🗑️ Delete Portfolio", key=f"delete_{selected_portfolio}"):
                        del st.session_state.portfolios[selected_portfolio]
                        st.success("✅ Portfolio deleted!")
                        st.rerun()
                
                with col2:
                    if st.button("🔄 Reset Analysis", key=f"reset_{selected_portfolio}"):
                        portfolio['stocks'] = {}
                        st.success("✅ Portfolio reset!")
                        st.rerun()
            
            else:
                st.info("📝 Add some stocks to see your portfolio analysis!")
                st.markdown("**💡 Example Scenarios to Try:**")
                st.markdown("""
                - **Tech Growth**: AAPL (30%), MSFT (30%), GOOGL (20%), NVDA (20%)
                - **Dividend Portfolio**: JNJ (25%), PG (25%), KO (25%), MMM (25%)
                - **Balanced Mix**: AAPL (20%), JNJ (20%), JPM (20%), XOM (20%), TLT (20%)
                """)
    
    else:
        st.info("📝 Create your first investment scenario to get started!")
        
        # Show example scenarios
        st.markdown("**💡 Example Investment Scenarios:**")
        st.markdown("""
        - **Tech Growth Strategy**: $10K invested in tech stocks over 1 year
        - **Dividend Income Portfolio**: $10K in dividend-paying stocks over 2 years  
        - **Conservative Mix**: $10K in blue-chip stocks over 5 years
        - **Sector Rotation**: $10K rotated between sectors over 2 years
        """)

def show_market_analysis():
    """Market analysis and insights with improved design"""
    st.header("📊 Market Analysis")
    
    # Sector performance
    st.markdown("""
    <div class="metric-card">
        <h3>🏭 Sector Performance Today</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("*Shows how each major sector performed today based on average price changes of key stocks*")
    
    # Popular stocks by sector for analysis
    sector_stocks = {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META'],
        'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'TMO'],
        'Financial': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
        'Consumer': ['AMZN', 'TSLA', 'NFLX', 'HD', 'MCD'],
        'Industrial': ['BA', 'CAT', 'GE', 'MMM', 'HON']
    }
    
    sector_performance = {}
    
    for sector, stocks in sector_stocks.items():
        sector_return = 0
        valid_stocks = 0
        
        for ticker in stocks:
            try:
                stock_data = data_service.get_stock_data(ticker)
                if stock_data and stock_data.get('price_change_percent'):
                    sector_return += stock_data['price_change_percent']
                    valid_stocks += 1
            except:
                continue
        
        if valid_stocks > 0:
            sector_performance[sector] = sector_return / valid_stocks
    
    if sector_performance:
        # Display sector performance in easy-to-read format first
        st.subheader("📊 Sector Performance Summary")
        
        # Create a clean table format
        col1, col2, col3 = st.columns(3)
        
        # Sort sectors by performance
        sorted_sectors = sorted(sector_performance.items(), key=lambda x: x[1], reverse=True)
        
        with col1:
            for i in range(0, len(sorted_sectors), 3):
                if i < len(sorted_sectors):
                    sector, change = sorted_sectors[i]
                    color = "🟢" if change > 0 else "🔴"
                    st.markdown(f"**{color} {sector}**")
                    st.markdown(f"*{change:+.2f}%*")
        
        with col2:
            for i in range(1, len(sorted_sectors), 3):
                if i < len(sorted_sectors):
                    sector, change = sorted_sectors[i]
                    color = "🟢" if change > 0 else "🔴"
                    st.markdown(f"**{color} {sector}**")
                    st.markdown(f"*{change:+.2f}%*")
        
        with col3:
            for i in range(2, len(sorted_sectors), 3):
                if i < len(sorted_sectors):
                    sector, change = sorted_sectors[i]
                    color = "🟢" if change > 0 else "🔴"
                    st.markdown(f"**{color} {sector}**")
                    st.markdown(f"*{change:+.2f}%*")
        
        st.markdown("---")
        st.subheader("📈 Visual Chart")
        
        # Create sector performance chart
        fig = px.bar(
            x=list(sector_performance.keys()),
            y=list(sector_performance.values()),
            title="Sector Performance Today (Average % Change)",
            color=list(sector_performance.values()),
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            xaxis_title="Sector",
            yaxis_title="Average Daily Change (%)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Market breadth
    st.markdown("""
    <div class="metric-card">
        <h3>📈 Market Breadth Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("*Shows market sentiment by analyzing how many major stocks are moving up vs down today*")
    
    # Explain what market breadth means
    with st.expander("ℹ️ **What is Market Breadth?**"):
        st.markdown("""
        **Market Breadth** measures how broad-based market movements are:
        
        - **📈 Advancing**: Stocks that went up today
        - **📉 Declining**: Stocks that went down today  
        - **➡️ Unchanged**: Stocks with minimal price change
        
        **Why This Matters:**
        - **Strong breadth** = Many stocks moving up (bullish market)
        - **Weak breadth** = Few stocks moving up (narrow rally)
        - **Mixed breadth** = Balanced up/down movement
        
        **Stocks Analyzed (10 major stocks):**
        AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, NFLX, JPM, JNJ
        
        These represent different sectors and give a snapshot of overall market sentiment.
        """)
    
    # Analyze popular stocks for market breadth
    popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'JPM', 'JNJ']
    
    advancing = 0
    declining = 0
    unchanged = 0
    
    stock_data_list = []
    
    for ticker in popular_stocks:
        try:
            data = data_service.get_stock_data(ticker)
            if data and data.get('price_change'):
                stock_data_list.append(data)
                if data['price_change'] > 0:
                    advancing += 1
                elif data['price_change'] < 0:
                    declining += 1
                else:
                    unchanged += 1
        except:
            continue
    
    if stock_data_list:
        st.subheader("📊 Today's Market Sentiment")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Stocks Up Today", advancing, delta=f"+{advancing}")
        
        with col2:
            st.metric("📉 Stocks Down Today", declining, delta=f"-{declining}")
        
        with col3:
            st.metric("➡️ Stocks Unchanged", unchanged)
        
        # Market breadth chart
        fig = go.Figure(data=[
            go.Pie(
                labels=['Stocks Up', 'Stocks Down', 'Unchanged'],
                values=[advancing, declining, unchanged],
                hole=0.3,
                marker_colors=['#00FF88', '#FF6B6B', '#6C757D']
            )
        ])
        
        fig.update_layout(
            title="Market Sentiment Breakdown",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add market sentiment interpretation
        st.markdown("---")
        st.subheader("🎯 Market Sentiment Interpretation")
        
        if advancing > declining and advancing >= 7:
            st.success("**🟢 Strong Bullish Sentiment**: Most major stocks are advancing, indicating broad market strength.")
        elif advancing > declining:
            st.info("**🔵 Moderately Bullish**: More stocks up than down, but not overwhelmingly so.")
        elif declining > advancing and declining >= 7:
            st.error("**🔴 Strong Bearish Sentiment**: Most major stocks are declining, indicating broad market weakness.")
        elif declining > advancing:
            st.warning("**🟡 Moderately Bearish**: More stocks down than up, but not overwhelmingly so.")
        else:
            st.info("**⚪ Mixed Sentiment**: Balanced movement with no clear directional bias.")
        
        # Top movers
        st.subheader("🚀 Top Movers")
        
        # Sort by absolute change
        stock_data_list.sort(key=lambda x: abs(x.get('price_change_percent', 0)), reverse=True)
        
        top_movers_df = pd.DataFrame(stock_data_list[:10])
        
        # Format for display
        top_movers_df['current_price'] = top_movers_df['current_price'].apply(lambda x: f"${x:,.2f}" if x else "N/A")
        top_movers_df['price_change'] = top_movers_df['price_change'].apply(lambda x: f"{x:+.2f}" if x else "N/A")
        top_movers_df['price_change_percent'] = top_movers_df['price_change_percent'].apply(lambda x: f"{x:+.2f}%" if x else "N/A")
        
        st.dataframe(
            top_movers_df[['ticker', 'company_name', 'current_price', 'price_change', 'price_change_percent', 'sector']],
            use_container_width=True
        )

if __name__ == "__main__":
    main()
