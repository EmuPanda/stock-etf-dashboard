import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime


from data_service import StockDataService
from portfolio_service import PortfolioService
from utils.styles import get_custom_css

def show_portfolio_simulator():
    """Real portfolio analysis tool with historical performance simulation"""
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
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
                            data_service = StockDataService()
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
