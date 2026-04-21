from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
MODELS_DIR = PROJECT_DIR / 'models'

MODEL_PATH = MODELS_DIR / 'rf_smote_enn_tuned_model.joblib'
if not MODEL_PATH.exists():
    raise FileNotFoundError(f'Model file not found: {MODEL_PATH}')

FCOLS_PATH = MODELS_DIR / 'feature_cols.joblib'
if not FCOLS_PATH.exists():
    raise FileNotFoundError(f'Feature columns file not found: {FCOLS_PATH}')

MODEL = joblib.load(MODEL_PATH)
FCOLS = joblib.load(FCOLS_PATH)

LABEL_MAP = {0: "BenignPositive", 1: "MultiStageAttack", 2: "TruePositive"}

SEVERITY_MAP = {
    "BenignPositive":   {"level": "LOW",      "icon": "✅", "action": "False alarm — no action needed. Safe to close this incident."},
    "TruePositive":     {"level": "MEDIUM",   "icon": "⚠️", "action": "Real threat detected — assign to analyst for investigation."},
    "MultiStageAttack": {"level": "CRITICAL", "icon": "🚨", "action": "ACTIVE ATTACK! Escalate immediately. Isolate affected systems."},
}

FORM_OPTIONS = {
    "alert_titles":   ["Malware detected", "Suspicious login attempt", "Ransomware activity", "Phishing email detected", "Brute force attack", "Data exfiltration attempt", "Privilege escalation", "Lateral movement", "Credential theft", "Others"],
    "categories":     ["Malware", "Phishing", "Ransomware", "UnwantedSoftware", "SuspiciousActivity", "Exploit", "General"],
    "entity_types":   ["File", "Process", "RegistryKey", "User", "Ip", "Url", "Mailbox", "MailMessage", "MailCluster", "CloudApplication"],
    "evidence_roles": ["Related", "Impacted", "ContextualEvidence", "Attacker", "Detector"],
    "os_families":    ["Windows", "Linux", "macOS", "Android", "iOS"],
    "country_codes":  ["US", "IN", "GB", "CN", "RU", "DE", "FR", "BR", "AU", "Others"],
    "states":         ["California", "Texas", "New York", "Florida", "Maharashtra", "Others"],
    "cities":         ["New York", "Los Angeles", "Chicago", "Houston", "Mumbai", "Others"],
    "device_names":   ["DESKTOP-001", "SERVER-DB01", "LAPTOP-HR03", "WORKSTATION-FIN", "Others"],
    "account_names":  ["admin", "user01", "svc_account", "guest", "Others"],
}

def build_vector(form):
    X = pd.DataFrame([np.zeros(len(FCOLS))], columns=FCOLS)
    def ohe(prefix, value):
        col = f"{prefix}_{value}"
        if col in X.columns:
            X.at[0, col] = 1.0
    ohe("AlertTitle",   form.get("alert_title",  "Others"))
    ohe("Category",     form.get("category",     "General"))
    ohe("EntityType",   form.get("entity_type",  "File"))
    ohe("EvidenceRole", form.get("evidence_role","Related"))
    ohe("AccountName",  form.get("account_name", "Others"))
    ohe("DeviceName",   form.get("device_name",  "Others"))
    ohe("OSFamily",     form.get("os_family",    "Windows"))
    ohe("CountryCode",  form.get("country_code", "Others"))
    ohe("State",        form.get("state",        "Others"))
    ohe("City",         form.get("city",         "Others"))
    try:
        hour_cols = [c for c in FCOLS if c.startswith("Hour_")]
        day_cols  = [c for c in FCOLS if c.startswith("Day_")]
        if hour_cols: X.at[0, hour_cols[0]] = float(form.get("hour", 12))
        if day_cols:  X.at[0, day_cols[0]]  = float(form.get("day",  15))
    except: pass
    return X.values.astype(np.float32)

@app.route("/")
def index():
    return render_template("index.html", **FORM_OPTIONS)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        form  = request.form.to_dict()
        X     = build_vector(form)
        pred  = int(MODEL.predict(X)[0])
        proba = MODEL.predict_proba(X)[0]
        label = LABEL_MAP[pred]
        sev   = SEVERITY_MAP[label]
        conf  = round(float(proba[pred]) * 100, 1)
        probs = {LABEL_MAP[i]: round(float(p)*100, 1) for i, p in enumerate(proba)}
        return render_template("result.html", label=label, severity=sev, confidence=conf, class_probs=probs, form_data=form)
    except Exception as e:
        return render_template("result.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)