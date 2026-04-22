from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
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
FCOLS_SET = set(FCOLS)

LABEL_MAP = {0: "BenignPositive", 1: "MultiStageAttack", 2: "TruePositive"}

SEVERITY_MAP = {
    "BenignPositive":   {"level": "LOW",      "icon": "✅", "action": "False alarm — no action needed. Safe to close this incident."},
    "TruePositive":     {"level": "MEDIUM",   "icon": "⚠️", "action": "Real threat detected — assign to analyst for investigation."},
    "MultiStageAttack": {"level": "CRITICAL", "icon": "🚨", "action": "ACTIVE ATTACK! Escalate immediately. Isolate affected systems."},
}

def _feature_values(prefix):
    vals = [str(c).split(f"{prefix}_", 1)[1] for c in FCOLS if str(c).startswith(f"{prefix}_")]
    def sort_key(v):
        return (v == "Others", int(v) if v.isdigit() else v.lower())
    return sorted(vals, key=sort_key)

def _feature_default(prefix, fallback="Others"):
    vals = _feature_values(prefix)
    if fallback in vals:
        return fallback
    return vals[0] if vals else fallback

PREFIX_DEFAULTS = {
    "AlertTitle": _feature_default("AlertTitle", "Others"),
    "Category": _feature_default("Category", "Malware"),
    "EntityType": _feature_default("EntityType", "File"),
    "EvidenceRole": _feature_default("EvidenceRole", "Related"),
    "AccountName": _feature_default("AccountName", "Others"),
    "DeviceName": _feature_default("DeviceName", "Others"),
    "OSFamily": _feature_default("OSFamily", "Others"),
    "CountryCode": _feature_default("CountryCode", "Others"),
    "State": _feature_default("State", "Others"),
    "City": _feature_default("City", "Others"),
}

# UI labels remain human-readable; values are mapped to encoded model tokens internally.
VALUE_ALIASES = {
    "AlertTitle": {
        "Malware detected": "1",
        "Suspicious login attempt": "2",
        "Ransomware activity": "3",
        "Phishing email detected": "4",
        "Brute force attack": "2",
        "Data exfiltration attempt": "4",
        "Privilege escalation": "3",
        "Lateral movement": "3",
        "Credential theft": "2",
        "Others": "Others",
    },
    "Category": {
        "Phishing": "InitialAccess",
        "General": "SuspiciousActivity",
    },
    "EvidenceRole": {
        "Impacted": "Related",
        "ContextualEvidence": "Related",
        "Attacker": "Related",
        "Detector": "Related",
    },
    "OSFamily": {
        "Windows": "1",
        "Linux": "2",
        "macOS": "3",
        "Android": "4",
        "iOS": "5",
    },
    "AccountName": {
        "admin": "1",
        "user01": "2",
        "svc_account": "3",
        "guest": "453297",
        "Others": "Others",
    },
    "DeviceName": {
        "DESKTOP-001": "1",
        "SERVER-DB01": "4",
        "LAPTOP-HR03": "5",
        "WORKSTATION-FIN": "153085",
        "Others": "Others",
    },
    "CountryCode": {
        "US": "1",
        "IN": "2",
        "GB": "4",
        "CN": "242",
        "RU": "242",
        "DE": "4",
        "FR": "4",
        "BR": "2",
        "AU": "1",
        "Others": "Others",
    },
    "State": {
        "California": "1",
        "Texas": "2",
        "New York": "3",
        "Florida": "1445",
        "Maharashtra": "1445",
        "Others": "Others",
    },
    "City": {
        "New York": "1",
        "Los Angeles": "2",
        "Chicago": "3",
        "Houston": "10630",
        "Mumbai": "10630",
        "Others": "Others",
    },
}

