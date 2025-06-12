"""
API Key Status Checker
Simple utility to help users verify their API keys are working
"""
import streamlit as st
import requests
import os

def check_api_keys():
    """Check and display API key status"""
    st.markdown("## 🔑 API Keys Status")
    
    # Get API keys from secrets or environment
    fred_key = st.secrets.get("FRED_API_KEY", os.getenv("FRED_API_KEY", ""))
    exchange_key = st.secrets.get("EXCHANGE_RATE_API_KEY", os.getenv("EXCHANGE_RATE_API_KEY", ""))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏦 FRED API")
        if fred_key and fred_key != "your_fred_key_here":
            # Test FRED API
            try:
                test_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={fred_key}&file_type=json&limit=1"
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200:
                    st.success("✅ FRED API Working!")
                    st.info("🌐 Real-time economic data enabled")
                else:
                    st.error("❌ FRED API Error")
                    st.code(f"Status: {response.status_code}")
            except Exception as e:
                st.error("❌ FRED API Connection Failed")
                st.code(str(e))
        else:
            st.warning("⚠️ FRED API Key Missing")
            st.info("📊 Using sample economic data")
    
    with col2:
        st.markdown("### 💱 Exchange Rate API")
        if exchange_key and exchange_key != "your_exchange_rate_key_here":
            # Test Exchange Rate API
            try:
                test_url = f"https://v6.exchangerate-api.com/v6/{exchange_key}/latest/USD"
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200:
                    st.success("✅ Exchange Rate API Working!")
                    st.info("💱 Real-time currency data enabled")
                else:
                    st.error("❌ Exchange Rate API Error")
                    st.code(f"Status: {response.status_code}")
            except Exception as e:
                st.error("❌ Exchange Rate API Connection Failed")
                st.code(str(e))
        else:
            st.warning("⚠️ Exchange Rate API Key Missing")
            st.info("💰 Using sample currency data")
    
    # Overall status
    st.markdown("---")
    if fred_key and exchange_key:
        st.success("🎉 All APIs configured! You have full real-time data access.")
    elif fred_key or exchange_key:
        st.info("⚡ Partial API setup - some real-time features enabled.")
    else:
        st.info("📝 No API keys detected - app running with sample data.")
        
        with st.expander("🚀 Want real-time data? Get free API keys!"):
            st.markdown("""
            ### 🔑 Quick Setup (2 minutes):
            
            1. **FRED API** (Economic Data): 
               - Go to: https://fred.stlouisfed.org/docs/api/api_key.html
               - Get instant free key
            
            2. **Exchange Rate API** (Currency Data):
               - Go to: https://exchangerate-api.com/
               - 1,500 free requests/month
            
            3. **Add to Streamlit Cloud**:
               - Settings → Secrets → Add your keys
            
            See `API_KEYS_SETUP.md` for detailed instructions.
            """)

if __name__ == "__main__":
    check_api_keys()
