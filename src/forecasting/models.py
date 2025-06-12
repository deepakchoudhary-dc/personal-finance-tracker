"""
Advanced forecasting models for inflation and cost prediction
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Machine Learning and Forecasting imports
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

logger = logging.getLogger(__name__)

class InflationForecaster:
    """Advanced inflation forecasting using multiple models"""
    
    def __init__(self):
        self.models = {}
        self.prophet_model = None
        self.arima_model = None
        self.xgb_model = None
        
    def prepare_prophet_data(self, df: pd.DataFrame, 
                           date_col: str = 'date',
                           value_col: str = 'value') -> pd.DataFrame:
        """
        Prepare data for Prophet forecasting
        
        Args:
            df: Input dataframe
            date_col: Date column name
            value_col: Value column name
            
        Returns:
            pandas.DataFrame: Prophet-formatted data
        """
        prophet_df = df[[date_col, value_col]].copy()
        prophet_df.columns = ['ds', 'y']
        prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
        prophet_df = prophet_df.sort_values('ds')
        
        return prophet_df
    
    def train_prophet_model(self, 
                          data: pd.DataFrame,
                          seasonality_mode: str = 'multiplicative',
                          yearly_seasonality: bool = True,
                          monthly_seasonality: bool = True) -> Prophet:
        """
        Train Prophet model for inflation forecasting
        
        Args:
            data: Training data in Prophet format
            seasonality_mode: 'additive' or 'multiplicative'
            yearly_seasonality: Include yearly seasonality
            monthly_seasonality: Include monthly seasonality
            
        Returns:
            Prophet: Trained model
        """
        try:
            model = Prophet(
                seasonality_mode=seasonality_mode,
                yearly_seasonality=yearly_seasonality,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05,
                seasonality_prior_scale=10
            )
            
            if monthly_seasonality:
                model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            
            model.fit(data)
            self.prophet_model = model
            
            logger.info("Prophet model trained successfully")
            return model
            
        except Exception as e:
            logger.error(f"Error training Prophet model: {str(e)}")
            return None
    
    def forecast_prophet(self, 
                        periods: int = 12,
                        freq: str = 'M') -> pd.DataFrame:
        """
        Generate Prophet forecasts
        
        Args:
            periods: Number of periods to forecast
            freq: Frequency ('M' for monthly, 'Q' for quarterly)
            
        Returns:
            pandas.DataFrame: Forecast results
        """
        if self.prophet_model is None:
            logger.error("Prophet model not trained")
            return pd.DataFrame()
        
        try:
            future = self.prophet_model.make_future_dataframe(
                periods=periods, 
                freq=freq
            )
            forecast = self.prophet_model.predict(future)
            
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
            
        except Exception as e:
            logger.error(f"Error generating Prophet forecast: {str(e)}")
            return pd.DataFrame()
    
    def train_arima_model(self, 
                         data: pd.DataFrame,
                         order: Tuple[int, int, int] = None) -> Any:
        """
        Train ARIMA model for inflation forecasting
        
        Args:
            data: Time series data
            order: ARIMA order (p, d, q)
            
        Returns:
            Fitted ARIMA model
        """
        try:
            # Check stationarity
            ts_data = data['y'].values
            
            # Auto-determine order if not provided
            if order is None:
                order = self._auto_arima_order(ts_data)
            
            model = ARIMA(ts_data, order=order)
            fitted_model = model.fit()
            
            self.arima_model = fitted_model
            
            logger.info(f"ARIMA{order} model trained successfully")
            return fitted_model
            
        except Exception as e:
            logger.error(f"Error training ARIMA model: {str(e)}")
            return None
    
    def forecast_arima(self, steps: int = 12) -> pd.DataFrame:
        """
        Generate ARIMA forecasts
        
        Args:
            steps: Number of steps to forecast
            
        Returns:
            pandas.DataFrame: Forecast results
        """
        if self.arima_model is None:
            logger.error("ARIMA model not trained")
            return pd.DataFrame()
        
        try:
            forecast = self.arima_model.forecast(steps=steps)
            conf_int = self.arima_model.get_forecast(steps=steps).conf_int()
            
            forecast_df = pd.DataFrame({
                'forecast': forecast,
                'lower_ci': conf_int.iloc[:, 0],
                'upper_ci': conf_int.iloc[:, 1]
            })
            
            return forecast_df
            
        except Exception as e:
            logger.error(f"Error generating ARIMA forecast: {str(e)}")
            return pd.DataFrame()
    
    def train_xgboost_model(self, 
                          data: pd.DataFrame,
                          feature_columns: List[str],
                          target_column: str = 'y') -> xgb.XGBRegressor:
        """
        Train XGBoost model for inflation forecasting
        
        Args:
            data: Training data
            feature_columns: List of feature column names
            target_column: Target column name
            
        Returns:
            xgb.XGBRegressor: Trained model
        """
        try:
            X = data[feature_columns]
            y = data[target_column]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            logger.info(f"XGBoost model trained - MAE: {mae:.4f}, MSE: {mse:.4f}, R²: {r2:.4f}")
            
            self.xgb_model = model
            return model
            
        except Exception as e:
            logger.error(f"Error training XGBoost model: {str(e)}")
            return None
    
    def create_ensemble_forecast(self, 
                               prophet_forecast: pd.DataFrame,
                               arima_forecast: pd.DataFrame,
                               weights: Dict[str, float] = None) -> pd.DataFrame:
        """
        Create ensemble forecast from multiple models
        
        Args:
            prophet_forecast: Prophet forecast results
            arima_forecast: ARIMA forecast results
            weights: Model weights for ensemble
            
        Returns:
            pandas.DataFrame: Ensemble forecast
        """
        if weights is None:
            weights = {'prophet': 0.6, 'arima': 0.4}
        
        try:
            ensemble_forecast = pd.DataFrame()
            
            if not prophet_forecast.empty and not arima_forecast.empty:
                min_length = min(len(prophet_forecast), len(arima_forecast))
                
                ensemble_forecast['forecast'] = (
                    weights['prophet'] * prophet_forecast['yhat'].iloc[:min_length].values +
                    weights['arima'] * arima_forecast['forecast'].iloc[:min_length].values
                )
                
                # Calculate confidence intervals
                ensemble_forecast['lower_ci'] = (
                    weights['prophet'] * prophet_forecast['yhat_lower'].iloc[:min_length].values +
                    weights['arima'] * arima_forecast['lower_ci'].iloc[:min_length].values
                )
                
                ensemble_forecast['upper_ci'] = (
                    weights['prophet'] * prophet_forecast['yhat_upper'].iloc[:min_length].values +
                    weights['arima'] * arima_forecast['upper_ci'].iloc[:min_length].values
                )
            
            return ensemble_forecast
            
        except Exception as e:
            logger.error(f"Error creating ensemble forecast: {str(e)}")
            return pd.DataFrame()
    
    def _auto_arima_order(self, ts_data: np.ndarray) -> Tuple[int, int, int]:
        """Automatically determine ARIMA order"""
        # Simple heuristic for auto ARIMA order selection
        # Check stationarity
        result = adfuller(ts_data)
        d = 0 if result[1] < 0.05 else 1
        
        # Use simple defaults
        p, q = 1, 1
        
        return (p, d, q)

class CostPredictor:
    """Predict future costs based on multiple factors"""
    
    def __init__(self):
        self.models = {}
        
    def predict_housing_costs(self, 
                            current_rent: float,
                            inflation_forecast: pd.DataFrame,
                            location_factor: float = 1.0) -> pd.DataFrame:
        """
        Predict future housing costs
        
        Args:
            current_rent: Current rent/housing cost
            inflation_forecast: Inflation forecast data
            location_factor: Location-specific adjustment factor
            
        Returns:
            pandas.DataFrame: Housing cost predictions
        """
        try:
            predictions = pd.DataFrame()
            
            if not inflation_forecast.empty:
                # Apply inflation to housing costs
                predictions['period'] = range(1, len(inflation_forecast) + 1)
                predictions['base_cost'] = current_rent
                
                # Calculate cumulative inflation effect
                cumulative_inflation = 1.0
                predicted_costs = []
                
                for inflation_rate in inflation_forecast['forecast']:
                    cumulative_inflation *= (1 + inflation_rate / 100)
                    predicted_cost = current_rent * cumulative_inflation * location_factor
                    predicted_costs.append(predicted_cost)
                
                predictions['predicted_cost'] = predicted_costs
                predictions['inflation_adjustment'] = (
                    predictions['predicted_cost'] / predictions['base_cost'] - 1
                ) * 100
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting housing costs: {str(e)}")
            return pd.DataFrame()
    
    def predict_total_living_costs(self, 
                                 current_costs: Dict[str, float],
                                 inflation_forecast: pd.DataFrame,
                                 category_factors: Dict[str, float] = None) -> pd.DataFrame:
        """
        Predict total living costs across categories
        
        Args:
            current_costs: Current costs by category
            inflation_forecast: Inflation forecast data
            category_factors: Category-specific inflation factors
            
        Returns:
            pandas.DataFrame: Total cost predictions
        """
        try:
            if category_factors is None:
                category_factors = {
                    'Housing': 1.2,        # Housing inflates faster
                    'Food': 1.1,           # Food moderately faster
                    'Transportation': 1.0, # Transportation at general rate
                    'Healthcare': 1.3,     # Healthcare inflates much faster
                    'Education': 1.1,      # Education moderately faster
                    'Entertainment': 0.9,  # Entertainment slower
                    'Utilities': 1.0       # Utilities at general rate
                }
            
            predictions = pd.DataFrame()
            predictions['period'] = range(1, len(inflation_forecast) + 1)
            
            # Predict each category
            total_predicted_costs = np.zeros(len(inflation_forecast))
            
            for category, current_cost in current_costs.items():
                category_factor = category_factors.get(category, 1.0)
                
                cumulative_inflation = 1.0
                category_costs = []
                
                for inflation_rate in inflation_forecast['forecast']:
                    cumulative_inflation *= (1 + (inflation_rate * category_factor) / 100)
                    predicted_cost = current_cost * cumulative_inflation
                    category_costs.append(predicted_cost)
                
                predictions[f'{category}_cost'] = category_costs
                total_predicted_costs += np.array(category_costs)
            
            predictions['total_cost'] = total_predicted_costs
            predictions['current_total'] = sum(current_costs.values())
            predictions['cost_increase'] = (
                predictions['total_cost'] / predictions['current_total'] - 1
            ) * 100
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting total living costs: {str(e)}")
            return pd.DataFrame()

class PersonalBudgetForecaster:
    """Forecast personal budget needs based on inflation and life changes"""
    
    def __init__(self):
        self.inflation_forecaster = InflationForecaster()
        self.cost_predictor = CostPredictor()
    
    def forecast_budget_needs(self, 
                            current_income: float,
                            current_expenses: Dict[str, float],
                            inflation_forecast: pd.DataFrame,
                            income_growth_rate: float = 0.03) -> Dict[str, pd.DataFrame]:
        """
        Forecast future budget needs
        
        Args:
            current_income: Current annual income
            current_expenses: Current expenses by category
            inflation_forecast: Inflation forecast data
            income_growth_rate: Expected annual income growth
            
        Returns:
            Dict: Budget forecasts and recommendations
        """
        try:
            results = {}
            
            # Predict future costs
            cost_predictions = self.cost_predictor.predict_total_living_costs(
                current_expenses, inflation_forecast
            )
            
            # Predict future income
            periods = len(inflation_forecast)
            future_income = []
            income = current_income
            
            for period in range(periods):
                income *= (1 + income_growth_rate)
                future_income.append(income)
            
            # Create budget analysis
            budget_analysis = pd.DataFrame({
                'period': range(1, periods + 1),
                'predicted_income': future_income,
                'predicted_expenses': cost_predictions['total_cost'],
                'surplus_deficit': np.array(future_income) - cost_predictions['total_cost'].values,
                'savings_rate': ((np.array(future_income) - cost_predictions['total_cost'].values) / 
                               np.array(future_income)) * 100
            })
            
            results['budget_analysis'] = budget_analysis
            results['cost_predictions'] = cost_predictions
            results['recommendations'] = self._generate_budget_recommendations(budget_analysis)
            
            return results
            
        except Exception as e:
            logger.error(f"Error forecasting budget needs: {str(e)}")
            return {}
    
    def _generate_budget_recommendations(self, budget_analysis: pd.DataFrame) -> List[str]:
        """Generate budget recommendations based on analysis"""
        recommendations = []
        
        # Check savings rate
        avg_savings_rate = budget_analysis['savings_rate'].mean()
        
        if avg_savings_rate < 10:
            recommendations.append("⚠️ Low savings rate projected. Consider reducing expenses or increasing income.")
        elif avg_savings_rate > 25:
            recommendations.append("✅ Excellent savings rate projected. Consider increasing investments.")
        
        # Check deficit periods
        deficit_periods = budget_analysis[budget_analysis['surplus_deficit'] < 0]
        
        if not deficit_periods.empty:
            recommendations.append(f"⚠️ Budget deficit expected in {len(deficit_periods)} periods. Plan accordingly.")
        
        # Check trend
        if budget_analysis['surplus_deficit'].iloc[-1] < budget_analysis['surplus_deficit'].iloc[0]:
            recommendations.append("📉 Financial position declining over time. Review budget allocation.")
        else:
            recommendations.append("📈 Financial position improving over time. Good trajectory!")
        
        return recommendations
