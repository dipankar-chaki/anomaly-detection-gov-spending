import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("anomalies_detected.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Anomalies")
agencies = df["agency"].unique()
selected_agencies = st.sidebar.multiselect("Select Agencies", agencies, default=agencies)

min_amount = float(df["amount"].min())
max_amount = float(df["amount"].max())
amount_range = st.sidebar.slider("Amount Range", min_value=min_amount, max_value=max_amount,
                                 value=(min_amount, max_amount))

# Apply filters
filtered_df = df[
    (df["agency"].isin(selected_agencies)) &
    (df["amount"] >= amount_range[0]) &
    (df["amount"] <= amount_range[1])
]

# Main app
st.title("💰 Government Spending Anomaly Detection")
st.markdown("This dashboard visualizes anomalies in government payment data using Isolation Forest.")

st.subheader("📊 Filtered Anomalies")
st.write(f"Showing {len(filtered_df)} anomalies:")
st.dataframe(filtered_df)

# Distribution plot
st.subheader("📈 Anomaly Amount Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_df["amount"], bins=30, kde=True, ax=ax)
ax.set_xlabel("Amount")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Agency-wise boxplot
st.subheader("🏛️ Agency-wise Spending")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x="agency", y="amount", ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)