FORM_OPTIONS = {
    "alert_titles": ["Malware detected", "Suspicious login attempt", "Ransomware activity", "Phishing email detected", "Brute force attack", "Data exfiltration attempt", "Privilege escalation", "Lateral movement", "Credential theft", "Others"],
    "categories": ["Malware", "Phishing", "Ransomware", "UnwantedSoftware", "SuspiciousActivity", "Exploit", "General"],
    "entity_types": ["File", "Process", "RegistryKey", "User", "Ip", "Url", "Mailbox", "MailMessage", "MailCluster", "CloudApplication"],
    "evidence_roles": ["Related", "Impacted", "ContextualEvidence", "Attacker", "Detector"],
    "os_families": ["Windows", "Linux", "macOS", "Android", "iOS"],
    "country_codes": ["US", "IN", "GB", "CN", "RU", "DE", "FR", "BR", "AU", "Others"],
    "states": ["California", "Texas", "New York", "Florida", "Maharashtra", "Others"],
    "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Mumbai", "Others"],
    "device_names": ["DESKTOP-001", "SERVER-DB01", "LAPTOP-HR03", "WORKSTATION-FIN", "Others"],
    "account_names": ["admin", "user01", "svc_account", "guest", "Others"],
}

HOUR_VALUES = [v for v in _feature_values("Hour") if v.isdigit()]
DAY_VALUES = [v for v in _feature_values("Day") if v.isdigit()]

def build_vector(form):
    X = pd.DataFrame([np.zeros(len(FCOLS), dtype=np.float32)], columns=FCOLS)

    def resolve_value(prefix, raw_value):
        text = str(raw_value).strip()
        aliases = VALUE_ALIASES.get(prefix, {})
        if text in aliases:
            return aliases[text]
        lower_text = text.lower()
        for key, val in aliases.items():
            if key.lower() == lower_text:
                return val
        return text

    def ohe(prefix, value):
        text = str(resolve_value(prefix, value)).strip()
        candidates = [text, text.lower(), text.upper(), text.title()]
        for cand in candidates:
            col = f"{prefix}_{cand}"
            if col in FCOLS_SET:
                X.at[0, col] = 1.0
                return
        fallback_col = f"{prefix}_{PREFIX_DEFAULTS[prefix]}"
        if fallback_col in FCOLS_SET:
            X.at[0, fallback_col] = 1.0

    ohe("AlertTitle",   form.get("alert_title",   PREFIX_DEFAULTS["AlertTitle"]))
    ohe("Category",     form.get("category",      PREFIX_DEFAULTS["Category"]))
    ohe("EntityType",   form.get("entity_type",   PREFIX_DEFAULTS["EntityType"]))
    ohe("EvidenceRole", form.get("evidence_role", PREFIX_DEFAULTS["EvidenceRole"]))
    ohe("AccountName",  form.get("account_name",  PREFIX_DEFAULTS["AccountName"]))
    ohe("DeviceName",   form.get("device_name",   PREFIX_DEFAULTS["DeviceName"]))
    ohe("OSFamily",     form.get("os_family",     PREFIX_DEFAULTS["OSFamily"]))
    ohe("CountryCode",  form.get("country_code",  PREFIX_DEFAULTS["CountryCode"]))
    ohe("State",        form.get("state",         PREFIX_DEFAULTS["State"]))
    ohe("City",         form.get("city",          PREFIX_DEFAULTS["City"]))

    try:
        hour = str(int(form.get("hour", 12)))
    except Exception:
        hour = "12"
    try:
        day = str(int(form.get("day", 15)))
    except Exception:
        day = "15"
    ohe("Hour", hour if hour in HOUR_VALUES else (HOUR_VALUES[0] if HOUR_VALUES else "0"))
    ohe("Day", day if day in DAY_VALUES else (DAY_VALUES[0] if DAY_VALUES else "1"))

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
        label = LABEL_MAP.get(pred, f"Class_{pred}")
        sev   = SEVERITY_MAP[label]
        class_prob = {int(c): float(p) for c, p in zip(MODEL.classes_, proba)}
        conf  = round(class_prob.get(pred, 0.0) * 100, 1)
        probs = {LABEL_MAP.get(int(c), f"Class_{int(c)}"): round(float(p) * 100, 1) for c, p in zip(MODEL.classes_, proba)}
        return render_template("result.html", label=label, severity=sev, confidence=conf, class_probs=probs, form_data=form)
    except Exception as e:
        return render_template("result.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)