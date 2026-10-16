from pipeline import X_train, X_test, y_train, y_test

import pandas as pd
import xgboost as xgb

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)


print("\nXGBoost modeli eğitiliyor...")


# Bilge'nin kullandığı XGBoost ayarlarını aynen koruyoruz.
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss"
)


# Modeli aynı eğitim verisiyle eğitiyoruz.
xgb_model.fit(X_train, y_train)


# Aynı test kümesinde tahmin yaptırıyoruz.
y_pred = xgb_model.predict(X_test)


# Performans sonuçları
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)


print(f"\nAccuracy: {accuracy:.4f}")

print("\nConfusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(class_report)


# XGBoost hangi özelliklere daha çok önem vermiş?
feature_importances = pd.Series(
    xgb_model.feature_importances_,
    index=X_train.columns
)

print("\nEn Önemli İlk 5 Özellik (XGBoost):")
print(
    feature_importances
    .sort_values(ascending=False)
    .head(5)
)