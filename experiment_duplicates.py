import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix

print("1. Veri seti yükleniyor...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

raw_count = len(df)
print(f"Toplam Satır Sayısı: {raw_count}")

# 2. Duplicate (Tekrar eden) URL'leri temizleme
df_clean = df.drop_duplicates(subset=['URL']).copy()
clean_count = len(df_clean)
dropped_count = raw_count - clean_count

print(f"Temizlenen Duplicate URL Sayısı: {dropped_count}")
print(f"Kalan Satır Sayısı: {clean_count}")

# 3. Metin Sütunlarını Temizleme ve Sadece Sayısal (Numeric) Özellikleri Seçme
y = df_clean['label']
groups = df_clean['Domain']

# Hedef ve grup sütunlarını çıkarıp sadece sayısal olan özellikleri (features) otomatik alıyoruz
X_raw = df_clean.drop(columns=['label', 'Domain', 'URL', 'FILENAME', 'TLD', 'Title'], errors='ignore')
X = X_raw.select_dtypes(include=['number'])

# 4. Domain-Aware Split (GroupShuffleSplit)
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print(f"\nTrain Kümesi: {len(X_train)} | Test Kümesi: {len(X_test)}")

# 5. Modellerin Tanımlanması
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "XGBoost": xgb.XGBClassifier(eval_metric='logloss', random_state=42, n_jobs=-1)
}

print("\n--- 4 MODEL İÇİN DUPLICATE SONRASI SONUÇLAR ---")
results = []

for name, model in models.items():
    print(f"\n{name} eğitiliyor...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    # Label Sözlüğü: 0 = Phishing, 1 = Legitimate
    phishing_missed = cm[0][1] # False Positive (Phishing iken Legitimate denmiş)
    false_alarm = cm[1][0]     # False Negative (Legitimate iken Phishing denmiş)
    
    results.append({
        "Model": name,
        "Accuracy": f"%{acc * 100:.2f}",
        "Kaçırılan Phishing (0->1)": phishing_missed,
        "Yanlış Alarm (1->0)": false_alarm
    })

# 6. Tabloyu Yazdırma
results_df = pd.DataFrame(results)
print("\n" + "="*60)
print("DUPLICATE TEMİZLİĞİ SONRASI KARŞILAŞTIRMA TABLOSU")
print("="*60)
print(results_df.to_string(index=False))