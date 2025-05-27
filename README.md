![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-ff4b4b)

# 🕵️ Government Spending Anomaly Detection

This project applies unsupervised machine learning to detect anomalies in government payment data — such as unusually large transactions or suspicious spending patterns — using **Isolation Forest** and **SHAP explainability**.

---

## 📌 Project Overview

Government agencies handle billions in transactions. This project simulates a real-world scenario where we:

- Analyze spending patterns from a government department dataset  
- Detect outliers (potential fraud, errors, or misallocations)  
- Explain why each transaction was flagged as anomalous using SHAP  

---

## 📂 Dataset

For demonstration, we use a **simulated dataset** based on:
- Agency name (Health, Education, Defence, Infrastructure)
- Recipient type (Company, Non-profit, Individual)
- Payment amount (Gamma-distributed)
- Payment date (daily range)

➡️ You can adapt this to use real data from [data.gov.au](https://data.gov.au/).

---

## ⚙️ Technologies Used

| Tool                    | Purpose                                      |
|-------------------------|----------------------------------------------|
| **Python**              | Core language                                |
| **Jupyter Notebook**    | Interactive development and exploration      |
| **Pandas & NumPy**      | Data handling                                |
| **Scikit-learn**        | Isolation Forest for anomaly detection       |
| **Seaborn & Matplotlib**| Data visualization                           |
| **SHAP**                | Model interpretability                       |

---

## 🚀 How It Works

### 1. Data Preprocessing
- Categorical encoding (`get_dummies`)
- Extracted features from date (month, weekday)

### 2. Anomaly Detection
- Trained an `IsolationForest` model (unsupervised)
- Predicted anomalies with 5% contamination
- Labeled transactions as “Normal” or “Anomaly”

### 3. Explainability
- Used **SHAP** to explain what made a transaction anomalous
- Visualized individual outlier reasoning with waterfall plots

---

## 📊 Example Visuals

- Spending distribution with anomalies highlighted
- Anomalies by weekday and agency
- SHAP waterfall plot for one suspicious transaction

*(See notebook for live charts)*

---

## 📁 Output Files

- `anomalies_detected.csv` — flagged transactions with their scores and features

---

## 📦 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/government-anomaly-detection.git
cd government-anomaly-detection
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook
```bash
jupyter notebook
```

Open gov_anomaly_detection.ipynb and run cell by cell.

---

## 🙈 .gitignore
This project includes a .gitignore file that excludes:

Virtual environments (venv/)

Bytecode files (__pycache__/)

Notebook checkpoints

System files like .DS_Store

Large output files (e.g., .csv exports)

---

## 📄 License
MIT — use freely with attribution.

---

## 🙋‍♂️ Author

Dipankar Chaki

PhD in Computer Science | ML & AI Researcher