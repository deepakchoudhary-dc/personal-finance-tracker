"""
Advanced visualization module for Finance Tracker
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import seaborn as sns
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

class FinanceVisualizer:
    """Advanced visualization class for financial data"""
    
    def __init__(self):
        # Set default plotly theme
        self.theme = 'plotly_white'
        self.color_palette = px.colors.qualitative.Set3
        
    def plot_inflation_trends(self, 
                            df: pd.DataFrame,
                            countries: List[str] = None,
                            title: str = "Inflation Trends Over Time") -> go.Figure:
        """
        Create interactive inflation trends plot
        
        Args:
            df: Inflation data
            countries: List of countries to plot
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive plot
        """
        try:
            fig = go.Figure()
            
            if countries is None:
                countries = df['country'].unique()[:5]  # Limit to 5 countries
            
            for i, country in enumerate(countries):
                country_data = df[df['country'] == country]
                
                if not country_data.empty:
                    fig.add_trace(go.Scatter(
                        x=country_data['date'],
                        y=country_data['value'],
                        mode='lines+markers',
                        name=country,
                        line=dict(width=3),
                        marker=dict(size=6),
                        hovertemplate=f'<b>{country}</b><br>' +
                                    'Date: %{x}<br>' +
                                    'Inflation Rate: %{y:.2f}%<br>' +
                                    '<extra></extra>'
                    ))
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                xaxis_title="Date",
                yaxis_title="Inflation Rate (%)",
                template=self.theme,
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                height=600
            )
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating inflation trends plot: {str(e)}")
            return go.Figure()
    
    def plot_real_vs_nominal_income(self, 
                                  income_data: pd.DataFrame,
                                  title: str = "Real vs Nominal Income") -> go.Figure:
        """
        Plot real vs nominal income comparison
        
        Args:
            income_data: DataFrame with real and nominal income data
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive plot
        """
        try:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Income Comparison', 'Purchasing Power Loss'),
                vertical_spacing=0.12
            )
            
            # Income comparison
            fig.add_trace(
                go.Scatter(
                    x=income_data['date'],
                    y=income_data['nominal_income'],
                    mode='lines+markers',
                    name='Nominal Income',
                    line=dict(color='blue', width=3),
                    hovertemplate='Nominal Income: $%{y:,.0f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=income_data['date'],
                    y=income_data['real_income'],
                    mode='lines+markers',
                    name='Real Income (Inflation-Adjusted)',
                    line=dict(color='red', width=3),
                    hovertemplate='Real Income: $%{y:,.0f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Purchasing power loss
            purchasing_power_loss = ((income_data['nominal_income'] - income_data['real_income']) / 
                                   income_data['nominal_income']) * 100
            
            fig.add_trace(
                go.Scatter(
                    x=income_data['date'],
                    y=purchasing_power_loss,
                    mode='lines+markers',
                    name='Purchasing Power Loss (%)',
                    line=dict(color='orange', width=3),
                    fill='tonexty',
                    hovertemplate='Power Loss: %{y:.1f}%<extra></extra>'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                template=self.theme,
                height=700,
                showlegend=True
            )
            
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Income ($)", row=1, col=1)
            fig.update_yaxes(title_text="Loss (%)", row=2, col=1)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating real vs nominal income plot: {str(e)}")
            return go.Figure()
    
    def plot_cost_of_living_comparison(self, 
                                     cost_data: pd.DataFrame,
                                     title: str = "Cost of Living Comparison") -> go.Figure:
        """
        Create cost of living comparison chart
        
        Args:
            cost_data: Cost of living data by city
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive plot
        """
        try:
            # Create horizontal bar chart
            fig = go.Figure()
            
            cities = cost_data['city'].tolist()
            indices = cost_data['cost_of_living_index'].tolist()
            
            fig.add_trace(go.Bar(
                y=cities,
                x=indices,
                orientation='h',
                marker=dict(
                    color=indices,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Cost Index")
                ),
                text=[f'{idx:.1f}' for idx in indices],
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>' +
                            'Cost Index: %{x:.1f}<br>' +
                            '<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                xaxis_title="Cost of Living Index",
                yaxis_title="City",
                template=self.theme,
                height=max(400, len(cities) * 30),
                margin=dict(l=150)
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating cost of living comparison: {str(e)}")
            return go.Figure()
    
    def plot_budget_breakdown(self, 
                            budget_data: Dict[str, float],
                            title: str = "Budget Breakdown") -> go.Figure:
        """
        Create interactive pie chart for budget breakdown
        
        Args:
            budget_data: Dictionary of budget categories and amounts
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive pie chart
        """
        try:
            categories = list(budget_data.keys())
            values = list(budget_data.values())
            
            # Calculate percentages
            total = sum(values)
            percentages = [v/total*100 for v in values]
            
            fig = go.Figure(data=[go.Pie(
                labels=categories,
                values=values,
                hole=0.4,
                textinfo='label+percent',
                textposition='outside',
                marker=dict(
                    colors=self.color_palette[:len(categories)],
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>' +
                            'Amount: $%{value:,.0f}<br>' +
                            'Percentage: %{percent}<br>' +
                            '<extra></extra>'
            )])
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                template=self.theme,
                height=500,
                annotations=[dict(text=f'Total<br>${total:,.0f}', 
                                x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating budget breakdown: {str(e)}")
            return go.Figure()
    
    def plot_forecast_results(self, 
                            historical_data: pd.DataFrame,
                            forecast_data: pd.DataFrame,
                            title: str = "Inflation Forecast") -> go.Figure:
        """
        Plot historical data with forecast predictions
        
        Args:
            historical_data: Historical time series data
            forecast_data: Forecast predictions with confidence intervals
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive forecast plot
        """
        try:
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical_data['date'],
                y=historical_data['value'],
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='blue', width=3),
                marker=dict(size=6),
                hovertemplate='Historical: %{y:.2f}%<extra></extra>'
            ))
            
            # Forecast data
            if 'forecast' in forecast_data.columns:
                # Generate future dates
                last_date = historical_data['date'].max()
                future_dates = pd.date_range(
                    start=last_date + pd.DateOffset(months=1),
                    periods=len(forecast_data),
                    freq='M'
                )
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=forecast_data['forecast'],
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='red', width=3, dash='dash'),
                    marker=dict(size=6),
                    hovertemplate='Forecast: %{y:.2f}%<extra></extra>'
                ))
                
                # Confidence intervals
                if 'lower_ci' in forecast_data.columns and 'upper_ci' in forecast_data.columns:
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=forecast_data['upper_ci'],
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=forecast_data['lower_ci'],
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(255, 0, 0, 0.2)',
                        name='Confidence Interval',
                        hovertemplate='CI: %{y:.2f}%<extra></extra>'
                    ))
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                xaxis_title="Date",
                yaxis_title="Rate (%)",
                template=self.theme,
                height=600,
                hovermode='x unified'
            )
            
            # Add vertical line at forecast start
            if not historical_data.empty:
                fig.add_vline(
                    x=historical_data['date'].max(),
                    line_dash="dash",
                    line_color="gray",
                    annotation_text="Forecast Start"
                )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating forecast plot: {str(e)}")
            return go.Figure()
    
    def plot_affordability_heatmap(self, 
                                  affordability_data: pd.DataFrame,
                                  title: str = "Regional Affordability Heatmap") -> go.Figure:
        """
        Create affordability heatmap
        
        Args:
            affordability_data: DataFrame with affordability scores by region
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive heatmap
        """
        try:
            # Pivot data for heatmap
            if 'country' in affordability_data.columns and 'city' in affordability_data.columns:
                heatmap_data = affordability_data.pivot(
                    index='country', 
                    columns='city', 
                    values='affordability_score_normalized'
                )
            else:
                # Fallback to simple visualization
                return self.plot_cost_of_living_comparison(affordability_data, title)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='RdYlGn',
                colorbar=dict(title="Affordability Score"),
                hovertemplate='<b>%{y} - %{x}</b><br>' +
                            'Score: %{z:.1f}<br>' +
                            '<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                xaxis_title="City",
                yaxis_title="Country",
                template=self.theme,
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating affordability heatmap: {str(e)}")
            return go.Figure()
    
    def plot_budget_forecast(self, 
                           budget_forecast: pd.DataFrame,
                           title: str = "Budget Forecast Analysis") -> go.Figure:
        """
        Plot budget forecast with income vs expenses
        
        Args:
            budget_forecast: Budget forecast data
            title: Plot title
            
        Returns:
            plotly.graph_objects.Figure: Interactive plot
        """
        try:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Income vs Expenses Forecast', 'Savings Rate Projection'),
                vertical_spacing=0.12
            )
            
            # Income vs Expenses
            fig.add_trace(
                go.Scatter(
                    x=budget_forecast['period'],
                    y=budget_forecast['predicted_income'],
                    mode='lines+markers',
                    name='Predicted Income',
                    line=dict(color='green', width=3),
                    hovertemplate='Income: $%{y:,.0f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=budget_forecast['period'],
                    y=budget_forecast['predicted_expenses'],
                    mode='lines+markers',
                    name='Predicted Expenses',
                    line=dict(color='red', width=3),
                    hovertemplate='Expenses: $%{y:,.0f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Savings Rate
            fig.add_trace(
                go.Scatter(
                    x=budget_forecast['period'],
                    y=budget_forecast['savings_rate'],
                    mode='lines+markers',
                    name='Savings Rate',
                    line=dict(color='blue', width=3),
                    fill='tonexty',
                    hovertemplate='Savings Rate: %{y:.1f}%<extra></extra>'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=dict(text=title, font=dict(size=20)),
                template=self.theme,
                height=700
            )
            
            fig.update_xaxes(title_text="Period (Months)", row=2, col=1)
            fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
            fig.update_yaxes(title_text="Savings Rate (%)", row=2, col=1)
            
            # Add target savings rate line
            fig.add_hline(y=20, line_dash="dash", line_color="orange", 
                         annotation_text="Target 20%", row=2, col=1)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating budget forecast plot: {str(e)}")
            return go.Figure()

class DashboardComponents:
    """Reusable dashboard components"""
    
    def __init__(self):
        self.visualizer = FinanceVisualizer()
    
    def create_metric_card(self, 
                          title: str, 
                          value: float, 
                          delta: float = None,
                          format_type: str = 'currency') -> Dict:
        """
        Create metric card data for dashboard
        
        Args:
            title: Metric title
            value: Current value
            delta: Change from previous period
            format_type: 'currency', 'percentage', or 'number'
            
        Returns:
            Dict: Metric card data
        """
        if format_type == 'currency':
            formatted_value = f"${value:,.0f}"
            delta_text = f"${delta:+,.0f}" if delta else ""
        elif format_type == 'percentage':
            formatted_value = f"{value:.1f}%"
            delta_text = f"{delta:+.1f}%" if delta else ""
        else:
            formatted_value = f"{value:,.0f}"
            delta_text = f"{delta:+,.0f}" if delta else ""
        
        delta_color = "green" if delta and delta > 0 else "red" if delta and delta < 0 else "gray"
        
        return {
            'title': title,
            'value': formatted_value,
            'delta': delta_text,
            'delta_color': delta_color
        }
    
    def create_summary_stats(self, data: pd.DataFrame) -> Dict:
        """
        Create summary statistics for dashboard
        
        Args:
            data: Input data
            
        Returns:
            Dict: Summary statistics
        """
        if data.empty:
            return {}
        
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        stats = {}
        for col in numeric_columns:
            stats[col] = {
                'mean': data[col].mean(),
                'median': data[col].median(),
                'std': data[col].std(),
                'min': data[col].min(),
                'max': data[col].max()
            }
        
        return stats
