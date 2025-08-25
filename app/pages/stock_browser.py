import streamlit as st
import pandas as pd
from datetime import datetime


from data_service import StockDataService
from utils.styles import get_custom_css

def show_stock_browser():
    """Stock browser and screening with improved design"""
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
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
                data_service = StockDataService()
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
