import pandas as pd

print("Veri seti yükleniyor...")
# Büyük veri setini test etmek için ilk 5000 satırı okuyoruz
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv", nrows=5000)

print(f"Toplam {len(df)} satır yüklendi. Sütunlar:")
print(df.columns)

import pandas as pd

print("Veri seti yükleniyor ve lexical özellikler filtreleniyor...")

# 1. Büyük veri setini yüklüyoruz (test amaçlı ilk 5000 satır)
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv", nrows=5000)

# 2. Sadece URL-only (lexical) özellikler ile target (label) sütununu seçiyoruz
# Bu sütunlar URL'in kendi yapısını (uzunluk, özel karakterler, HTTPS vb.) temsil eder.
selected_features = [
    'URL', 
    'URLLength', 
    'DomainLength', 
    'IsDomainIP', 
    'NoOfSubDomain', 
    'HasObfuscation', 
    'NoOfObfuscatedChar', 
    'ObfuscationRatio', 
    'NoOfLettersInURL', 
    'LetterRatioInURL', 
    'NoOfDegitsInURL', 
    'DegitRatioInURL', 
    'NoOfEqualsInURL', 
    'NoOfQMarkInURL', 
    'NoOfAmpersandInURL', 
    'NoOfOtherSpecialCharsInURL', 
    'SpacialCharRatioInURL', 
    'IsHTTPS', 
    'label'
]

# Sadece bu sütunları filtreleyip yeni bir DataFrame oluşturuyoruz
df_filtered = df[selected_features]

print(f"Toplam {len(df_filtered)} satır ve {len(df_filtered.columns)} seçilen sütun ile filtrelendi.")
print("Seçilen Sütunlar:")
print(df_filtered.columns.tolist())

# HTML veya dış ağ bağımlı yasaklı kelimelerin listede olup olmadığını kontrol edelim
forbidden_keywords = ['LineOfCode', 'NoOfiFrame', 'NoOfJS', 'NoOfCSS', 'Title']

for col in forbidden_keywords:
    if col in df_filtered.columns:
        print(f"UYARI: Yasaklı bir sütun listede bulundu: {col}")
    else:
        print(f"DOĞRULAMA BAŞARILI: '{col}' sütunu filtrelenip başarıyla atıldı.")


# 3. Adım: Eksik Veri (NaN / Null) Kontrolü ve Temizliği
print("\nEksik veri kontrolü yapılıyor...")

# Her sütunda kaç tane eksik (NaN) değer olduğunu kontrol ediyoruz
missing_values = df_filtered.isnull().sum()
print("Sütunlardaki eksik veri sayıları:")
print(missing_values[missing_values > 0])

# Eğer eksik veri varsa temizleyelim (dropna: eksik satırları veri setinden atar)
initial_row_count = len(df_filtered)
df_clean = df_filtered.dropna()
cleaned_row_count = len(df_clean)

print(f"Temizlik öncesi satır sayısı: {initial_row_count}")
print(f"Temizlik sonrası satır sayısı: {cleaned_row_count}")

if initial_row_count == cleaned_row_count:
    print("Harika! Veri setinde hiç eksik (NaN) veri bulunmuyor, satır kaybı yaşanmadı.")
else:
    print(f"Dikkat: {initial_row_count - cleaned_row_count} adet eksik verili satır temizlendi.")