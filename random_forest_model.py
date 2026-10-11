from pipeline import X_train, X_test, y_train, y_test
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd

print("Random Forest modeli eğitiliyor...")

# 1. Modelin Kurulumu (Hyperparameters)
# n_estimators=100: Modelin içinde 100 adet bağımsız Karar Ağacı (Decision Tree) olacağını belirtir.
# random_state=42: Her çalıştırdığımızda aynı rastgeleliği vererek sonuçların tekrarlanabilir olmasını sağlar.
# n_jobs=-1: Bilgisayarın tüm işlemci çekirdeklerini kullanarak eğitimi hızlandırır (büyük veri setinde hayat kurtarır).
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

# 2. Modelin Eğitilmesi (Fit)
rf_model.fit(X_train, y_train)

# 3. Test Kümesi Üzerinden Tahmin Yapılması
y_pred = rf_model.predict(X_test)

# 4. Performans Metriklerinin Hesaplanması
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nConfusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(class_report)

# 5. Feature Importance (Özellik Önem Düzeyleri) Analizi
# Modelin karar verirken en çok hangi özelliklere baktığını görelim
feature_importances = pd.Series(rf_model.feature_importances_, index=X_train.columns)
#Random Forest, kararları verirken hangi sütunları en çok kullandığının istatistiğini tutar.
print("\nEn Önemli İlk 5 Özellik:")
print(feature_importances.sort_values(ascending=False).head(5))