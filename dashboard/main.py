"""
Main Streamlit Dashboard for Personal Finance & Inflation Impact Tracker
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import custom modules
from data_collection.collectors import DataCollector, RealTimeDataCollector
from preprocessing.data_processing import DataPreprocessor, FeatureEngineer
from forecasting.models import InflationForecaster, CostPredictor, PersonalBudgetForecaster
from visualization.charts import FinanceVisualizer, DashboardComponents
from config.config import Config, REGIONS, BUDGET_CATEGORIES

# Configure page
st.set_page_config(
    page_title="Personal Finance & Inflation Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all components with caching"""
    Config.create_directories()
    return {
        'data_collector': DataCollector(),
        'realtime_collector': RealTimeDataCollector(),
        'preprocessor': DataPreprocessor(),
        'feature_engineer': FeatureEngineer(),
        'inflation_forecaster': InflationForecaster(),
        'cost_predictor': CostPredictor(),
        'budget_forecaster': PersonalBudgetForecaster(),
        'visualizer': FinanceVisualizer(),
        'dashboard_components': DashboardComponents()
    }

def load_sample_data():
    """Load sample data for demonstration"""
    # Generate sample inflation data
    dates = pd.date_range(start='2015-01-01', end='2023-12-31', freq='M')
    countries = ['United States', 'United Kingdom', 'Germany', 'France', 'Japan']
    
    inflation_data = []
    for country in countries:
        base_rate = np.random.uniform(1, 4)  # Base inflation rate
        for date in dates:
            # Add some seasonality and trend
            seasonal = 0.5 * np.sin(2 * np.pi * date.month / 12)
            trend = 0.01 * (date.year - 2015)
            noise = np.random.normal(0, 0.5)
            
            rate = base_rate + seasonal + trend + noise
            inflation_data.append({
                'date': date,
                'country': country,
                'value': max(0, rate)  # Ensure non-negative
            })
    
    return pd.DataFrame(inflation_data)

def load_sample_cost_data():
    """Load sample cost of living data"""
    cities_data = {
        'city': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Toronto', 'Mumbai', 'Shanghai'],
        'country': ['United States', 'United Kingdom', 'France', 'Japan', 'Australia', 'Canada', 'India', 'China'],
        'rent_1br_city_center': [3000, 2500, 1800, 1500, 2200, 1800, 800, 1200],
        'rent_1br_outside_center': [2200, 1800, 1300, 1000, 1600, 1300, 500, 800],
        'meal_inexpensive_restaurant': [20, 18, 15, 10, 25, 15, 5, 8],
        'transportation_monthly': [120, 150, 75, 80, 130, 110, 30, 50],
        'utilities_basic': [150, 200, 180, 120, 180, 150, 50, 80],
        'cost_of_living_index': [85, 78, 72, 68, 75, 70, 35, 45]
    }
    
    return pd.DataFrame(cities_data)

