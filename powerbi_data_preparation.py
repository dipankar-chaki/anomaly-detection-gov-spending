import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

def prepare_powerbi_data():
    
    print("Loading anomaly detection results...")
    df = pd.read_csv('anomalies_detected.csv')
    
    df['date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
    
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year
    df['month_name'] = df['date'].dt.month_name()
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['hour'] = np.random.randint(0, 24, len(df))
    
    print("Classifying risk levels...")
    df['risk_score'] = abs(df['anomaly_score']) * 100
    
    df['risk_level'] = pd.cut(df['risk_score'], 
                              bins=[0, 1, 2, 5, 100], 
                              labels=['Low', 'Medium', 'High', 'Critical'])
    
    df['entity_name'] = df['agency'] + '_' + df['recipient_type']
    
    print("Creating main anomaly details table...")
    anomaly_details = df[[
        'entity_name', 'date', 'amount', 'risk_score', 'risk_level',
        'agency', 'recipient_type', 'month', 'day_of_week', 'quarter',
        'year', 'month_name', 'week_of_year', 'hour', 'is_anomaly'
    ]].copy()
    
    anomaly_details = anomaly_details.rename(columns={
        'entity_name': 'Entity',
        'date': 'Date',
        'amount': 'Transaction_Amount',
        'risk_score': 'Risk_Score',
        'risk_level': 'Risk_Level',
        'agency': 'Agency',
        'recipient_type': 'Recipient_Type',
        'month': 'Month',
        'day_of_week': 'Day_of_Week',
        'quarter': 'Quarter',
        'year': 'Year',
        'month_name': 'Month_Name',
        'week_of_year': 'Week_of_Year',
        'hour': 'Hour',
        'is_anomaly': 'Is_Anomaly'
    })
    
    print("Creating executive overview metrics...")
    exec_metrics = pd.DataFrame([{
        'Total_Transactions': len(df),
        'Anomalies_Detected': len(df[df['is_anomaly'] == 'Anomaly']),
        'Detection_Rate': (len(df[df['is_anomaly'] == 'Anomaly']) / len(df)) * 100,
        'Average_Risk_Score': df['risk_score'].mean(),
        'Total_Amount_Flagged': df[df['is_anomaly'] == 'Anomaly']['amount'].sum(),
        'High_Risk_Count': len(df[df['risk_level'] == 'Critical']),
        'Medium_Risk_Count': len(df[df['risk_level'] == 'High']),
        'Low_Risk_Count': len(df[df['risk_level'].isin(['Low', 'Medium'])])
    }])
    
    print("Creating time series aggregations...")
    time_series = df[df['is_anomaly'] == 'Anomaly'].groupby(['year', 'quarter', 'month']).agg({
        'amount': 'sum',
        'risk_score': 'mean',
        'is_anomaly': 'count'
    }).reset_index()
    
    time_series = time_series.rename(columns={
        'amount': 'Total_Amount',
        'risk_score': 'Avg_Risk_Score',
        'is_anomaly': 'Anomaly_Count',
        'year': 'Year',
        'quarter': 'Quarter',
        'month': 'Month'
    })
    
    print("Creating entity summary...")
    entity_summary = df[df['is_anomaly'] == 'Anomaly'].groupby('entity_name').agg({
        'amount': ['sum', 'mean', 'count'],
        'risk_score': 'mean'
    }).reset_index()
    
    entity_summary.columns = ['Entity', 'Total_Amount', 'Avg_Amount', 'Anomaly_Count', 'Avg_Risk_Score']
    entity_summary = entity_summary.sort_values('Anomaly_Count', ascending=False)
    
    print("Creating day-hour heatmap data...")
    day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                   4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    heatmap_data = df[df['is_anomaly'] == 'Anomaly'].groupby(['day_of_week', 'hour']).size().reset_index(name='Count')
    heatmap_data['Day_Name'] = heatmap_data['day_of_week'].map(day_mapping)
    
    print("Creating feature importance data (simulated SHAP values)...")
    features = ['Transaction Amount', 'Agency Type', 'Recipient Type', 'Time of Day', 
                'Day of Week', 'Historical Pattern', 'Seasonal Factor', 'Entity Risk Profile']
    
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Importance': np.random.uniform(0.1, 1.0, len(features)),
        'Impact_Direction': np.random.choice(['Positive', 'Negative'], len(features))
    })
    feature_importance = feature_importance.sort_values('Importance', ascending=False)
    feature_importance['Importance_Percentage'] = (feature_importance['Importance'] / 
                                                   feature_importance['Importance'].sum()) * 100
    
    print("Creating risk distribution data...")
    risk_distribution = df['risk_level'].value_counts().reset_index()
    risk_distribution.columns = ['Risk_Level', 'Count']
    risk_distribution['Percentage'] = (risk_distribution['Count'] / risk_distribution['Count'].sum()) * 100
    
    print("Exporting data for Power BI...")
    
    if not os.path.exists('powerbi_data'):
        os.makedirs('powerbi_data')
    
    anomaly_details.to_csv('powerbi_data/anomaly_details.csv', index=False)
    exec_metrics.to_csv('powerbi_data/executive_metrics.csv', index=False)
    time_series.to_csv('powerbi_data/time_series.csv', index=False)
    entity_summary.to_csv('powerbi_data/entity_summary.csv', index=False)
    heatmap_data.to_csv('powerbi_data/heatmap_data.csv', index=False)
    feature_importance.to_csv('powerbi_data/feature_importance.csv', index=False)
    risk_distribution.to_csv('powerbi_data/risk_distribution.csv', index=False)
    
    print("\n✅ Data preparation complete!")
    print(f"📊 Generated {len(anomaly_details)} records for analysis")
    print(f"📁 Data files saved in 'powerbi_data' directory")
    
    return {
        'total_transactions': len(df),
        'anomalies_detected': len(df[df['is_anomaly'] == 'Anomaly']),
        'detection_rate': (len(df[df['is_anomaly'] == 'Anomaly']) / len(df)) * 100,
        'files_created': 7
    }

if __name__ == "__main__":
    stats = prepare_powerbi_data()
    print("\nSummary Statistics:")
    print(f"- Total Transactions: {stats['total_transactions']:,}")
    print(f"- Anomalies Detected: {stats['anomalies_detected']:,}")
    print(f"- Detection Rate: {stats['detection_rate']:.2f}%")
    print(f"- Files Created: {stats['files_created']}")