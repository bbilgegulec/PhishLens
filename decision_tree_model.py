from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from pipeline import X_train, X_test, y_train, y_test


print("\nDecision Tree modeli eğitiliyor...")

# Tek bir karar ağacı oluşturuyoruz.
# Şimdilik özel ayar yapmıyoruz; önce modelin doğal halini görmek istiyoruz.
model = DecisionTreeClassifier(
    random_state=42
)

# Model eğitim verisinden örüntüleri öğreniyor.
model.fit(X_train, y_train)

# Model daha önce görmediği test verileri için tahmin yapıyor.
y_pred = model.predict(X_test)


# Genel doğruluk oranı
accuracy = accuracy_score(y_test, y_pred)

# Veri setimizde 0 = phishing olduğu için
# phishing sınıfını özellikle 0 olarak değerlendiriyoruz.
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


print(f"\nAccuracy: {accuracy:.4f}")
print(f"Phishing Precision: {phishing_precision:.4f}")
print(f"Phishing Recall: {phishing_recall:.4f}")
print(f"Phishing F1: {phishing_f1:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))