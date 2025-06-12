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
    import os
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
            import importlib.util
            spec = importlib.util.spec_from_file_location("realtime_dashboard", 
                os.path.join(dashboard_path, "realtime_dashboard.py"))
            realtime_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(realtime_module)
            st.success("🌐 Loading Real-time Dashboard with Live API Data...")
            # Execute the main content of realtime dashboard
            if hasattr(realtime_module, 'main'):
                realtime_module.main()
            else:
                # If no main function, execute the script content
                exec(open(os.path.join(dashboard_path, 'realtime_dashboard.py')).read())
        except Exception as e:
            st.error(f"⚠️ Real-time dashboard unavailable: {str(e)}")
            st.info("💡 Try the Sample Data Dashboard instead")
            st.code(f"Error details: {str(e)}")
            
    elif app_mode == "Sample Data Dashboard":
        try:
            # Import and run the working dashboard
            exec(open(os.path.join(dashboard_path, 'working_dashboard.py')).read())
        except Exception as e:
            st.error(f"Error loading sample dashboard: {str(e)}")
            st.code(f"Error details: {str(e)}")
            
    elif app_mode == "Simple Dashboard":
        try:
            # Import and run the simple streamlit app
            exec(open(os.path.join(dashboard_path, 'streamlit_app.py')).read())
        except Exception as e:
            st.error(f"Error loading simple dashboard: {str(e)}")
            st.code(f"Error details: {str(e)}")
    
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
