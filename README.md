<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5b2fb8b4-d5aa-4533-afd1-b511fdd82e59" /><div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d3a5c,100:00d4ff&height=200&section=header&text=Cybersecurity%20Threat%20Classifier&fontSize=36&fontColor=ffffff&fontAlignY=38&desc=AI-Powered%20SOC%20Incident%20Triage%20Engine&descAlignY=58&descSize=16" width="100%"/>

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-FFD43B?style=flat-square&logo=python&logoColor=blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4.0-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-FF6600?style=flat-square)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.3.0-02B56A?style=flat-square)](https://lightgbm.readthedocs.io)
[![Dataset](https://img.shields.io/badge/Dataset-Microsoft%20GUIDE-0078D4?style=flat-square&logo=microsoft)](https://microsoft.com)

</div>

<div align="center">

![Records](https://img.shields.io/badge/Training%20Records-8.9%20Million-ff6b35?style=flat-square)
![Accuracy](https://img.shields.io/badge/Model%20Accuracy-70.45%25-00d4ff?style=flat-square)
![RAM](https://img.shields.io/badge/RAM%20Used-2.3%20GB-brightgreen?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-success?style=flat-square)

</div>

---

## 📸 Application Demo

> **SOC Dashboard — Incident Input Form**

![Dashboard](screenshots/Screenshot__1271_.png)

> **AI Classification Result — Real-time Threat Analysis**

![Result](screenshots/Screenshot__1272_.png)

---

## 🧠 What is this Project?

**Cybersecurity Threat Classifier** is a machine learning system that automatically classifies cybersecurity incidents for Security Operations Center (SOC) analysts. Instead of manually investigating thousands of alerts every day, analysts simply enter incident details and the AI model instantly returns the threat classification.

### Three Output Classes:

| Class | Severity | Meaning | Action |
|-------|----------|---------|--------|
| ✅ BenignPositive | LOW | False alarm | Close the ticket |
| ⚠️ TruePositive | MEDIUM | Real threat | Assign to analyst |
| 🚨 MultiStageAttack | CRITICAL | Active attack | Escalate immediately |

---

## 📊 Dataset

| Property | Details |
|----------|---------|
| Source | Microsoft GUIDE Dataset |
| Train Size | 9,500,000+ rows, 45 columns |
| Test Size | 4,100,000+ rows, 46 columns |
| After Preprocessing | 8,922,805 rows × 154 features |
| Target Column | `IncidentGrade` |
| File Size (Encoded) | ~1.40 GB |

---

## 🏗️ Project Structure

```
Cybersecurity-Threat-Classifier/
│
├── 📓 notebooks/
│   ├── Part_A_Data_Preprocessing_Exploration.ipynb
│   └── Part_B_Modeling_Evaluation_Deployment.ipynb
│
├── 🌐 app/
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   └── models/
│       ├── rf_no_smote_model.joblib
│       ├── rf_smote_tuned_model.joblib
│       └── rf_smote_enn_tuned_model.joblib
│
├── 📸 screenshots/
│   ├── Screenshot__1271_.png
│   └── Screenshot__1272_.png
│
├── requirements.txt
└── README.md
```

---

## 🔄 Workflow

```
Raw CSV (9.5M rows)
       ↓
Chunked Loading → Memory Optimization (500K rows/chunk)
       ↓
Drop columns >50% missing | Drop null IncidentGrade rows
       ↓
Feature Engineering: Timestamp → Year, Month, Day, Hour
       ↓
Drop 22 irrelevant ID columns
       ↓
Group rare categories → "Others" (top 5 per column)
       ↓
Label Encoding (target) + One-Hot Encoding (15 features)
       ↓
Save as encoded_train_data.joblib
       ↓
Index-based 80:20 Split (RAM-safe, no data copy)
       ↓
Train: RF | RF+SMOTE | RF+SMOTEENN
       ↓
Evaluate on Test Data
       ↓
Best Model → Flask Web App
```

---

## 📈 Model Results

### Comparison Table (10% Sample)

| Model | Accuracy | Macro-F1 |
|-------|----------|----------|
| Logistic Regression | 0.6319 | 0.54 |
| Decision Tree | 0.7032 | 0.67 |
| **Random Forest** ⭐ | **0.7045** | **0.67** |
| XGBoost | 0.6794 | 0.62 |
| LightGBM | 0.6773 | 0.61 |

### SMOTE Comparison (2% Sample)

| Strategy | Accuracy | Macro-F1 |
|----------|----------|----------|
| RF + SMOTE | 0.67 | 0.65 |
| **RF No SMOTE** ✅ | **0.68** | **0.65** |
| RF + SMOTEENN | 0.65 | 0.62 |

> **Deployed Model:** `rf_no_smote_model.joblib` — Best accuracy

---

## ⚡ Key Technical Achievement

> Processed **8.9 Million rows** on a machine with only **2.3 GB RAM** — no cloud, no GPU!

| Challenge | Solution |
|-----------|----------|
| Full data load → MemoryError | `mmap_mode='r'` memory-mapped loading |
| `.drop()` crash on large data | Direct column list indexing |
| `train_test_split` RAM crash | `StratifiedShuffleSplit` index-based |
| SMOTE on full data → crash | 2% subsample before resampling |

---

## 🛠️ Tech Stack

```
Language     →  Python 3.10+
ML           →  Scikit-Learn, XGBoost, LightGBM
Resampling   →  Imbalanced-Learn (SMOTE, SMOTEENN)
Data         →  Pandas, NumPy, Joblib
Viz          →  Matplotlib, Seaborn
Web App      →  Flask 3.0
Frontend     →  HTML5, CSS3 (SOC terminal dark theme)
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Rutujamurkute98/Cybersecurity-Threat-Classifier.git
cd Cybersecurity-Threat-Classifier

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app/app.py

# 5. Open in browser
# http://127.0.0.1:5000
```

> **Note:** Model `.joblib` files are not included in the repo due to size (300MB+). Run the notebooks to generate them.

---

## 🌐 Web Application Features

- 🖥️ **SOC-style dark terminal UI** — professional cybersecurity aesthetic
- 📋 **5-section structured form** — Alert, Entity, Device, Location, Timestamp
- ⚡ **Real-time classification** in under 1 second
- 📊 **Confidence score** + probability bars for all 3 classes
- 🚨 **Color-coded severity** — Green / Yellow / Red
- 💾 **RAM-safe prediction** — runs on low-spec machines

---

## 👩‍💻 About

**Rutuja Murkute** — Final Year B.E. Information Technology | CGPA 9.22 | GATE 2025 Qualified

Passionate about building real-world AI/ML applications.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rutuja-murkute-087a64231/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Rutujamurkute98)
[![Gmail](https://img.shields.io/badge/Gmail-Mail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rutujamurkute98@gmail.com)

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00d4ff,100:0d3a5c&height=120&section=footer" width="100%"/>

⭐ **Star this repo if you found it helpful!**

</div>
