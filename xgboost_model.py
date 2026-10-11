import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import xgboost as xgb

print("Veri seti yükleniyor...")
df = pd.read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')

print(f"Toplam {len(df)} satır yüklendi.")

# URL tabanlı özellikler ve label seçimi
selected_features = [
    'URL', 'URLLength', 'DomainLength', 'IsDomainIP', 'NoOfSubDomain', 
    'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio', 
    'NoOfLettersInURL', 'LetterRatioInURL', 'NoOfDegitsInURL', 
    'DegitRatioInURL', 'NoOfEqualsInURL', 'NoOfQMarkInURL', 
    'NoOfAmpersandInURL', 'NoOfOtherSpecialCharsInURL', 
    'SpacialCharRatioInURL', 'IsHTTPS', 'label'
]

df_filtered = df[selected_features].copy()

# Temizlik ve Eksik Veri Kontrolü
df_filtered = df_filtered.drop_duplicates(subset=['URL'])
df_filtered = df_filtered.dropna()

print(f"Temizlik sonrası satır sayısı: {len(df_filtered)}")

# Domain-Aware Train/Test Bölünmesi (GroupShuffleSplit)
# URL'den domain türetme (Örn: https://www.example.com/path -> example.com)
df_filtered['RegistrableDomain'] = df_filtered['URL'].str.extract(r'://([^/]+)')[0]
df_filtered['RegistrableDomain'] = df_filtered['RegistrableDomain'].fillna(df_filtered['URL'])

X = df_filtered.drop(columns=['label', 'URL', 'RegistrableDomain'])
y = df_filtered['label']
groups = df_filtered['RegistrableDomain']

gss = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print(f"Eğitim (Train) kümesi satır sayısı: {len(X_train)}")
print(f"Test kümesi satır sayısı: {len(X_test)}")

# XGBoost Modeli Eğitimi
print("XGBoost modeli eğitiliyor...")
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

xgb_model.fit(X_train, y_train)

# Tahmin ve Metrikler
y_pred = xgb_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)

# Feature Importance (Özellik Önem Düzeyleri)
feature_importances = pd.Series(xgb_model.feature_importances_, index=X_train.columns)
print("\nEn Önemli İlk 5 Özellik (XGBoost):")
print(feature_importances.sort_values(ascending=False).head(5))