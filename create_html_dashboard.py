import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import os

print("📊 Creating Financial Anomaly Detection Dashboard...")
print("=" * 60)

# Load all data files
print("Loading data files...")
anomaly_details = pd.read_csv('powerbi_data/anomaly_details.csv')
exec_metrics = pd.read_csv('powerbi_data/executive_metrics.csv')
time_series = pd.read_csv('powerbi_data/time_series.csv')
entity_summary = pd.read_csv('powerbi_data/entity_summary.csv')
heatmap_data = pd.read_csv('powerbi_data/heatmap_data.csv')
feature_importance = pd.read_csv('powerbi_data/feature_importance.csv')
risk_distribution = pd.read_csv('powerbi_data/risk_distribution.csv')

# Convert date column
anomaly_details['Date'] = pd.to_datetime(anomaly_details['Date'])

# Define color scheme
colors = {
    'primary': '#1976D2',
    'success': '#4CAF50',
    'warning': '#FFC107',
    'danger': '#F44336',
    'info': '#00BCD4',
    'Low': '#4CAF50',
    'Medium': '#FFC107',
    'High': '#FF9800',
    'Critical': '#F44336'
}

# Create the HTML dashboard
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Anomaly Detection Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .dashboard-container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
            color: white;
            padding: 30px 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .nav-tabs {
            background: #f5f5f5;
            padding: 0 30px;
            border-bottom: 1px solid #ddd;
            display: flex;
            gap: 5px;
        }
        
        .nav-tab {
            padding: 15px 30px;
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            top: 1px;
        }
        
        .nav-tab:hover {
            color: #1976D2;
        }
        
        .nav-tab.active {
            color: #1976D2;
            background: white;
            border-bottom: 3px solid #1976D2;
            font-weight: 500;
        }
        
        .tab-content {
            display: none;
            padding: 30px;
            animation: fadeIn 0.5s;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .kpi-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #1976D2;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        .kpi-card.danger { border-left-color: #F44336; }
        .kpi-card.success { border-left-color: #4CAF50; }
        .kpi-card.warning { border-left-color: #FFC107; }
        
        .kpi-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .kpi-value {
            font-size: 2.2rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        
        .kpi-change {
            font-size: 0.85rem;
            color: #666;
        }
        
        .chart-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .chart-title {
            font-size: 1.2rem;
            font-weight: 500;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .insight-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .insight-box h3 {
            margin-bottom: 10px;
            font-size: 1.3rem;
        }
        
        .insight-box p {
            opacity: 0.95;
            line-height: 1.6;
        }
        
        .methodology-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .methodology-section h3 {
            color: #1976D2;
            margin-bottom: 15px;
            font-size: 1.4rem;
        }
        
        .methodology-section p {
            color: #555;
            line-height: 1.8;
            margin-bottom: 10px;
        }
        
        .risk-levels {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .risk-level-item {
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            color: white;
            font-weight: 500;
        }
        
        .footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        .timestamp {
            font-size: 0.9rem;
            color: #999;
        }
        
        @media (max-width: 768px) {
            .chart-row {
                grid-template-columns: 1fr;
            }
            .kpi-row {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1>🔍 Financial Anomaly Detection Dashboard</h1>
            <p>Real-time monitoring and analysis of government spending patterns</p>
        </div>
        
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="switchTab('executive')">Executive Overview</button>
            <button class="nav-tab" onclick="switchTab('detailed')">Detailed Analysis</button>
            <button class="nav-tab" onclick="switchTab('explainability')">Explainability & Insights</button>
        </div>
        
        <!-- Executive Overview Tab -->
        <div id="executive" class="tab-content active">
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-label">Total Transactions</div>
                    <div class="kpi-value">""" + f"{exec_metrics['Total_Transactions'].values[0]:,}" + """</div>
                    <div class="kpi-change">All time records analyzed</div>
                </div>
                <div class="kpi-card danger">
                    <div class="kpi-label">Anomalies Detected</div>
                    <div class="kpi-value">""" + f"{exec_metrics['Anomalies_Detected'].values[0]:,}" + """</div>
                    <div class="kpi-change">Requires investigation</div>
                </div>
                <div class="kpi-card warning">
                    <div class="kpi-label">Detection Rate</div>
                    <div class="kpi-value">""" + f"{exec_metrics['Detection_Rate'].values[0]:.1f}%" + """</div>
                    <div class="kpi-change">Of all transactions flagged</div>
                </div>
                <div class="kpi-card success">
                    <div class="kpi-label">Average Risk Score</div>
                    <div class="kpi-value">""" + f"{exec_metrics['Average_Risk_Score'].values[0]:.2f}" + """</div>
                    <div class="kpi-change">Risk assessment metric</div>
                </div>
            </div>
            
            <div class="chart-row">
                <div class="chart-container">
                    <h3 class="chart-title">📈 Anomaly Trend Over Time</h3>
                    <div id="trend-chart"></div>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">🎯 Risk Level Distribution</h3>
                    <div id="risk-donut"></div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">🏢 Top 10 Entities by Anomaly Count</h3>
                <div id="top-entities"></div>
            </div>
            
            <div class="insight-box">
                <h3>💡 Key Insights</h3>
                <p>• The system has analyzed """ + f"{exec_metrics['Total_Transactions'].values[0]:,}" + """ transactions with a """ + f"{exec_metrics['Detection_Rate'].values[0]:.1f}%" + """ anomaly detection rate</p>
                <p>• Total flagged amount: $""" + f"{exec_metrics['Total_Amount_Flagged'].values[0]:,.2f}" + """</p>
                <p>• High-risk transactions requiring immediate attention: """ + f"{exec_metrics['High_Risk_Count'].values[0]}" + """</p>
            </div>
        </div>
        
        <!-- Detailed Analysis Tab -->
        <div id="detailed" class="tab-content">
            <div class="chart-row">
                <div class="chart-container">
                    <h3 class="chart-title">💰 Transaction Amount vs Risk Score</h3>
                    <div id="scatter-plot"></div>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">📊 Anomaly Pattern Heatmap</h3>
                    <div id="heatmap"></div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">📋 Recent High-Risk Transactions</h3>
                <div id="transactions-table"></div>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">🏛️ Anomalies by Agency</h3>
                <div id="agency-breakdown"></div>
            </div>
        </div>
        
        <!-- Explainability Tab -->
        <div id="explainability" class="tab-content">
            <div class="chart-container">
                <h3 class="chart-title">🎯 Feature Importance Analysis</h3>
                <div id="feature-importance"></div>
            </div>
            
            <div class="methodology-section">
                <h3>🔬 Anomaly Detection Methodology</h3>
                <p><strong>Algorithm:</strong> The system employs advanced machine learning algorithms including Isolation Forest to identify unusual patterns in financial transactions.</p>
                <p><strong>Risk Scoring:</strong> Each transaction receives a risk score based on its deviation from normal patterns. The score considers multiple factors including amount, timing, entity history, and seasonal patterns.</p>
                <p><strong>Continuous Learning:</strong> The model continuously updates its understanding of normal patterns, adapting to legitimate changes while maintaining sensitivity to anomalies.</p>
                
                <div class="risk-levels">
                    <div class="risk-level-item" style="background: #4CAF50;">
                        <div>Low Risk (0-1)</div>
                        <div>Minor deviations</div>
                    </div>
                    <div class="risk-level-item" style="background: #FFC107;">
                        <div>Medium Risk (1-2)</div>
                        <div>Needs attention</div>
                    </div>
                    <div class="risk-level-item" style="background: #FF9800;">
                        <div>High Risk (2-5)</div>
                        <div>Investigation required</div>
                    </div>
                    <div class="risk-level-item" style="background: #F44336;">
                        <div>Critical (>5)</div>
                        <div>Immediate action</div>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">📈 Risk Score Distribution</h3>
                <div id="risk-histogram"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated on """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</p>
            <p class="timestamp">Dashboard Version 1.0 | Data refreshed daily</p>
        </div>
    </div>
    
    <script>
"""

print("Creating visualizations...")

# 1. Trend Chart
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=time_series['Month'].values,
    y=time_series['Anomaly_Count'].values,
    mode='lines+markers',
    name='Anomalies',
    line=dict(color='#1976D2', width=3),
    marker=dict(size=8),
    fill='tozeroy',
    fillcolor='rgba(25, 118, 210, 0.1)'
))
fig_trend.update_layout(
    showlegend=False,
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title="Month",
    yaxis_title="Count",
    hovermode='x unified'
)

# 2. Risk Donut Chart
fig_donut = go.Figure(data=[go.Pie(
    labels=risk_distribution['Risk_Level'].values,
    values=risk_distribution['Count'].values,
    hole=.5,
    marker_colors=['#4CAF50', '#FFC107', '#FF9800', '#F44336']
)])
fig_donut.update_layout(
    showlegend=True,
    height=300,
    margin=dict(l=0, r=0, t=0, b=0)
)

# 3. Top Entities Bar Chart
top_10 = entity_summary.head(10)
fig_entities = go.Figure(data=[go.Bar(
    x=top_10['Anomaly_Count'].values,
    y=top_10['Entity'].values,
    orientation='h',
    marker_color='#1976D2',
    text=top_10['Anomaly_Count'].values,
    textposition='auto',
)])
fig_entities.update_layout(
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title="Anomaly Count",
    yaxis_title=""
)

# 4. Scatter Plot
fig_scatter = px.scatter(
    anomaly_details,
    x='Transaction_Amount',
    y='Risk_Score',
    color='Risk_Level',
    size='Risk_Score',
    color_discrete_map=colors,
    hover_data=['Entity', 'Agency']
)
fig_scatter.update_layout(
    height=400,
    margin=dict(l=0, r=0, t=0, b=0)
)

# 5. Heatmap
pivot_data = heatmap_data.pivot_table(
    values='Count',
    index='Day_Name',
    columns='hour',
    fill_value=0
)
fig_heatmap = go.Figure(data=go.Heatmap(
    z=pivot_data.values,
    x=pivot_data.columns,
    y=pivot_data.index,
    colorscale='Blues'
))
fig_heatmap.update_layout(
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title="Hour of Day",
    yaxis_title="Day of Week"
)

# 6. Feature Importance
fig_features = go.Figure(data=[go.Bar(
    x=feature_importance['Importance_Percentage'].values,
    y=feature_importance['Feature'].values,
    orientation='h',
    marker_color=['#4CAF50' if x == 'Positive' else '#F44336' 
                   for x in feature_importance['Impact_Direction'].values]
)])
fig_features.update_layout(
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title="Importance (%)",
    yaxis_title=""
)

# 7. Risk Histogram
fig_histogram = go.Figure(data=[go.Histogram(
    x=anomaly_details['Risk_Score'].values,
    nbinsx=30,
    marker_color='#1976D2'
)])
fig_histogram.update_layout(
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title="Risk Score",
    yaxis_title="Frequency"
)

# 8. Agency Breakdown
agency_counts = anomaly_details.groupby('Agency').size().reset_index(name='Count')
fig_agency = go.Figure(data=[go.Bar(
    x=agency_counts['Agency'].values,
    y=agency_counts['Count'].values,
    marker_color=['#1976D2', '#4CAF50', '#FFC107']
)])
fig_agency.update_layout(
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title="Agency",
    yaxis_title="Anomaly Count"
)

# 9. Transactions Table
top_transactions = anomaly_details.nlargest(10, 'Risk_Score')[
    ['Entity', 'Date', 'Transaction_Amount', 'Risk_Score', 'Risk_Level']
]
fig_table = go.Figure(data=[go.Table(
    header=dict(
        values=['Entity', 'Date', 'Amount ($)', 'Risk Score', 'Level'],
        fill_color='#1976D2',
        font=dict(color='white', size=12),
        align='left'
    ),
    cells=dict(
        values=[
            top_transactions['Entity'].values,
            top_transactions['Date'].dt.strftime('%Y-%m-%d').values,
            ['${:,.2f}'.format(x) for x in top_transactions['Transaction_Amount'].values],
            ['{:.2f}'.format(x) for x in top_transactions['Risk_Score'].values],
            top_transactions['Risk_Level'].values
        ],
        fill_color=['#f0f0f0', 'white'],
        align='left'
    )
)])
fig_table.update_layout(
    height=400,
    margin=dict(l=0, r=0, t=0, b=0)
)

# Add all charts to HTML
html_content += f"""
        Plotly.newPlot('trend-chart', {fig_trend.to_json()});
        Plotly.newPlot('risk-donut', {fig_donut.to_json()});
        Plotly.newPlot('top-entities', {fig_entities.to_json()});
        Plotly.newPlot('scatter-plot', {fig_scatter.to_json()});
        Plotly.newPlot('heatmap', {fig_heatmap.to_json()});
        Plotly.newPlot('feature-importance', {fig_features.to_json()});
        Plotly.newPlot('risk-histogram', {fig_histogram.to_json()});
        Plotly.newPlot('agency-breakdown', {fig_agency.to_json()});
        Plotly.newPlot('transactions-table', {fig_table.to_json()});
        
        function switchTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.nav-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""

# Save the HTML file
output_file = 'anomaly_detection_dashboard.html'
with open(output_file, 'w') as f:
    f.write(html_content)

print(f"\n✅ Dashboard created successfully!")
print(f"📁 File saved as: {output_file}")
print(f"📊 Total visualizations: 9")
print(f"📈 Data points analyzed: {len(anomaly_details):,}")
print(f"\n🚀 To view the dashboard:")
print(f"   1. Open Finder")
print(f"   2. Navigate to: {os.getcwd()}")
print(f"   3. Double-click: {output_file}")
print(f"   Or run: open {output_file}")
print("\n" + "=" * 60)
print("Dashboard is fully interactive - hover, zoom, and click on elements!")