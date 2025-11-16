# Power BI Dashboard Setup Guide
## Financial Anomaly Detection Dashboard

### Prerequisites
- Power BI Desktop (latest version)
- Python 3.x installed
- Access to the generated CSV files in `powerbi_data/` directory

### Quick Start (15 minutes)

#### Step 1: Prepare the Data
```bash
python3 powerbi_data_preparation.py
```
This creates 7 CSV files in the `powerbi_data/` directory with all necessary data transformations.

#### Step 2: Import Data into Power BI

1. Open Power BI Desktop
2. Click **Get Data** → **Text/CSV**
3. Navigate to the `powerbi_data/` folder
4. Import all 7 CSV files:
   - `anomaly_details.csv` (main transaction data)
   - `executive_metrics.csv` (KPI metrics)
   - `time_series.csv` (trend analysis)
   - `entity_summary.csv` (top entities)
   - `heatmap_data.csv` (pattern analysis)
   - `feature_importance.csv` (explainability)
   - `risk_distribution.csv` (risk breakdown)

#### Step 3: Create Relationships

In Power BI:
1. Go to **Model View**
2. Create these relationships:
   - `anomaly_details[Entity]` → `entity_summary[Entity]`
   - `anomaly_details[Risk_Level]` → `risk_distribution[Risk_Level]`

### Building the Dashboard Pages

#### Page 1: Executive Overview

**Cards (Top Row)**
1. Total Transactions: `SUM(executive_metrics[Total_Transactions])`
2. Anomalies Detected: `SUM(executive_metrics[Anomalies_Detected])`
3. Detection Rate: `AVERAGE(executive_metrics[Detection_Rate])`
4. Average Risk Score: `AVERAGE(executive_metrics[Average_Risk_Score])`

**Visualizations**
- **Line Chart**: Month on X-axis, Anomaly_Count on Y-axis (from time_series)
- **Donut Chart**: Risk_Level as Legend, Count as Values (from risk_distribution)
- **Bar Chart**: Top 10 Entities by Anomaly_Count (from entity_summary)

#### Page 2: Detailed Analysis

**Main Table**
- Add all columns from `anomaly_details`
- Apply conditional formatting on Risk_Level:
  - Critical: Red background
  - High: Orange background
  - Medium: Yellow background
  - Low: Green background

**Scatter Plot**
- X-axis: Transaction_Amount
- Y-axis: Risk_Score
- Size: Risk_Score
- Color: Risk_Level

**Heat Map**
- Use Matrix visual
- Rows: Day_Name
- Columns: Hour
- Values: Count (from heatmap_data)

**Slicers**
- Date Range (Date field)
- Agency (Dropdown)
- Risk Level (Buttons)

#### Page 3: Explainability

**Bar Chart**
- Feature on X-axis
- Importance_Percentage on Y-axis
- Sort descending

**Text Box**
- Copy the methodology text from the JSON template
- Format as markdown

**Gauge**
- Create measure: `System Health = 85`
- Set min=0, max=100
- Color zones: Red (0-50), Yellow (50-75), Green (75-100)

### DAX Measures to Create

```dax
// Detection Effectiveness
Detection Rate % = 
DIVIDE(
    COUNTROWS(FILTER(anomaly_details, anomaly_details[Is_Anomaly] = "Anomaly")),
    COUNTROWS(anomaly_details)
) * 100

// High Risk Alert Count
High Risk Count = 
CALCULATE(
    COUNTROWS(anomaly_details),
    anomaly_details[Risk_Level] = "Critical"
)

// Total Flagged Amount
Total Flagged = 
CALCULATE(
    SUM(anomaly_details[Transaction_Amount]),
    anomaly_details[Is_Anomaly] = "Anomaly"
)

// Average Transaction Size
Avg Transaction = AVERAGE(anomaly_details[Transaction_Amount])

// Risk Trend
Risk Trend = 
VAR CurrentMonth = MAX(anomaly_details[Month])
VAR PreviousMonth = CurrentMonth - 1
VAR CurrentRisk = CALCULATE(
    AVERAGE(anomaly_details[Risk_Score]),
    anomaly_details[Month] = CurrentMonth
)
VAR PreviousRisk = CALCULATE(
    AVERAGE(anomaly_details[Risk_Score]),
    anomaly_details[Month] = PreviousMonth
)
RETURN
IF(
    CurrentRisk > PreviousRisk,
    "Increasing ↑",
    "Decreasing ↓"
)
```

### Refresh Settings

1. Go to **Transform Data** → **Data Source Settings**
2. Change source paths to your local `powerbi_data/` folder
3. Set up scheduled refresh:
   - File → Options → Data Load
   - Enable background data refresh
   - Set interval to Daily at 6:00 AM

### Color Theme

Apply consistent colors:
- Primary: #1976D2 (Blue)
- Success: #4CAF50 (Green)
- Warning: #FFC107 (Amber)
- Danger: #F44336 (Red)
- Background: #FAFAFA (Light Gray)

### Publishing to Power BI Service

1. Save your .pbix file
2. Click **Publish** in Home ribbon
3. Select your workspace
4. Configure gateway for automatic refresh:
   - Install Power BI Gateway
   - Map local CSV folder
   - Set refresh schedule

### Advanced Features

#### Drill-Through
1. Right-click on any entity in Page 2 table
2. Select "Drill through" → "Explainability"
3. View detailed breakdown for that entity

#### Bookmarks
Create quick views:
- "High Risk Only": Filter to Critical risk level
- "Recent Week": Last 7 days only
- "Health Sector": Agency = Health

#### Alerts
In Power BI Service:
1. Pin "Anomalies Detected" card to dashboard
2. Click (...) → Manage Alerts
3. Set threshold (e.g., > 10 anomalies)
4. Configure email notifications

### Troubleshooting

**Issue: Data not refreshing**
- Check file paths in Data Source Settings
- Ensure Python script has write permissions
- Verify CSV files are not open in Excel

**Issue: Visuals not showing data**
- Check relationships in Model view
- Verify data types (especially dates)
- Clear filters and slicers

**Issue: Performance slow**
- Reduce data history (keep last 90 days)
- Use Import mode instead of DirectQuery
- Optimize DAX measures

### Performance Tips

1. **Use aggregated tables** for executive overview
2. **Limit detailed data** to last 90 days
3. **Pre-calculate** complex measures in Python
4. **Use incremental refresh** for large datasets
5. **Optimize visuals** (avoid too many on one page)

### Next Steps

1. Customize risk thresholds based on your business rules
2. Add more sophisticated ML features to feature_importance
3. Integrate with real-time data sources
4. Set up automated email reports
5. Create mobile-optimized views

### Support

For issues or enhancements:
1. Check Power BI documentation
2. Review the `powerbi_dashboard_template.json` for visual specifications
3. Run `python3 powerbi_data_preparation.py` to regenerate data
4. Modify risk levels in the Python script as needed

---
*Dashboard Version: 1.0*
*Last Updated: 2024*
*Estimated Setup Time: 4-6 hours*