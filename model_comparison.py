from pipeline import X_train, X_test, y_train, y_test

import pandas as pd
import xgboost as xgb

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        eval_metric="logloss"
    )
}


results = []


for model_name, model in models.items():

    print(f"\n{model_name} eğitiliyor...")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    phishing_precision = precision_score(
        y_test,
        y_pred,
        pos_label=0
    )

    phishing_recall = recall_score(
        y_test,
        y_pred,
        pos_label=0
    )

    phishing_f1 = f1_score(
        y_test,
        y_pred,
        pos_label=0
    )

    cm = confusion_matrix(y_test, y_pred)

    phishing_detected = cm[0, 0]
    phishing_missed = cm[0, 1]
    false_alarm = cm[1, 0]

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Phishing Precision": phishing_precision,
        "Phishing Recall": phishing_recall,
        "Phishing F1": phishing_f1,
        "Phishing Detected": phishing_detected,
        "Phishing Missed": phishing_missed,
        "False Alarm": false_alarm
    })


results_df = pd.DataFrame(results)

print("\n")
print("=" * 100)
print("MODEL KARŞILAŞTIRMA SONUÇLARI")
print("=" * 100)

print(results_df.to_string(index=False))