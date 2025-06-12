"""
Data collection module for Finance Tracker
Handles API calls and data acquisition from various sources
"""
import requests
import pandas as pd
import wbdata
from fredapi import Fred
import yfinance as yf
from typing import Dict, List, Optional, Tuple
import time
from datetime import datetime, timedelta
import logging
from config.config import Config, DATA_SOURCES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    """Main data collection class"""
    
    def __init__(self):
        self.fred = Fred(api_key=Config.FRED_API_KEY) if Config.FRED_API_KEY else None
        
    def collect_world_bank_data(self, 
                               countries: List[str], 
                               indicators: List[str],
                               start_year: int = 2000,
                               end_year: int = None) -> pd.DataFrame:
        """
        Collect data from World Bank API
        
        Args:
            countries: List of country names
            indicators: List of indicator codes
            start_year: Start year for data collection
            end_year: End year for data collection
            
        Returns:
            pandas.DataFrame: Collected data
        """
        try:
            if end_year is None:
                end_year = datetime.now().year
                
            logger.info(f"Collecting World Bank data for {len(countries)} countries")
            
            # Convert country names to codes if needed
            country_codes = self._get_country_codes(countries)
            
            data_frames = []
            
            for indicator in indicators:
                logger.info(f"Collecting data for indicator: {indicator}")
                
                # Collect data using wbdata
                indicator_data = wbdata.get_dataframe(
                    {indicator: indicator},
                    country=country_codes,
                    data_date=(datetime(start_year, 1, 1), datetime(end_year, 12, 31))
                )
                
                if not indicator_data.empty:
                    indicator_data = indicator_data.reset_index()
                    indicator_data['indicator'] = indicator
                    data_frames.append(indicator_data)
                    
                # Respect API rate limits
                time.sleep(0.5)
            
            if data_frames:
                combined_data = pd.concat(data_frames, ignore_index=True)
                return combined_data
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error collecting World Bank data: {str(e)}")
            return pd.DataFrame()
    
    def collect_fred_data(self, 
                         series_ids: List[str],
                         start_date: str = '2000-01-01',
                         end_date: str = None) -> pd.DataFrame:
        """
        Collect data from FRED API
        
        Args:
            series_ids: List of FRED series IDs
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            pandas.DataFrame: Collected data
        """
        if not self.fred:
            logger.warning("FRED API key not configured")
            return pd.DataFrame()
            
        try:
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
                
            logger.info(f"Collecting FRED data for {len(series_ids)} series")
            
            data_frames = []
            
            for series_id in series_ids:
                logger.info(f"Collecting data for series: {series_id}")
                
                series_data = self.fred.get_series(
                    series_id,
                    start=start_date,
                    end=end_date
                )
                
                if not series_data.empty:
                    df = series_data.to_frame(name='value')
                    df['series_id'] = series_id
                    df['date'] = df.index
                    df = df.reset_index(drop=True)
                    data_frames.append(df)
                
                # Respect API rate limits
                time.sleep(0.1)
            
            if data_frames:
                combined_data = pd.concat(data_frames, ignore_index=True)
                return combined_data
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error collecting FRED data: {str(e)}")
            return pd.DataFrame()
    
    def collect_inflation_data(self, countries: List[str]) -> pd.DataFrame:
        """
        Collect inflation data for specified countries
        
        Args:
            countries: List of country names
            
        Returns:
            pandas.DataFrame: Inflation data
        """
        inflation_indicator = DATA_SOURCES['world_bank']['indicators']['inflation']
        return self.collect_world_bank_data(
            countries=countries,
            indicators=[inflation_indicator],
            start_year=2000
        )
    
    def collect_cost_of_living_data(self) -> pd.DataFrame:
        """
        Collect cost of living data from various sources
        This is a placeholder for integrating with Numbeo or similar APIs
        
        Returns:
            pandas.DataFrame: Cost of living data
        """
        # This would integrate with Numbeo API or similar sources
        # For now, return sample data structure
        sample_data = {
            'city': ['New York', 'London', 'Paris', 'Tokyo', 'Mumbai'],
            'country': ['United States', 'United Kingdom', 'France', 'Japan', 'India'],
            'rent_1br_city_center': [3000, 2500, 1800, 1500, 800],
            'rent_1br_outside_center': [2200, 1800, 1300, 1000, 500],
            'meal_inexpensive_restaurant': [20, 18, 15, 10, 5],
            'transportation_monthly': [120, 150, 75, 80, 30],
            'utilities_basic': [150, 200, 180, 120, 50]
        }
        
        return pd.DataFrame(sample_data)
    
    def _get_country_codes(self, country_names: List[str]) -> List[str]:
        """
        Convert country names to ISO codes for World Bank API
        
        Args:
            country_names: List of country names
            
        Returns:
            List[str]: List of country codes
        """
        # Mapping of common country names to ISO codes
        country_mapping = {
            'United States': 'US',
            'United Kingdom': 'GB',
            'Germany': 'DE',
            'France': 'FR',
            'Japan': 'JP',
            'Canada': 'CA',
            'Australia': 'AU',
            'India': 'IN',
            'China': 'CN',
            'Brazil': 'BR',
            'Mexico': 'MX'
        }
        
        return [country_mapping.get(name, name) for name in country_names]

class RealTimeDataCollector:
    """Real-time data collection for live updates"""
    
    def __init__(self):
        self.data_collector = DataCollector()
    
    def get_latest_inflation_rates(self, countries: List[str]) -> Dict:
        """Get the most recent inflation rates for specified countries"""
        try:
            data = self.data_collector.collect_inflation_data(countries)
            if not data.empty:
                # Get the most recent data for each country
                latest_data = data.groupby('country').tail(1)
                return latest_data.set_index('country')['value'].to_dict()
            return {}
        except Exception as e:
            logger.error(f"Error getting latest inflation rates: {str(e)}")
            return {}
    
    def get_currency_exchange_rates(self, base_currency: str = 'USD') -> Dict:
        """Get current currency exchange rates"""
        try:
            # Using yfinance for currency data
            major_currencies = ['EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'INR']
            rates = {}
            
            for currency in major_currencies:
                if currency != base_currency:
                    ticker = f"{base_currency}{currency}=X"
                    data = yf.Ticker(ticker)
                    hist = data.history(period="1d")
                    if not hist.empty:
                        rates[currency] = hist['Close'].iloc[-1]
            
            return rates
        except Exception as e:
            logger.error(f"Error getting exchange rates: {str(e)}")
            return {}