def main():
    """Main dashboard function"""
    
    # Initialize components
    components = initialize_components()
    
    # Sidebar configuration
    st.sidebar.title("🎯 Configuration")
    
    # User inputs
    st.sidebar.header("Personal Information")
    user_income = st.sidebar.number_input("Annual Income ($)", 
                                         min_value=20000, 
                                         max_value=500000, 
                                         value=75000, 
                                         step=5000)
    
    user_age = st.sidebar.slider("Age", min_value=18, max_value=70, value=30)
    
    family_size = st.sidebar.selectbox("Family Size", [1, 2, 3, 4, 5], index=1)
    
    location_type = st.sidebar.selectbox("Location Type", 
                                       ["Urban", "Suburban", "Rural"], 
                                       index=0)
    
    selected_country = st.sidebar.selectbox("Country", 
                                          REGIONS['countries'], 
                                          index=0)
    
    # Dashboard title
    st.title("💰 Personal Finance & Inflation Impact Tracker")
    st.markdown("### Advanced Analytics for Financial Planning")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Inflation Analysis", 
        "🏙️ Cost of Living", 
        "🔮 Forecasting", 
        "💡 Budget Planner"
    ])
    
    # Load sample data
    inflation_data = load_sample_data()
    cost_data = load_sample_cost_data()
    
    with tab1:
        st.header("📊 Financial Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate some sample metrics
        current_inflation = 3.2  # Sample current inflation rate
        real_income = user_income / (1 + current_inflation/100)
        purchasing_power_loss = ((user_income - real_income) / user_income) * 100
        
        with col1:
            st.metric(
                label="Annual Income",
                value=f"${user_income:,.0f}",
                delta=f"+{user_income*0.03:,.0f} (3% growth)"
            )
        
        with col2:
            st.metric(
                label="Real Income (Inflation-Adjusted)",
                value=f"${real_income:,.0f}",
                delta=f"-{user_income-real_income:,.0f}"
            )
        
        with col3:
            st.metric(
                label="Current Inflation Rate",
                value=f"{current_inflation}%",
                delta="0.2%"
            )
        
        with col4:
            st.metric(
                label="Purchasing Power Loss",
                value=f"{purchasing_power_loss:.1f}%",
                delta=None
            )
        
        # Personal spending profile
        st.subheader("🎯 Your Spending Profile")
        
        spending_profile = components['feature_engineer'].create_spending_profile(
            income=user_income,
            age=user_age,
            location_type=location_type.lower()
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Budget breakdown chart
            budget_chart = components['visualizer'].plot_budget_breakdown(
                spending_profile,
                "Recommended Budget Allocation"
            )
            st.plotly_chart(budget_chart, use_container_width=True)
        
        with col2:
            # Display spending recommendations
            st.subheader("💡 Spending Recommendations")
            for category, amount in spending_profile.items():
                percentage = (amount / user_income) * 100
                st.write(f"**{category}**: ${amount:,.0f} ({percentage:.1f}%)")
            
            # Demographic insights
            demo_features = components['feature_engineer'].create_demographic_features(
                age=user_age,
                income=user_income,
                family_size=family_size
            )
            
            st.subheader("📋 Your Profile")
            st.write(f"**Age Group**: {demo_features['age_group']}")
            st.write(f"**Income Bracket**: {demo_features['income_bracket']}")
            st.write(f"**Per Capita Income**: ${demo_features['per_capita_income']:,.0f}")
    
    with tab2:
        st.header("📈 Inflation Analysis")
        
        # Inflation trends
        selected_countries = st.multiselect(
            "Select Countries for Comparison",
            REGIONS['countries'],
            default=['United States', 'United Kingdom', 'Germany']
        )
        
        if selected_countries:
            # Filter data for selected countries
            filtered_data = inflation_data[inflation_data['country'].isin(selected_countries)]
            
            # Create inflation trends chart
            inflation_chart = components['visualizer'].plot_inflation_trends(
                filtered_data,
                selected_countries,
                "Inflation Trends Comparison"
            )
            st.plotly_chart(inflation_chart, use_container_width=True)
            
            # Real vs nominal income analysis
            st.subheader("💵 Real vs Nominal Income Impact")
            
            # Calculate real income over time for selected country
            if selected_country in selected_countries:
                country_data = filtered_data[filtered_data['country'] == selected_country].copy()
                
                # Generate income data
                country_data['nominal_income'] = user_income
                country_data['real_income'] = components['preprocessor'].calculate_real_income(
                    user_income, country_data, base_year=2020
                )['real_income']
                
                real_income_chart = components['visualizer'].plot_real_vs_nominal_income(
                    country_data,
                    f"Income Impact Analysis - {selected_country}"
                )
                st.plotly_chart(real_income_chart, use_container_width=True)
        
        # Regional inflation summary
        st.subheader("🌍 Regional Inflation Summary")
        summary_data = inflation_data.groupby('country').agg({
            'value': ['mean', 'std', 'min', 'max']
        }).round(2)
        summary_data.columns = ['Average', 'Std Dev', 'Minimum', 'Maximum']
        st.dataframe(summary_data, use_container_width=True)
    
    with tab3:
        st.header("🏙️ Cost of Living Analysis")
        
        # Cost of living comparison
        cost_chart = components['visualizer'].plot_cost_of_living_comparison(
            cost_data,
            "Cost of Living Index by City"
        )
        st.plotly_chart(cost_chart, use_container_width=True)
        
        # Detailed cost breakdown
        st.subheader("💰 Detailed Cost Breakdown")
        
        selected_cities = st.multiselect(
            "Select Cities for Detailed Comparison",
            cost_data['city'].tolist(),
            default=['New York', 'London', 'Tokyo']
        )
        
        if selected_cities:
            filtered_cost_data = cost_data[cost_data['city'].isin(selected_cities)]
            
            # Display detailed comparison table
            comparison_columns = [
                'city', 'country', 'rent_1br_city_center', 'rent_1br_outside_center',
                'meal_inexpensive_restaurant', 'transportation_monthly', 'utilities_basic'
            ]
            
            comparison_table = filtered_cost_data[comparison_columns].copy()
            comparison_table.columns = [
                'City', 'Country', 'Rent (City Center)', 'Rent (Outside)',
                'Restaurant Meal', 'Transportation', 'Utilities'
            ]
            
            st.dataframe(comparison_table, use_container_width=True)
            
            # Affordability analysis
            st.subheader("🎯 Affordability for Your Income")
            
            for city in selected_cities:
                city_data = cost_data[cost_data['city'] == city].iloc[0]
                monthly_costs = (
                    city_data['rent_1br_city_center'] +
                    city_data['meal_inexpensive_restaurant'] * 30 +
                    city_data['transportation_monthly'] +
                    city_data['utilities_basic']
                )
                annual_costs = monthly_costs * 12
                affordability_ratio = (annual_costs / user_income) * 100
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"{city} - Monthly Costs", f"${monthly_costs:,.0f}")
                with col2:
                    st.metric(f"{city} - Annual Costs", f"${annual_costs:,.0f}")
                with col3:
                    color = "red" if affordability_ratio > 50 else "orange" if affordability_ratio > 30 else "green"
                    st.metric(f"{city} - % of Income", f"{affordability_ratio:.1f}%")
    
    with tab4:
        st.header("🔮 Financial Forecasting")
        
        # Forecasting parameters
        col1, col2 = st.columns(2)
        
        with col1:
            forecast_periods = st.slider("Forecast Periods (Months)", 6, 60, 24)
            income_growth_rate = st.slider("Expected Income Growth Rate (%)", 0.0, 10.0, 3.0) / 100
        
        with col2:
            inflation_scenario = st.selectbox(
                "Inflation Scenario",
                ["Conservative (2-3%)", "Moderate (3-5%)", "High (5-7%)"]
            )
        
        # Generate sample forecast data
        if st.button("Generate Forecast", type="primary"):
            with st.spinner("Generating forecasts..."):
                # Create sample forecast data
                future_dates = pd.date_range(
                    start=datetime.now(),
                    periods=forecast_periods,
                    freq='M'
                )
                
                # Sample inflation forecast based on scenario
                if "Conservative" in inflation_scenario:
                    base_inflation = 2.5
                elif "Moderate" in inflation_scenario:
                    base_inflation = 4.0
                else:
                    base_inflation = 6.0
                
                forecast_values = []
                for i in range(forecast_periods):
                    # Add some random variation
                    variation = np.random.normal(0, 0.3)
                    seasonal = 0.2 * np.sin(2 * np.pi * i / 12)
                    value = base_inflation + variation + seasonal
                    forecast_values.append(max(0, value))
                
                forecast_df = pd.DataFrame({
                    'forecast': forecast_values,
                    'lower_ci': [v - 1 for v in forecast_values],
                    'upper_ci': [v + 1 for v in forecast_values]
                })
                
                # Historical data for chart
                historical_df = inflation_data[
                    inflation_data['country'] == selected_country
                ].tail(36)  # Last 3 years
                
                # Create forecast chart
                forecast_chart = components['visualizer'].plot_forecast_results(
                    historical_df,
                    forecast_df,
                    f"Inflation Forecast - {inflation_scenario}"
                )
                st.plotly_chart(forecast_chart, use_container_width=True)
                
                # Budget impact forecast
                st.subheader("💰 Budget Impact Forecast")
                
                budget_results = components['budget_forecaster'].forecast_budget_needs(
                    current_income=user_income,
                    current_expenses=spending_profile,
                    inflation_forecast=forecast_df,
                    income_growth_rate=income_growth_rate
                )
                
                if budget_results:
                    budget_chart = components['visualizer'].plot_budget_forecast(
                        budget_results['budget_analysis'],
                        "Personal Budget Forecast"
                    )
                    st.plotly_chart(budget_chart, use_container_width=True)
                    
                    # Display recommendations
                    st.subheader("💡 Forecast Recommendations")
                    for recommendation in budget_results.get('recommendations', []):
                        st.write(f"• {recommendation}")
    
    with tab5:
        st.header("💡 Personalized Budget Planner")
        
        st.subheader("🎯 Smart Budget Recommendations")
        
        # Current vs recommended comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Current Budget Input")
            current_expenses = {}
            
            for category in BUDGET_CATEGORIES.keys():
                if category != 'Savings':
                    current_expenses[category] = st.number_input(
                        f"Monthly {category} ($)",
                        min_value=0,
                        value=int(spending_profile[category] / 12),
                        step=50,
                        key=f"current_{category}"
                    )
            
            total_expenses = sum(current_expenses.values())
            monthly_income = user_income / 12
            monthly_savings = monthly_income - total_expenses
            
            st.metric("Monthly Income", f"${monthly_income:,.0f}")
            st.metric("Total Monthly Expenses", f"${total_expenses:,.0f}")
            st.metric("Available for Savings", f"${monthly_savings:,.0f}")
        
        with col2:
            st.subheader("🎯 Recommended Allocation")
            
            # Show recommended vs actual
            comparison_data = []
            for category, current_amount in current_expenses.items():
                recommended_monthly = spending_profile[category] / 12
                difference = current_amount - recommended_monthly
                
                comparison_data.append({
                    'Category': category,
                    'Current': current_amount,
                    'Recommended': recommended_monthly,
                    'Difference': difference,
                    'Status': '✅' if abs(difference) < recommended_monthly * 0.1 else '⚠️'
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
        
        # Optimization suggestions
        st.subheader("🔧 Budget Optimization")
        
        if monthly_savings < monthly_income * 0.2:  # Less than 20% savings
            st.warning("⚠️ Low savings rate! Consider these optimizations:")
            
            # Find categories that are over budget
            over_budget = comparison_df[comparison_df['Difference'] > 0]
            
            if not over_budget.empty:
                st.write("**Categories over recommended budget:**")
                for _, row in over_budget.iterrows():
                    st.write(f"• **{row['Category']}**: ${row['Difference']:,.0f} over budget")
                    
                    # Specific suggestions
                    if row['Category'] == 'Housing':
                        st.write("  - Consider a smaller place or additional roommates")
                        st.write("  - Look into areas with lower rent")
                    elif row['Category'] == 'Food':
                        st.write("  - Cook more meals at home")
                        st.write("  - Use meal planning and bulk shopping")
                    elif row['Category'] == 'Transportation':
                        st.write("  - Use public transportation more")
                        st.write("  - Consider carpooling or ridesharing")
                    elif row['Category'] == 'Entertainment':
                        st.write("  - Look for free or low-cost activities")
                        st.write("  - Set a monthly entertainment budget")
        else:
            st.success("✅ Great savings rate! You're on track for financial success!")
        
        # Scenario planning
        st.subheader("🎲 What-If Scenarios")
        
        scenario_col1, scenario_col2 = st.columns(2)
        
        with scenario_col1:
            income_change = st.slider("Income Change (%)", -50, 50, 0)
            inflation_impact = st.slider("Additional Inflation (%)", 0, 10, 0)
        
        with scenario_col2:
            adjusted_income = user_income * (1 + income_change/100)
            adjusted_expenses = total_expenses * 12 * (1 + inflation_impact/100)
            adjusted_savings = adjusted_income - adjusted_expenses
            savings_rate = (adjusted_savings / adjusted_income) * 100 if adjusted_income > 0 else 0
            
            st.metric("Adjusted Annual Income", f"${adjusted_income:,.0f}")
            st.metric("Adjusted Annual Expenses", f"${adjusted_expenses:,.0f}")
            st.metric("Adjusted Annual Savings", f"${adjusted_savings:,.0f}")
            st.metric("Adjusted Savings Rate", f"{savings_rate:.1f}%")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Personal Finance & Inflation Impact Tracker** - "
        "Advanced analytics for smarter financial decisions. "
        "Built with Python, Streamlit, and machine learning."
    )

if __name__ == "__main__":
    main()
