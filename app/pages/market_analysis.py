import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from data_service import StockDataService
from app.utils.styles import get_custom_css

def show_market_analysis():
    """Market analysis and insights with improved design"""
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
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
                data_service = StockDataService()
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
            data_service = StockDataService()
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
