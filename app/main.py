import streamlit as st
from pages.dashboard import show_dashboard
from pages.stock_browser import show_stock_browser
from pages.portfolio import show_portfolio_simulator
from pages.market_analysis import show_market_analysis

# Page configuration
st.set_page_config(
    page_title="Stock/ETF Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the Streamlit sidebar completely
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stApp > header {display: none;}
    .stApp > footer {display: none;}
    .stApp > div[data-testid="stToolbar"] {display: none;}
    .stApp > div[data-testid="stDecoration"] {display: none;}
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

if __name__ == "__main__":
    main()
