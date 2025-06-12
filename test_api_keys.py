"""
🔑 API Configuration Helper
Run this to test your API keys before deploying
"""
import os
import requests

def test_fred_api(api_key):
    """Test FRED API key"""
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={api_key}&file_type=json&limit=1"
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def test_exchange_rate_api(api_key):
    """Test Exchange Rate API key"""
    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔑 Personal Finance Tracker - API Key Tester")
    print("=" * 50)
    
    # Test FRED API
    fred_key = input("\n🏦 Enter your FRED API key (or press Enter to skip): ").strip()
    if fred_key:
        print("🔄 Testing FRED API...")
        if test_fred_api(fred_key):
            print("✅ FRED API key is working!")
        else:
            print("❌ FRED API key failed - check your key")
    else:
        print("⏭️ Skipping FRED API test")
    
    # Test Exchange Rate API
    exchange_key = input("\n💱 Enter your Exchange Rate API key (or press Enter to skip): ").strip()
    if exchange_key:
        print("🔄 Testing Exchange Rate API...")
        if test_exchange_rate_api(exchange_key):
            print("✅ Exchange Rate API key is working!")
        else:
            print("❌ Exchange Rate API key failed - check your key")
    else:
        print("⏭️ Skipping Exchange Rate API test")
    
    print("\n🎯 Results Summary:")
    print("-" * 30)
    
    if fred_key and exchange_key:
        print("🎉 All APIs configured! Full real-time features available.")
    elif fred_key or exchange_key:
        print("⚡ Partial setup complete - some real-time features available.")
    else:
        print("📊 No API keys configured - app will use sample data.")
    
    print("\n📋 For Streamlit Cloud deployment:")
    print("1. Go to your app settings")
    print("2. Click 'Secrets'")
    print("3. Add your working API keys")
    
    if fred_key:
        print(f"\nFRED_API_KEY = \"{fred_key}\"")
    if exchange_key:
        print(f"EXCHANGE_RATE_API_KEY = \"{exchange_key}\"")
    
    print("\n📖 Need API keys? See API_KEYS_SETUP.md for instructions!")

if __name__ == "__main__":
    main()
