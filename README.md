<div align="center">

# 🛡️ Cyber Security Threat Classifier

<img src="https://readme-typing-svg.herokuapp.com?font=Rajdhani&size=22&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=AI-Powered+Threat+Classification+System;Security+Operations+Center+Assistant;Microsoft+GUIDE+Dataset+%7C+8.9M+Records;Random+Forest+%7C+SMOTE+%7C+Flask+Web+App" alt="Typing SVG" />

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.3.0-02B56A?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![Imbalanced-Learn](https://img.shields.io/badge/Imbalanced--Learn-0.12.0-F09300?style=for-the-badge)](https://imbalanced-learn.org)

</div>

<div align="center">

![Status](https://img.shields.io/badge/Status-Complete-00ff88?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-Microsoft%20GUIDE-0078D4?style=flat-square&logo=microsoft)
![Records](https://img.shields.io/badge/Train%20Records-8.9M-ff6b35?style=flat-square)
![Accuracy](https://img.shields.io/badge/Best%20Accuracy-70.45%25-00d4ff?style=flat-square)

</div>

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Project Architecture](#-project-architecture)
- [Dataset Overview](#-dataset-overview)
- [Tech Stack](#-tech-stack)
- [Project Workflow](#-project-workflow)
- [Model Results](#-model-results)
- [Flask Web Application](#-flask-web-application)
- [How to Run](#-how-to-run)
- [Key Challenges](#-key-challenges)
- [Conclusion](#-conclusion)

---

## 🎯 Problem Statement

Cybersecurity incidents are growing in volume and complexity. Security Operations Center (SOC) analysts are overwhelmed by thousands of alerts daily — most of which are false alarms.

**This project builds an AI-powered classification system** that automatically categorizes cybersecurity incidents into:

| Class | Description | Priority |
|-------|-------------|----------|
| 🟢 **BenignPositive** | False alarm — no real threat | LOW — ignore |
| 🟡 **TruePositive** | Real threat — needs investigation | MEDIUM — assign analyst |
| 🔴 **MultiStageAttack** | Active multi-stage attack | CRITICAL — escalate immediately |

> **Real-world Impact**: Saves SOC analysts hours of manual triage. Enables faster response to critical threats.

---

## 🏗️ Project Architecture

```
Cyber Security Threat Classifier/
│
├── 📓 notebooks/
│   ├── Part_A_Data_Preprocessing_Exploration.ipynb   # EDA + Cleaning + Encoding
│   └── Part_B_Modeling_Evaluation_Deployment.ipynb   # Training + Evaluation
│
├── 🌐 app/
│   ├── app.py                    # Flask backend
│   ├── templates/
│   │   ├── index.html            # SOC input dashboard
│   │   └── result.html           # Prediction result page
│   └── static/
│
├── 💾 models/
│   ├── rf_no_smote_model.joblib       # ✅ Best model (deployed)
│   ├── rf_smote_tuned_model.joblib
│   └── rf_smote_enn_tuned_model.joblib
│
├── 📊 data/
│   ├── GUIDE_Train.csv           # 9.5M rows, 45 columns
│   └── GUIDE_Test.csv            # 4.1M rows, 46 columns
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset Overview

| Property | Train Set | Test Set |
|----------|-----------|----------|
| **Source** | Microsoft GUIDE Dataset | Microsoft GUIDE Dataset |
| **Rows** | 9,500,000+ | 4,100,000+ |
| **Columns** | 45 | 46 |
| **Target Column** | `IncidentGrade` | `IncidentGrade` |
| **After Preprocessing** | 8,922,805 rows × 154 cols | — |
| **File Size (Encoded)** | ~1.40 GB | — |

### Target Class Distribution

```
BenignPositive   ████████████████████  ~42%
TruePositive     █████████████         ~36%
MultiStageAttack ████████              ~22%
```

### Key Features Used

| Feature | Type | Description |
|---------|------|-------------|
| `AlertTitle` | Categorical | Type of security alert triggered |
| `Category` | Categorical | Incident category (Malware, Phishing, etc.) |
| `EntityType` | Categorical | Type of entity involved (File, User, IP, etc.) |
| `EvidenceRole` | Categorical | Role of evidence in incident |
| `DeviceName` | Categorical | Affected device identifier |
| `AccountName` | Categorical | Compromised account name |
| `OSFamily` | Categorical | Operating system of affected device |
| `CountryCode` | Categorical | Geographic location of incident |
| `Hour` | Numerical | Hour of day incident occurred |
| `Day` | Numerical | Day of month incident occurred |

---

## 🛠️ Tech Stack

```python
Language     : Python 3.10+
ML Libraries : Scikit-Learn, XGBoost, LightGBM
Imbalance    : Imbalanced-Learn (SMOTE, SMOTEENN)
Data         : Pandas, NumPy, Joblib
Viz          : Matplotlib, Seaborn
Web App      : Flask 3.0
Frontend     : HTML5, CSS3 (custom SOC dashboard UI)
Memory Mgmt  : mmap_mode + chunked loading (2.3GB RAM constraint)
```

---

## 🔄 Project Workflow

### Part A — Data Preprocessing & EDA

```
Raw CSV (9.5M rows)
        ↓
Chunked Loading (500K rows/chunk) → Memory Optimization
        ↓
Drop columns with >50% missing values
        ↓
Drop rows where IncidentGrade is null
        ↓
Remove duplicates
        ↓
Feature Engineering: Timestamp → Year, Month, Day, Hour
        ↓
Drop ID/irrelevant columns (22 columns removed)
        ↓
Group rare categories → "Others" (top 5 kept per column)
        ↓
Label Encoding: IncidentGrade (target)
        ↓
One-Hot Encoding: 15 categorical columns
        ↓
Saved as encoded_train_data.joblib (1.40 GB)
```

### Part B — Modeling & Evaluation

```
Load encoded data (mmap_mode='r' — RAM safe)
        ↓
Index-based 80:20 Stratified Split (no data copy)
        ↓
10% sample → 6 Model Comparison
        ↓
2% sample + SMOTE → RF + RandomizedSearchCV (5 iter, 3-fold CV)
        ↓
2% sample (No SMOTE) → RF Training
        ↓
2% sample + SMOTEENN → RF + RandomizedSearchCV
        ↓
All 3 models evaluated on Test Data
        ↓
Best model saved → rf_no_smote_model.joblib
```

---

## 📈 Model Results

### Model Comparison (10% Training Sample)

| Model | Accuracy | Macro-F1 | Precision | Recall |
|-------|----------|----------|-----------|--------|
| Logistic Regression | 0.6319 | 0.54 | 0.64 | 0.55 |
| Decision Tree | 0.7032 | 0.67 | 0.70 | 0.66 |
| **Random Forest** | **0.7045** | **0.67** | **0.70** | **0.66** |
| XGBoost | 0.6794 | 0.62 | 0.71 | 0.61 |
| LightGBM | 0.6773 | 0.61 | 0.72 | 0.61 |

### SMOTE Comparison (2% Sample + Validation on 100K rows)

| Strategy | Accuracy | Macro-F1 | Notes |
|----------|----------|----------|-------|
| RF + SMOTE | 0.67 | 0.65 | Balanced but slightly lower accuracy |
| **RF No SMOTE** | **0.68** | **0.65** | ✅ Best — deployed in Flask app |
| RF + SMOTEENN | 0.65 | 0.62 | Over-cleaned data hurt performance |

### Best Model — Random Forest (No SMOTE)

```
Classification Report (Validation — 100K samples):

              precision    recall  f1-score   support
           0       0.67      0.80      0.73     42530   ← BenignPositive
           1       0.62      0.43      0.51     21813   ← MultiStageAttack
           2       0.73      0.70      0.71     35657   ← TruePositive

    accuracy                           0.68    100000
   macro avg       0.67      0.64      0.65    100000
```

---

## 🌐 Flask Web Application

A real-world SOC Dashboard built with Flask — dark cybersecurity theme with animated UI.

### Features
- 🖥️ **SOC-style dark dashboard** — professional cybersecurity aesthetic
- 📋 **5-section input form** — Alert Info, Entity, Device, Location, Timestamp
- 🎯 **Instant classification** — BenignPositive / TruePositive / MultiStageAttack
- 📊 **Confidence score** + **class probability bars**
- 🚨 **Color-coded severity** — Green / Yellow / Red with action recommendation
- ✅ **RAM-safe prediction** — works on 2GB RAM machines

### App Screenshots

> Input Dashboard (SOC Terminal style)
```
┌─────────────────────────────────────────┐
│ 🛡 CYBER SECURITY THREAT CLASSIFIER   SYSTEM ONLINE ●       │
├─────────────────────────────────────────┤
│ [ 01 ] ALERT INFORMATION               │
│   Alert Title: [Malware detected    ▼] │
│   Category:    [Malware             ▼] │
├─────────────────────────────────────────┤
│ [ 02 ] ENTITY & EVIDENCE               │
│   Entity Type:    [File          ▼]    │
│   Evidence Role:  [Related       ▼]    │
├─────────────────────────────────────────┤
│         🔍 ANALYZE INCIDENT            │
└─────────────────────────────────────────┘
```

> Result Page
```
┌─────────────────────────────────────────┐
│         🚨                             │
│    MultiStageAttack                    │
│    SEVERITY: CRITICAL                  │
│  ▶ Immediate response required!        │
├──────────────────┬──────────────────────┤
│ CONFIDENCE: 74%  │ BenignPositive  12% │
│                  │ TruePositive    14% │
│                  │ MultiStage      74% │
└──────────────────┴──────────────────────┘
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/Rutujamurkute98/cyber-security-threat-classifier.git
cd cyber-security-threat-classifier
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Models (Optional — if .joblib files not present)

```bash
# Run notebooks in order:
# 1. Part_A_Data_Preprocessing_Exploration.ipynb
# 2. Part_B_Modeling_Evaluation_Deployment.ipynb
```

### 5. Run Flask App

```bash
python app/app.py
```

### 6. Open in Browser

```
http://127.0.0.1:5000
```

---

## ☁️ Upload to GitHub

If Git is not installed on your machine, install it first from:
https://git-scm.com/downloads

Then run these commands from project root:

```bash
git init
git add .
git commit -m "Initial commit: Cyber Security Threat Classifier project"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

If any model file is larger than 100 MB, use Git LFS before push:

```bash
git lfs install
git lfs track "*.joblib"
git add .gitattributes
git add .
git commit -m "Track model artifacts with Git LFS"
git push
```

---

## ▲ Deploy on Vercel

This project includes `vercel.json` and `api/index.py` for Vercel Python runtime.

### Option A: Vercel Dashboard

1. Push code to GitHub.
2. Open Vercel and click **Add New Project**.
3. Import your GitHub repository.
4. Keep defaults and deploy.

### Option B: Vercel CLI

```bash
npm i -g vercel
vercel login
vercel
vercel --prod
```

### Important Note

Vercel serverless functions have size and cold-start limits, so heavy ML models can be slow.
If you face deployment/runtime limits, deploy the same Flask app on Render or Railway for better ML backend support.

---

---

## 🏆 Conclusion

**Cyber Security Threat Classifier** demonstrates that production-grade ML systems can be built even under severe hardware constraints. Key achievements:

- ✅ Processed **8.9 million records** on a **2.3GB RAM** machine using memory-mapped loading
- ✅ Achieved **70.45% accuracy** with Random Forest on 10% sample
- ✅ Built a **real-time Flask web app** with SOC-grade dark UI
- ✅ Deployed 3 model variants (SMOTE / No SMOTE / SMOTEENN) for comparison
- ✅ Complete end-to-end pipeline: Raw CSV → Preprocessing → Training → Web App

---

## 👩‍💻 About Me

**Rutuja** — Final year IT Engineering student passionate about AI/ML and building real-world applications.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rutuja-murkute-087a64231/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Rutujamurkute98)
[![Gmail](https://img.shields.io/badge/Gmail-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rutujamurkute98@gmail.com)

---

<div align="center">

⭐ **Star this repo if you found it helpful!** ⭐

*Built with ❤️ using Python, Scikit-Learn & Flask*

</div>
