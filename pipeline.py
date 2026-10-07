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