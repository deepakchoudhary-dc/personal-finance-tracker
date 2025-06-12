"""
Data preprocessing and cleaning module
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Data preprocessing and cleaning class"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
    
    def clean_inflation_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess inflation data
        
        Args:
            df: Raw inflation data
            
        Returns:
            pandas.DataFrame: Cleaned data
        """
        try:
            if df.empty:
                return df
            
            # Ensure proper column names
            df = df.copy()
            
            # Handle missing values
            df = self._handle_missing_values(df)
            
            # Remove outliers (inflation rates beyond reasonable bounds)
            df = self._remove_outliers(df, 'value', lower_bound=-20, upper_bound=100)
            
            # Sort by date
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values(['country', 'date'])
            
            logger.info(f"Cleaned inflation data: {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning inflation data: {str(e)}")
            return df
    
    def calculate_real_income(self, 
                            nominal_income: float, 
                            inflation_rates: pd.DataFrame,
                            base_year: int = 2020) -> pd.DataFrame:
        """
        Calculate real income adjusted for inflation
        
        Args:
            nominal_income: Nominal income value
            inflation_rates: DataFrame with inflation rates
            base_year: Base year for calculation
            
        Returns:
            pandas.DataFrame: Real income data
        """
        try:
            df = inflation_rates.copy()
            
            # Calculate cumulative inflation from base year
            df = df.sort_values('date')
            df['year'] = df['date'].dt.year
            
            # Calculate cumulative inflation factor
            base_year_mask = df['year'] == base_year
            if base_year_mask.any():
                base_cpi = df.loc[base_year_mask, 'value'].iloc[0]
            else:
                base_cpi = 100  # Default base
            
            df['inflation_factor'] = df['value'] / base_cpi
            df['real_income'] = nominal_income / df['inflation_factor']
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculating real income: {str(e)}")
            return pd.DataFrame()
    
    def create_cost_of_living_index(self, 
                                  cost_data: pd.DataFrame,
                                  weights: Dict[str, float] = None) -> pd.DataFrame:
        """
        Create a composite cost of living index
        
        Args:
            cost_data: Raw cost of living data
            weights: Weights for different categories
            
        Returns:
            pandas.DataFrame: Cost of living index
        """
        try:
            if weights is None:
                weights = {
                    'rent_1br_city_center': 0.3,
                    'meal_inexpensive_restaurant': 0.2,
                    'transportation_monthly': 0.2,
                    'utilities_basic': 0.15,
                    'rent_1br_outside_center': 0.15
                }
            
            df = cost_data.copy()
            
            # Normalize each cost category (0-100 scale)
            cost_columns = [col for col in weights.keys() if col in df.columns]
            
            for col in cost_columns:
                df[f'{col}_normalized'] = (df[col] / df[col].max()) * 100
            
            # Calculate weighted index
            df['cost_of_living_index'] = 0
            for col, weight in weights.items():
                if f'{col}_normalized' in df.columns:
                    df['cost_of_living_index'] += df[f'{col}_normalized'] * weight
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating cost of living index: {str(e)}")
            return cost_data
    
    def create_affordability_score(self, 
                                 income_data: pd.DataFrame,
                                 cost_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create regional affordability score
        
        Args:
            income_data: Income data by region
            cost_data: Cost of living data by region
            
        Returns:
            pandas.DataFrame: Affordability scores
        """
        try:
            # Merge income and cost data
            merged = pd.merge(income_data, cost_data, on=['city', 'country'], how='inner')
            
            # Calculate affordability score (higher is more affordable)
            merged['affordability_score'] = (merged['average_income'] / 
                                           merged['cost_of_living_index']) * 100
            
            # Normalize to 0-100 scale
            max_score = merged['affordability_score'].max()
            merged['affordability_score_normalized'] = (
                merged['affordability_score'] / max_score) * 100
            
            return merged
            
        except Exception as e:
            logger.error(f"Error creating affordability score: {str(e)}")
            return pd.DataFrame()
    
    def prepare_time_series_data(self, 
                               df: pd.DataFrame,
                               date_column: str = 'date',
                               value_column: str = 'value') -> pd.DataFrame:
        """
        Prepare data for time series analysis
        
        Args:
            df: Input dataframe
            date_column: Name of date column
            value_column: Name of value column
            
        Returns:
            pandas.DataFrame: Prepared time series data
        """
        try:
            ts_df = df.copy()
            
            # Ensure date column is datetime
            ts_df[date_column] = pd.to_datetime(ts_df[date_column])
            
            # Sort by date
            ts_df = ts_df.sort_values(date_column)
            
            # Handle missing dates (interpolate)
            ts_df = ts_df.set_index(date_column)
            ts_df = ts_df.resample('M').mean()  # Monthly resampling
            ts_df[value_column] = ts_df[value_column].interpolate(method='linear')
            
            # Reset index
            ts_df = ts_df.reset_index()
            
            # Add time-based features
            ts_df['year'] = ts_df[date_column].dt.year
            ts_df['month'] = ts_df[date_column].dt.month
            ts_df['quarter'] = ts_df[date_column].dt.quarter
            
            return ts_df
            
        except Exception as e:
            logger.error(f"Error preparing time series data: {str(e)}")
            return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if df[col].isnull().sum() > 0:
                # Forward fill then backward fill for time series
                df[col] = df[col].fillna(method='ffill').fillna(method='bfill')
                
                # If still missing, use median
                if df[col].isnull().sum() > 0:
                    df[col] = df[col].fillna(df[col].median())
        
        return df
    
    def _remove_outliers(self, 
                        df: pd.DataFrame, 
                        column: str,
                        lower_bound: float = None,
                        upper_bound: float = None,
                        method: str = 'iqr') -> pd.DataFrame:
        """Remove outliers from specified column"""
        if column not in df.columns:
            return df
        
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
        else:
            lower = lower_bound if lower_bound is not None else df[column].min()
            upper = upper_bound if upper_bound is not None else df[column].max()
        
        return df[(df[column] >= lower) & (df[column] <= upper)]

class FeatureEngineer:
    """Feature engineering for advanced analytics"""
    
    def __init__(self):
        pass
    
    def create_demographic_features(self, 
                                  age: int,
                                  income: float,
                                  family_size: int = 1) -> Dict[str, float]:
        """
        Create demographic-based features
        
        Args:
            age: User age
            income: User income
            family_size: Number of family members
            
        Returns:
            Dict: Demographic features
        """
        features = {
            'age_group': self._get_age_group(age),
            'income_bracket': self._get_income_bracket(income),
            'per_capita_income': income / family_size,
            'life_stage_factor': self._get_life_stage_factor(age, family_size)
        }
        
        return features
    
    def create_spending_profile(self, 
                              income: float,
                              age: int,
                              location_type: str = 'urban') -> Dict[str, float]:
        """
        Create expected spending profile based on demographics
        
        Args:
            income: Annual income
            age: User age
            location_type: Urban/suburban/rural
            
        Returns:
            Dict: Expected spending by category
        """
        # Base spending percentages
        base_percentages = {
            'Housing': 0.30,
            'Food': 0.15,
            'Transportation': 0.15,
            'Healthcare': 0.08,
            'Education': 0.05,
            'Entertainment': 0.07,
            'Savings': 0.20
        }
        
        # Adjust based on age
        age_adjustments = self._get_age_spending_adjustments(age)
        
        # Adjust based on location
        location_adjustments = self._get_location_spending_adjustments(location_type)
        
        # Calculate final spending profile
        spending_profile = {}
        for category, base_pct in base_percentages.items():
            adjusted_pct = (base_pct * 
                          age_adjustments.get(category, 1.0) * 
                          location_adjustments.get(category, 1.0))
            spending_profile[category] = income * adjusted_pct
        
        return spending_profile
    
    def _get_age_group(self, age: int) -> str:
        """Categorize age into groups"""
        if age < 25:
            return 'Young Adult'
        elif age < 35:
            return 'Early Career'
        elif age < 50:
            return 'Mid Career'
        elif age < 65:
            return 'Late Career'
        else:
            return 'Retirement'
    
    def _get_income_bracket(self, income: float) -> str:
        """Categorize income into brackets"""
        if income < 30000:
            return 'Low Income'
        elif income < 60000:
            return 'Lower Middle Income'
        elif income < 100000:
            return 'Middle Income'
        elif income < 200000:
            return 'Upper Middle Income'
        else:
            return 'High Income'
    
    def _get_life_stage_factor(self, age: int, family_size: int) -> float:
        """Calculate life stage factor affecting spending"""
        base_factor = 1.0
        
        # Young family adjustment
        if 25 <= age <= 45 and family_size > 2:
            base_factor += 0.2
        
        # Single person adjustment
        if family_size == 1:
            base_factor -= 0.1
        
        return base_factor
    
    def _get_age_spending_adjustments(self, age: int) -> Dict[str, float]:
        """Get spending adjustments based on age"""
        if age < 25:
            return {
                'Housing': 0.8,  # Lower housing costs (roommates, etc.)
                'Food': 1.2,     # Higher food spending (eating out)
                'Entertainment': 1.5,  # Higher entertainment
                'Healthcare': 0.7,     # Lower healthcare costs
                'Savings': 0.8         # Lower savings rate
            }
        elif age < 35:
            return {
                'Housing': 1.1,   # Higher housing (buying home)
                'Healthcare': 0.9,
                'Education': 1.2, # Higher education spending
                'Savings': 1.0
            }
        elif age >= 65:
            return {
                'Healthcare': 1.5,    # Higher healthcare
                'Entertainment': 0.8, # Lower entertainment
                'Transportation': 0.8, # Lower transportation
                'Savings': 0.5        # Lower savings (retirement)
            }
        else:
            return {key: 1.0 for key in ['Housing', 'Food', 'Transportation', 
                                       'Healthcare', 'Education', 'Entertainment', 'Savings']}
    
    def _get_location_spending_adjustments(self, location_type: str) -> Dict[str, float]:
        """Get spending adjustments based on location type"""
        if location_type.lower() == 'urban':
            return {
                'Housing': 1.3,        # Higher urban housing
                'Transportation': 0.8, # Lower car costs (public transit)
                'Entertainment': 1.2   # Higher entertainment options
            }
        elif location_type.lower() == 'rural':
            return {
                'Housing': 0.7,        # Lower rural housing
                'Transportation': 1.3, # Higher car costs
                'Food': 0.9           # Lower food costs
            }
        else:  # suburban
            return {key: 1.0 for key in ['Housing', 'Food', 'Transportation', 
                                       'Healthcare', 'Education', 'Entertainment', 'Savings']}
