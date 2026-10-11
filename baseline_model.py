from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# pipeline.py içinde hazırlanan train/test verilerini alıyoruz
from pipeline import X_train, X_test, y_train, y_test

print("\nLogistic Regression baseline modeli eğitiliyor...")

# İlk baseline modelimizi oluşturuyoruz
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

# Model eğitim verisini öğreniyor
model.fit(X_train, y_train)

# Daha önce görmediği test verisi üzerinde tahmin yapıyor
y_pred = model.predict(X_test)

# Sonuçlar
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Phishing", "Legitimate"]
))