"""
Configuration management for Finance Tracker
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Keys
    FRED_API_KEY = os.getenv('FRED_API_KEY')
    WORLD_BANK_API_KEY = os.getenv('WORLD_BANK_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    QUANDL_API_KEY = os.getenv('QUANDL_API_KEY')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/finance_tracker.db')
    
    # Dashboard
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
    STREAMLIT_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', 'localhost')
    
    # Data Settings
    DATA_UPDATE_FREQUENCY = int(os.getenv('DATA_UPDATE_FREQUENCY', 24))
    DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY', 'USD')
    DEFAULT_COUNTRY = os.getenv('DEFAULT_COUNTRY', 'United States')
    DEFAULT_BASE_YEAR = int(os.getenv('DEFAULT_BASE_YEAR', 2020))
    
    # File Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')
    
    # Ensure directories exist
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        dirs = [cls.DATA_DIR, cls.RAW_DATA_DIR, cls.PROCESSED_DATA_DIR, cls.EXTERNAL_DATA_DIR]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)

# Data source configurations
DATA_SOURCES = {
    'world_bank': {
        'base_url': 'https://api.worldbank.org/v2',
        'indicators': {
            'inflation': 'FP.CPI.TOTL.ZG',
            'gdp_per_capita': 'NY.GDP.PCAP.CD',
            'unemployment': 'SL.UEM.TOTL.ZS',
            'population': 'SP.POP.TOTL'
        }
    },
    'fred': {
        'base_url': 'https://api.stlouisfed.org/fred',
        'series': {
            'us_cpi': 'CPIAUCSL',
            'us_inflation': 'CPILFESL',
            'us_unemployment': 'UNRATE',
            'us_gdp': 'GDP'
        }
    }
}

# Regional configurations
REGIONS = {
    'countries': [
        'United States', 'United Kingdom', 'Germany', 'France', 'Japan',
        'Canada', 'Australia', 'India', 'China', 'Brazil', 'Mexico'
    ],
    'cities': [
        'New York', 'London', 'Paris', 'Tokyo', 'Sydney',
        'Toronto', 'Mumbai', 'Shanghai', 'São Paulo', 'Mexico City'
    ]
}

# Budget categories for analysis
BUDGET_CATEGORIES = {
    'Housing': 0.30,      # 30% of income
    'Food': 0.15,         # 15% of income
    'Transportation': 0.15, # 15% of income
    'Healthcare': 0.08,   # 8% of income
    'Education': 0.05,    # 5% of income
    'Entertainment': 0.07, # 7% of income
    'Savings': 0.20       # 20% of income
}
