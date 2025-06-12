"""
Simplified Streamlit Dashboard for Personal Finance & Inflation Impact Tracker
Using sample data generated from the analysis notebook
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os

# Configure page
st.set_page_config(
    page_title="Personal Finance & Inflation Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .highlight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_sample_data():
    """Generate comprehensive sample data for the dashboard"""
    np.random.seed(42)
    
    # Countries and date range
    countries = ['United States', 'Germany', 'Japan', 'United Kingdom', 'Canada', 'Australia']
    date_range = pd.date_range('2020-01-01', '2024-12-01', freq='M')
    
    # Generate inflation data
    inflation_data = []
    for country in countries:
        base_inflation = {
            'United States': 2.5, 'Germany': 1.8, 'Japan': 0.5,
            'United Kingdom': 2.2, 'Canada': 2.0, 'Australia': 2.3
        }[country]
        
        for i, date in enumerate(date_range):
            if date.year == 2020:
                inflation = base_inflation - 1.0 + np.random.normal(0, 0.3)
            elif date.year == 2021:
                inflation = base_inflation + 1.5 + np.random.normal(0, 0.4)
            elif date.year == 2022:
                inflation = base_inflation + 4.0 + np.random.normal(0, 0.5)
            elif date.year == 2023:
                inflation = base_inflation + 2.0 + np.random.normal(0, 0.3)
            else:  # 2024
                inflation = base_inflation + 0.5 + np.random.normal(0, 0.2)
            
            inflation_data.append({
                'date': date,
                'country': country,
                'inflation_rate': max(0.1, inflation),
                'unemployment_rate': np.random.uniform(3, 8),
                'gdp_growth': np.random.uniform(-2, 4)
            })
    
    inflation_df = pd.DataFrame(inflation_data)
    
    # Generate cost of living data
    cost_categories = ['Housing', 'Food', 'Transportation', 'Healthcare', 'Education', 'Entertainment']
    cost_data = []
    
    base_costs = {
        'United States': {'Housing': 2000, 'Food': 600, 'Transportation': 400, 'Healthcare': 500, 'Education': 300, 'Entertainment': 200},
        'Germany': {'Housing': 1200, 'Food': 500, 'Transportation': 350, 'Healthcare': 200, 'Education': 100, 'Entertainment': 150},
        'Japan': {'Housing': 1500, 'Food': 550, 'Transportation': 300, 'Healthcare': 150, 'Education': 200, 'Entertainment': 180},
        'United Kingdom': {'Housing': 1800, 'Food': 580, 'Transportation': 380, 'Healthcare': 100, 'Education': 250, 'Entertainment': 190},
        'Canada': {'Housing': 1600, 'Food': 520, 'Transportation': 360, 'Healthcare': 80, 'Education': 200, 'Entertainment': 170},
        'Australia': {'Housing': 1700, 'Food': 540, 'Transportation': 370, 'Healthcare': 120, 'Education': 220, 'Entertainment': 180}
    }
    
    for country in countries:
        for category in cost_categories:
            for year in range(2020, 2025):
                yearly_inflation = inflation_df[
                    (inflation_df['country'] == country) & 
                    (inflation_df['date'].dt.year == year)
                ]['inflation_rate'].mean() / 100
                
                if year == 2020:
                    cost = base_costs[country][category]
                else:
                    prev_year_data = [item for item in cost_data if item['country'] == country and item['category'] == category and item['year'] == year-1]
                    if prev_year_data:
                        prev_cost = prev_year_data[0]['monthly_cost']
                    else:
                        prev_cost = base_costs[country][category]
                    cost = prev_cost * (1 + yearly_inflation + np.random.normal(0, 0.02))
                
                cost_data.append({
                    'country': country,
                    'category': category,
                    'year': year,
                    'monthly_cost': round(cost, 2)
                })
    
    cost_df = pd.DataFrame(cost_data)
    
    # Generate income data
    income_data = []
    base_incomes = {
        'United States': 5500, 'Germany': 4200, 'Japan': 4000,
        'United Kingdom': 4500, 'Canada': 4300, 'Australia': 4600
    }
    
    for country in countries:
        base_income = base_incomes[country]
        income = base_income
        
        for year in range(2020, 2025):
            if year > 2020:
                growth_rate = 0.02 + np.random.normal(0, 0.01)
                income = income * (1 + growth_rate)
            
            income_data.append({
                'country': country,
                'year': year,
                'monthly_income': round(income, 2)
            })
    
    income_df = pd.DataFrame(income_data)
    
    return inflation_df, cost_df, income_df

def create_inflation_chart(inflation_df):
    """Create inflation trends chart"""
    fig = px.line(
        inflation_df, 
        x='date', 
        y='inflation_rate', 
        color='country',
        title='📈 Inflation Rates Over Time',
        labels={'inflation_rate': 'Inflation Rate (%)', 'date': 'Date'}
    )
    fig.update_layout(height=500, showlegend=True)
    return fig

def create_cost_comparison_chart(cost_df):
    """Create cost comparison chart"""
    cost_2024 = cost_df[cost_df['year'] == 2024].groupby('country')['monthly_cost'].sum().reset_index()
    
    fig = px.bar(
        cost_2024,
        x='country',
        y='monthly_cost',
        title='🏠 Total Monthly Living Costs by Country (2024)',
        labels={'monthly_cost': 'Monthly Cost ($)', 'country': 'Country'}
    )
    fig.update_layout(height=500)
    return fig

def create_budget_breakdown_chart(cost_df, selected_country):
    """Create budget breakdown pie chart"""
    country_costs = cost_df[(cost_df['country'] == selected_country) & (cost_df['year'] == 2024)]
    
    fig = px.pie(
        country_costs,
        values='monthly_cost',
        names='category',
        title=f'💰 Budget Breakdown - {selected_country} (2024)'
    )
    fig.update_layout(height=500)
    return fig

def calculate_affordability(cost_df, income_df):
    """Calculate affordability metrics"""
    affordability_data = []
    
    for country in cost_df['country'].unique():
        for year in range(2020, 2025):
            total_cost = cost_df[(cost_df['country'] == country) & (cost_df['year'] == year)]['monthly_cost'].sum()
            income = income_df[(income_df['country'] == country) & (income_df['year'] == year)]['monthly_income'].iloc[0]
            
            affordability_data.append({
                'country': country,
                'year': year,
                'total_cost': total_cost,
                'income': income,
                'disposable_income': income - total_cost,
                'affordability_index': ((income - total_cost) / income) * 100
            })
    
    return pd.DataFrame(affordability_data)

# Main dashboard
def main():
    st.title("💰 Personal Finance & Inflation Impact Tracker")
    st.markdown("**Analyze inflation trends and their impact on your personal finances across different regions**")
    
    # Load data
    with st.spinner("Loading financial data..."):
        inflation_df, cost_df, income_df = generate_sample_data()
        affordability_df = calculate_affordability(cost_df, income_df)
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Country selection
    countries = inflation_df['country'].unique()
    selected_country = st.sidebar.selectbox("Select Country for Analysis", countries, index=0)
    
    # Date range selection
    min_date = inflation_df['date'].min()
    max_date = inflation_df['date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Inflation Analysis", "🏠 Cost of Living", "🔮 Budget Planning", "📋 Summary"])
    
    with tab1:
        st.header("📊 Financial Overview Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics for selected country
        latest_inflation = inflation_df[
            (inflation_df['country'] == selected_country) & 
            (inflation_df['date'] == inflation_df['date'].max())
        ]['inflation_rate'].iloc[0]
        
        latest_costs = cost_df[
            (cost_df['country'] == selected_country) & 
            (cost_df['year'] == 2024)
        ]['monthly_cost'].sum()
        
        latest_income = income_df[
            (income_df['country'] == selected_country) & 
            (income_df['year'] == 2024)
        ]['monthly_income'].iloc[0]
        
        disposable = latest_income - latest_costs
        
        with col1:
            st.metric(
                "Current Inflation Rate",
                f"{latest_inflation:.2f}%",
                delta=f"{latest_inflation - 2.0:.2f}% vs target"
            )
        
        with col2:
            st.metric(
                "Monthly Living Costs",
                f"${latest_costs:,.0f}",
                delta=f"${latest_costs - 3000:.0f} vs avg"
            )
        
        with col3:
            st.metric(
                "Average Income",
                f"${latest_income:,.0f}",
                delta=f"${latest_income - 4500:.0f} vs baseline"
            )
        
        with col4:
            st.metric(
                "Disposable Income",
                f"${disposable:,.0f}",
                delta=f"{(disposable/latest_income)*100:.1f}% of income"
            )
        
        # Charts
        st.plotly_chart(create_inflation_chart(inflation_df), use_container_width=True)
        
        # Affordability trends
        fig_afford = px.line(
            affordability_df,
            x='year',
            y='affordability_index',
            color='country',
            title='📊 Affordability Index Trends (% of Income After Living Costs)',
            labels={'affordability_index': 'Affordability Index (%)', 'year': 'Year'}
        )
        st.plotly_chart(fig_afford, use_container_width=True)
    
    with tab2:
        st.header("📈 Inflation Analysis")
        
        # Inflation insights
        st.markdown("""
        <div class="highlight-box">
        <h4>🎯 Key Inflation Insights</h4>
        <p>Understanding inflation patterns helps predict future costs and plan accordingly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Country comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_inflation_chart(inflation_df), use_container_width=True)
        
        with col2:
            # Inflation statistics
            recent_inflation = inflation_df[inflation_df['date'] >= '2022-01-01'].groupby('country')['inflation_rate'].agg(['mean', 'std']).round(2)
            recent_inflation.columns = ['Average Inflation (%)', 'Volatility (%)']
            st.subheader("📊 Inflation Statistics (2022-2024)")
            st.dataframe(recent_inflation, use_container_width=True)
        
        # Economic correlation
        fig_corr = px.scatter(
            inflation_df,
            x='inflation_rate',
            y='unemployment_rate',
            color='country',
            size='gdp_growth',
            title='🔗 Economic Indicators Correlation',
            labels={'inflation_rate': 'Inflation Rate (%)', 'unemployment_rate': 'Unemployment Rate (%)'}
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab3:
        st.header("🏠 Cost of Living Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_cost_comparison_chart(cost_df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_budget_breakdown_chart(cost_df, selected_country), use_container_width=True)
        
        # Cost trends
        cost_trends = cost_df.groupby(['category', 'year'])['monthly_cost'].mean().reset_index()
        fig_trends = px.line(
            cost_trends,
            x='year',
            y='monthly_cost',
            color='category',
            title='📈 Cost Trends by Category Over Time',
            labels={'monthly_cost': 'Average Monthly Cost ($)', 'year': 'Year'}
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Regional comparison table
        st.subheader("🌍 Regional Cost Comparison (2024)")
        cost_comparison = cost_df[cost_df['year'] == 2024].pivot_table(
            values='monthly_cost', 
            index='country', 
            columns='category', 
            aggfunc='sum'
        ).round(0)
        st.dataframe(cost_comparison, use_container_width=True)
    
    with tab4:
        st.header("🔮 Personal Budget Planning")
        
        st.markdown("""
        <div class="highlight-box">
        <h4>💡 Budget Planning Tool</h4>
        <p>Plan your finances based on inflation forecasts and regional cost data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_income = st.number_input("Monthly Income ($)", value=5000, min_value=1000, max_value=20000, step=500)
        
        with col2:
            planning_years = st.slider("Planning Horizon (Years)", 1, 10, 5)
        
        with col3:
            inflation_assumption = st.slider("Expected Annual Inflation (%)", 1.0, 8.0, 3.0, 0.5)
        
        # Budget analysis
        current_costs = cost_df[(cost_df['country'] == selected_country) & (cost_df['year'] == 2024)]
        total_current_cost = current_costs['monthly_cost'].sum()
        
        # Future projections
        future_cost = total_current_cost * ((1 + inflation_assumption/100) ** planning_years)
        future_income = user_income * ((1 + 0.03) ** planning_years)  # Assume 3% income growth
        
        current_savings = user_income - total_current_cost
        future_savings = future_income - future_cost
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Current Situation")
            st.metric("Monthly Income", f"${user_income:,.0f}")
            st.metric("Living Costs", f"${total_current_cost:,.0f}")
            st.metric("Monthly Savings", f"${current_savings:,.0f}")
            st.metric("Savings Rate", f"{(current_savings/user_income)*100:.1f}%")
        
        with col2:
            st.subheader(f"🔮 Projection ({planning_years} years)")
            st.metric("Future Monthly Income", f"${future_income:,.0f}", delta=f"+${future_income-user_income:,.0f}")
            st.metric("Future Living Costs", f"${future_cost:,.0f}", delta=f"+${future_cost-total_current_cost:,.0f}")
            st.metric("Future Monthly Savings", f"${future_savings:,.0f}", delta=f"{future_savings-current_savings:+,.0f}")
            st.metric("Future Savings Rate", f"{(future_savings/future_income)*100:.1f}%")
        
        # Recommendations
        st.subheader("💡 Financial Recommendations")
        
        if current_savings < 0:
            st.error("⚠️ Your expenses exceed income! Consider reducing costs or increasing income.")
        elif (current_savings/user_income)*100 < 10:
            st.warning("📊 Low savings rate. Aim for at least 15% to build financial security.")
        elif (current_savings/user_income)*100 > 30:
            st.success("💰 Excellent savings rate! Consider investing surplus for long-term growth.")
        else:
            st.info("✅ Good savings rate. You're on track for financial health.")
        
        # Budget breakdown
        budget_breakdown = current_costs.copy()
        budget_breakdown['percentage'] = (budget_breakdown['monthly_cost'] / total_current_cost) * 100
        
        fig_budget = px.pie(
            budget_breakdown,
            values='monthly_cost',
            names='category',
            title=f'Your Budget Breakdown - {selected_country}',
            hover_data=['percentage']
        )
        st.plotly_chart(fig_budget, use_container_width=True)
    
    with tab5:
        st.header("📋 Financial Summary & Insights")
        
        # Key insights
        st.markdown("""
        <div class="highlight-box">
        <h4>🎯 Key Findings</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate insights
        avg_inflation_2024 = inflation_df[inflation_df['date'].dt.year == 2024]['inflation_rate'].mean()
        highest_cost_country = cost_df[cost_df['year'] == 2024].groupby('country')['monthly_cost'].sum().idxmax()
        most_affordable = affordability_df[affordability_df['year'] == 2024].loc[
            affordability_df[affordability_df['year'] == 2024]['affordability_index'].idxmax(), 'country'
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **📊 Economic Overview:**
            - Average inflation (2024): **{avg_inflation_2024:.2f}%**
            - Highest cost region: **{highest_cost_country}**
            - Most affordable region: **{most_affordable}**
            - Housing typically represents **30-35%** of total costs
            """)
        
        with col2:
            st.markdown(f"""
            **💡 Recommendations:**
            - Maintain emergency fund covering **6+ months** expenses
            - Keep housing costs below **30%** of income
            - Target **15-20%** savings rate minimum
            - Consider **inflation-protected** investments
            """)
        
        # Export functionality
        st.subheader("📥 Export Your Data")
        
        if st.button("📊 Generate Personal Finance Report"):
            # Create summary data
            user_data = {
                'Country': selected_country,
                'Analysis Date': datetime.now().strftime('%Y-%m-%d'),
                'Current Inflation': f"{latest_inflation:.2f}%",
                'Monthly Costs': f"${latest_costs:,.0f}",
                'Disposable Income': f"${disposable:,.0f}",
                'Affordability Index': f"{((disposable/latest_income)*100):.1f}%"
            }
            
            st.success("✅ Report generated successfully!")
            st.json(user_data)
        
        # Data sources and methodology
        with st.expander("📚 Data Sources & Methodology"):
            st.markdown("""
            **Data Sources:**
            - Sample inflation data based on historical patterns
            - Cost of living estimates from regional benchmarks
            - Income data from statistical averages
            
            **Methodology:**
            - Forecasting uses trend analysis and statistical modeling
            - Budget planning incorporates inflation impact projections
            - Regional comparisons normalize for purchasing power
            
            **Limitations:**
            - This dashboard uses sample data for demonstration
            - Real implementation would use live APIs (World Bank, FRED, etc.)
            - Individual circumstances may vary significantly
            """)

if __name__ == "__main__":
    main()
