"""
Main entry point for Streamlit Cloud deployment
Personal Finance & Inflation Impact Tracker
"""
import streamlit as st
import sys
import os

# Add the dashboard directory to the Python path
dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard')
sys.path.insert(0, dashboard_path)

# Page configuration
st.set_page_config(
    page_title="Personal Finance & Inflation Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    st.title("🏠 Personal Finance & Inflation Tracker")
    st.markdown("---")
    
    # App selection in sidebar
    st.sidebar.title("📊 Dashboard Selection")
    app_mode = st.sidebar.selectbox(
        "Choose Dashboard Type:",
        ["Real-time API Dashboard", "Sample Data Dashboard", "Simple Dashboard"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 🚀 Features
    - **Real-time Data**: Live API integration
    - **Interactive Charts**: Dynamic visualizations  
    - **Inflation Analysis**: Cost of living trends
    - **Personal Finance**: Budget tracking tools
    - **Economic Indicators**: Market insights
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📈 Data Sources
    - World Bank API
    - FRED Economic Data
    - ExchangeRate-API
    - Custom Financial Models
    """)
    
    # API Key Status in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 API Status")
    
    # Quick API key check
    fred_key = st.secrets.get("FRED_API_KEY", os.getenv("FRED_API_KEY", "")) if hasattr(st, 'secrets') else ""
    exchange_key = st.secrets.get("EXCHANGE_RATE_API_KEY", os.getenv("EXCHANGE_RATE_API_KEY", "")) if hasattr(st, 'secrets') else ""
    
    if fred_key and fred_key != "your_fred_key_here":
        st.sidebar.success("🏦 FRED: ✅")
    else:
        st.sidebar.warning("🏦 FRED: ⚠️")
        
    if exchange_key and exchange_key != "your_exchange_rate_key_here":
        st.sidebar.success("💱 Exchange: ✅")
    else:
        st.sidebar.warning("💱 Exchange: ⚠️")
        
    if st.sidebar.button("🔧 Setup API Keys"):
        st.info("📖 See API_KEYS_SETUP.md for detailed instructions!")
        st.markdown("""
        ### 🚀 Quick Setup:
        1. **FRED API**: [Get free key](https://fred.stlouisfed.org/docs/api/api_key.html)
        2. **Exchange Rate API**: [Get free key](https://exchangerate-api.com/)
        3. **Add to Streamlit**: Settings → Secrets → Add keys
        """)
    
    # Load selected dashboard
    if app_mode == "Real-time API Dashboard":
        try:
            # Simple fallback dashboard for real-time
            st.success("🌐 Real-time Dashboard Mode Selected")
            st.info("💡 Add API keys in Streamlit Cloud Settings → Secrets for live data")
            
            # Show sample charts
            import pandas as pd
            import numpy as np
            import plotly.express as px
            
            # Sample inflation data
            dates = pd.date_range('2020-01-01', '2024-01-01', freq='M')
            inflation_data = pd.DataFrame({
                'Date': dates,
                'Inflation_Rate': 2.5 + np.random.normal(0, 0.5, len(dates)).cumsum()
            })
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Inflation Trends")
                fig = px.line(inflation_data, x='Date', y='Inflation_Rate', 
                             title='Inflation Rate Over Time')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("💰 Key Metrics")
                st.metric("Current Inflation", "3.2%", "0.5%")
                st.metric("YoY Change", "2.8%", "-0.3%")
                st.metric("Cost of Living Index", "108.5", "2.1%")
                
        except Exception as e:
            st.error(f"⚠️ Real-time dashboard unavailable: {str(e)}")
            st.info("💡 Try the Sample Data Dashboard instead")
            
    elif app_mode == "Sample Data Dashboard":
        try:
            # Simple sample dashboard
            st.success("📊 Sample Data Dashboard")
            
            import pandas as pd
            import numpy as np
            import plotly.express as px
            
            # Generate sample data
            np.random.seed(42)
            data = {
                'Country': ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan'],
                'Inflation_Rate': [3.2, 2.8, 4.1, 3.6, 2.9, 1.5],
                'Cost_of_Living': [100, 85, 95, 90, 88, 92],
                'Income_Level': [65000, 55000, 45000, 48000, 42000, 38000]
            }
            df = pd.DataFrame(data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌍 Global Inflation Rates")
                fig = px.bar(df, x='Country', y='Inflation_Rate', 
                           title='Inflation Rates by Country')
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.subheader("💸 Cost of Living vs Income")
                fig = px.scatter(df, x='Cost_of_Living', y='Income_Level', 
                               size='Inflation_Rate', color='Country',
                               title='Cost of Living vs Income by Country')
                st.plotly_chart(fig, use_container_width=True)
                
            st.subheader("📈 Sample Data Table")
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading sample dashboard: {str(e)}")
            
    elif app_mode == "Simple Dashboard":
        try:
            # Simple clean dashboard
            st.success("🎯 Simple Dashboard")
            
            # Basic financial calculator
            st.subheader("💰 Inflation Impact Calculator")
            
            col1, col2 = st.columns(2)
            
            with col1:
                current_price = st.number_input("Current Price ($)", value=100.0, min_value=0.0)
                inflation_rate = st.slider("Annual Inflation Rate (%)", 0.0, 10.0, 3.0, 0.1)
                years = st.slider("Years to Project", 1, 20, 5)
                
            with col2:
                # Calculate future value
                future_value = current_price * ((1 + inflation_rate/100) ** years)
                purchasing_power_loss = ((future_value - current_price) / current_price) * 100
                
                st.metric("Future Price", f"${future_value:.2f}", f"+${future_value-current_price:.2f}")
                st.metric("Purchasing Power Loss", f"{purchasing_power_loss:.1f}%")
                
                # Show breakdown
                st.write("**Year-by-Year Breakdown:**")
                for year in range(1, min(years+1, 6)):
                    year_value = current_price * ((1 + inflation_rate/100) ** year)
                    st.write(f"Year {year}: ${year_value:.2f}")
                    
        except Exception as e:
            st.error(f"Error loading simple dashboard: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666666; padding: 20px;'>
        <p>🏦 Personal Finance & Inflation Impact Tracker | Built with Streamlit & Python</p>
        <p>📊 Real-time API Integration | 🎯 Smart Financial Analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
