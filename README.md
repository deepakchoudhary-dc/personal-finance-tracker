# 💰 Personal Finance & Inflation Impact Tracker

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B.svg)](https://share.streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Overview
A comprehensive real-time financial intelligence platform that analyzes how inflation affects cost of living and purchasing power across different regions. This advanced data science project provides live economic insights, predictive forecasting, and personalized budget planning using professional-grade APIs and machine learning models.

## ✨ Key Features
- **🌐 Real-time Data Integration**: Live inflation rates from World Bank API, FRED, and financial markets
- **📊 Interactive Dashboard**: Professional Streamlit web application with 5 comprehensive analysis tabs
- **🏠 Cost of Living Analysis**: Compare living costs between 190+ countries and major cities
- **💰 Real Income Calculator**: Inflation-adjusted purchasing power analysis with historical trends
- **🔮 AI-Powered Forecasting**: Machine learning models (Prophet, ARIMA, XGBoost) for future cost predictions
- **📈 Personal Budget Planner**: Customized financial recommendations based on location and demographics
- **🎯 Affordability Index**: Composite scoring system for optimal location selection
- **💱 Live Exchange Rates**: Real-time currency conversion and international cost comparisons

## 🛠️ Advanced Tech Stack
- **🌐 Real-time APIs**: World Bank API, FRED API, ExchangeRate-API, Economic data sources
- **📊 Data Science**: Python (Pandas, NumPy, SciPy), Advanced statistical analysis
- **🎨 Visualization**: Matplotlib, Seaborn, Interactive charts and real-time plots
- **🤖 Machine Learning**: Scikit-learn, Prophet, ARIMA, XGBoost for forecasting
- **🖥️ Web Application**: Streamlit with responsive design and real-time updates
- **⚡ Performance**: Smart caching, background data refresh, optimized API calls
- **🔒 Security**: Environment-based API key management, secure data handling

## 🎯 Live Demo Features
- **🌐 Live Demo**: [Deploy on Streamlit Cloud](https://share.streamlit.io) (See STREAMLIT_DEPLOYMENT.md)
- **📈 Real-time Inflation Dashboard**: Live API-powered economic data
- **🔄 Auto-refreshing Data**: Updates every hour with latest economic indicators
- **🌍 Global Coverage**: 190+ countries with live economic data
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 📁 Project Architecture
```
finance_tracker/
├── 📊 dashboard/                # Real-time Streamlit applications
│   ├── realtime_dashboard.py   # 🌐 Main API-powered dashboard
│   ├── working_dashboard.py    # 📈 Matplotlib-based dashboard
│   └── simple_dashboard.py     # 🎯 Basic demo version
├── 📁 data/                     # Data storage and management
│   ├── raw/                    # Raw API responses and datasets
│   ├── processed/              # Cleaned and processed data
│   └── external/               # External datasets and references
├── 🔧 src/                      # Core application modules
│   ├── data_collection/        # 🌐 API integrations and data fetchers
│   ├── preprocessing/          # 🧹 Data cleaning and preparation
│   ├── forecasting/           # 🤖 ML models and prediction engines
│   ├── visualization/         # 🎨 Chart generation and plotting
│   └── utils/                 # 🛠️ Utility functions and helpers
├── 📓 notebooks/               # 📊 Jupyter analysis notebooks
│   └── inflation_impact_analysis.ipynb
├── ⚙️ config/                  # 🔧 Configuration and settings
│   └── config.py              # API keys and environment management
├── 📋 requirements.txt         # 📦 Python dependencies
├── 🌐 .env.realtime           # 🔑 Environment variables template
└── 📚 docs/                   # 📖 Documentation and guides
    ├── REALTIME_SETUP.md      # 🚀 API setup instructions
    └── QUICK_START.py          # ⚡ Getting started guide
```

## 🚀 Quick Start

### 📦 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/personal-finance-inflation-tracker.git
cd personal-finance-inflation-tracker

# Install dependencies
pip install -r requirements.txt
```

### 🌐 Launch Real-time Dashboard
```bash
# Start the main real-time dashboard
streamlit run dashboard/realtime_dashboard.py

# Alternative: Basic dashboard (no API required)
streamlit run dashboard/working_dashboard.py
```

### ⚙️ API Configuration (Optional)
```bash
# Copy environment template
cp .env.realtime .env

# Add your free API keys (optional for enhanced features)
# FRED_API_KEY=your_fred_api_key_here
# WORLD_BANK_API_KEY=your_world_bank_key_here
```

### 🎯 No Setup Required
The dashboard works immediately with **free public APIs** - no API keys needed for basic functionality!

## 📊 Dashboard Features

### 🌐 Real-time Tabs
1. **📊 Overview**: Live economic metrics and key indicators
2. **📈 Inflation Analysis**: Real-time inflation trends across countries
3. **🏠 Cost of Living**: Detailed cost breakdowns and regional comparisons
4. **🔮 Budget Planning**: Personal financial planning with AI recommendations
5. **📋 Summary**: Comprehensive insights and data export options

### 🎯 Interactive Controls
- **🌍 Country Selection**: Choose from 190+ countries
- **⏰ Time Range**: Historical and current data analysis
- **🔄 Live Refresh**: Manual and automatic data updates
- **📱 Responsive Design**: Works on all devices

## 🌐 Live Data Sources
- **🏦 World Bank Open Data**: Global inflation and economic indicators (Free)
- **🏛️ FRED (Federal Reserve)**: US economic data and monetary policy (Free)
- **💱 ExchangeRate-API**: Real-time currency exchange rates (Free tier)
- **🌍 OECD Data**: Advanced economic statistics (Free)
- **🏠 Economic APIs**: Cost of living and salary data (Multiple sources)

## 🔬 Advanced Analytics

### 📈 Real-time Analysis
1. **🌡️ Inflation Impact Analysis**: Live tracking of price changes across sectors
2. **💰 Purchasing Power Calculator**: Real vs nominal income with inflation adjustment
3. **🗺️ Regional Economic Comparison**: Cost differences across 190+ locations
4. **👥 Demographic Profiling**: Spending patterns by age, income, and location
5. **🔮 Predictive Modeling**: AI-powered future cost and inflation forecasting

### 🤖 Machine Learning Pipeline
- **📊 Prophet Models**: Time series forecasting for inflation trends
- **📈 ARIMA/SARIMA**: Statistical forecasting with seasonal adjustments
- **🌲 XGBoost**: Multi-feature regression for cost prediction
- **🎯 K-Means Clustering**: Demographic and regional grouping analysis
- **🧠 Random Forest**: Feature importance analysis for economic factors

## 🎨 Professional Visualizations
- **📈 Interactive Time Series**: Real-time inflation and cost trends
- **🗺️ Geographic Heatmaps**: Regional affordability and cost comparisons
- **📊 Correlation Matrices**: Economic indicator relationships
- **🥧 Budget Breakdown Charts**: Category-wise spending analysis
- **🔮 Forecasting Plots**: Future predictions with confidence intervals
- **📱 Responsive Dashboards**: Mobile-friendly interactive charts

## 🚀 Performance Features
- **⚡ Smart Caching**: 1-hour data cache for optimal performance
- **🔄 Background Refresh**: Automatic data updates without interruption
- **🛡️ Fallback Systems**: Graceful handling of API failures
- **📊 Real-time Status**: Live indicators for data freshness and API health
- **🎯 Optimized Loading**: Efficient data processing and rendering

## 🤝 Contributing
We welcome contributions! Here's how to get started:

1. **🍴 Fork the repository**
2. **🌿 Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **✨ Make your changes**: Add features, fix bugs, improve documentation
4. **✅ Add tests**: Ensure your changes work correctly
5. **📝 Commit changes**: `git commit -m 'Add amazing feature'`
6. **📤 Push to branch**: `git push origin feature/amazing-feature`
7. **🔄 Open a Pull Request**: Describe your changes and benefits

### 🎯 Areas for Contribution
- **🌐 New API integrations**: Additional data sources
- **🤖 ML model improvements**: Better forecasting algorithms
- **🎨 UI/UX enhancements**: Dashboard improvements
- **📊 Data analysis features**: New analytical capabilities
- **🌍 Internationalization**: Support for more countries/currencies
- **📚 Documentation**: Guides, tutorials, and examples

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments
- **🏦 World Bank**: For providing free economic data APIs
- **🏛️ Federal Reserve**: For comprehensive economic indicators
- **🐍 Python Community**: For excellent data science libraries
- **🚀 Streamlit**: For the amazing web app framework
- **📊 Open Source**: All the fantastic libraries that make this possible

## 📊 Project Statistics
- **📈 Real-time Data**: 190+ countries supported
- **🔄 Auto-updates**: Hourly data refresh
- **🤖 ML Models**: 5+ forecasting algorithms
- **📱 Responsive**: Works on all screen sizes
- **⚡ Performance**: Sub-second page loads with caching
- **🌐 Global**: Multi-currency and international support

---

**💡 Built with passion for financial literacy and data-driven decision making!**

**🌟 If this project helps you make better financial decisions, please give it a star!**
