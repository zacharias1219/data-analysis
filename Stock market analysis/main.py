import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import plotly.io as pio

# Set default plotly template
pio.templates.default = 'plotly_white'

# Read stocks data from CSV
stocks_data = pd.read_csv('stocks.csv')
print(stocks_data.head())


# Calculate descriptive statistics
descriptive_stats = stocks_data.groupby('Ticker')['Close'].describe()
print(descriptive_stats)

# Convert 'Date' column to datetime
stocks_data['Date'] = pd.to_datetime(stocks_data['Date'])

# Pivot data for time series analysis
pivot_data = stocks_data.pivot(index='Date',columns='Ticker',values='Close')

# Create subplots
fig = make_subplots(rows=1, cols=1)

# Add traces for each stock
for column in pivot_data.columns:
    fig.add_trace(go.Scatter(x=pivot_data.index, y=pivot_data[column], name=column), row=1, col=1)

# Update layout
fig.update_layout(
    title_text='Time Series of Closing Prices',
    xaxis_title='Date',
    yaxis_title='Closing Price',
    legend_title='Ticker',
    showlegend=True
)

# Show the figure
fig.show()

# Calculate volatility
volatility = pivot_data.std().sort_values(ascending=False)

# Create bar chart for volatility
fig = px.bar(volatility, x=volatility.index, y=volatility.values, labels={'y':'Standard Deviation', 'x':'Ticker'}, title='Volatility of Closing Prices')
fig.show()

# Calculate correlation matrix
correlation_matrix = pivot_data.corr()

# Create heatmap for correlation matrix
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='blues',
    colorbar=dict(title='Correlation')
))
fig.update_layout(
    title='Correlation Matrix of Closing Prices',
    xaxis_title='Ticker',
    yaxis_title='Ticker'
)
fig.show()

# Calculate percentage change
percentage_change = ((pivot_data.iloc[-1] - pivot_data.iloc[0]) / pivot_data.iloc[0]) * 100

# Create bar chart for percentage change
fig = px.bar(percentage_change, x=percentage_change.index, y=percentage_change.values, labels={'y': 'Percentage Change (%)', 'x': 'Ticker'}, title='Percentage Change in Closing Prices')
fig.show()

# Calculate daily returns
daily_returns = pivot_data.pct_change().dropna()
avg_daily_return = daily_returns.mean()
risk = daily_returns.std()

# Create risk-return analysis plot
risk_return_df = pd.DataFrame({'Risk': risk, 'Average Daily Return': avg_daily_return})
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=risk_return_df['Risk'],
    y=risk_return_df['Average Daily Return'],
    mode='markers+text',
    text=risk_return_df.index,
    textposition="top center",
    marker=dict(size=10)
))
fig.update_layout(
    title='Risk vs. Return Analysis',
    xaxis_title='Risk (Standard Deviation)',
    yaxis_title='Average Daily Return',
    showlegend=False
)
fig.show()
