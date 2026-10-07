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

from sklearn.model_selection import GroupShuffleSplit
import urllib.parse

print("\nDomain-Aware Train/Test Bölünmesi (GroupShuffleSplit) hazırlanıyor...")

# 1. URL'lerden domain bilgisini (grup anahtarını) çıkartıyoruz
# Örn: "http://www.example.com/path" -> "example.com"
def extract_domain(url):
    try:
        parsed_url = urllib.parse.urlparse(str(url))
        netloc = parsed_url.netloc
        if not netloc:
            # Eğer şeması yoksa başına http ekleyip tekrar deneyelim
            parsed_url = urllib.parse.urlparse("http://" + str(url))
            netloc = parsed_url.netloc
        # www. kısmını temizleyip saf domain elde edelim
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc.split(':')[0] # Port numarasını ayıkla
    except:
        return "unknown"

# Temizlenmiş veri seti üzerinden domain gruplarını oluşturalım
df_clean['DomainGroup'] = df_clean['URL'].apply(extract_domain)

# 2. Özellikler (X), Etiket (y) ve Gruplar (groups) olarak ayıralım
# 'URL' ve 'label' ve 'DomainGroup' sütunlarını X'ten çıkarıyoruz (model sadece sayısal lexical özelliklerle öğrenecek)
X = df_clean.drop(columns=['URL', 'label', 'DomainGroup'])
y = df_clean['label']
groups = df_clean['DomainGroup']

# 3. GroupShuffleSplit ile %80 Train, %20 Test (Domain bazlı sızdırmasız bölme)
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

train_idx, test_idx = next(gss.split(X, y, groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print(f"Eğitim (Train) kümesi satır sayısı: {len(X_train)}")
print(f"Test kümesi satır sayısı: {len(X_test)}")
print("BAŞARILI: Domain-aware split (gruplu veri bölünmesi) tamamlandı! Hiçbir domain iki tarafa da aynı anda sızmadı.")

