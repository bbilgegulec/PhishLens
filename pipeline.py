import pandas as pd
import tldextract
import ipaddress
from urllib.parse import urlparse

print("Veri seti yükleniyor...")
# Büyük veri setini test etmek için ilk 5000 satırı okuyoruz
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv", nrows=5000)

print(f"Toplam {len(df)} satır yüklendi. Sütunlar:")
print(df.columns)



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
df_filtered = df[selected_features].copy()

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

# Duplicate URL kontrolü
duplicate_count = df_filtered['URL'].duplicated().sum()

print(
    f"\nTekrarlanan URL sayısı: {duplicate_count}"
)

# Aynı URL farklı label almış mı?
label_conflicts = (
    df_filtered.groupby('URL')['label']
    .nunique()
)

conflict_count = (label_conflicts > 1).sum()

print(
    f"Çelişkili label içeren URL sayısı: {conflict_count}"
)

if conflict_count > 0:
    raise ValueError(
        "Aynı URL için farklı label değerleri bulundu!"
    )
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


print("\nDomain-Aware Train/Test Bölünmesi (GroupShuffleSplit) hazırlanıyor...")

# 1. URL'lerden domain bilgisini (grup anahtarını) çıkartıyoruz
# Örn: "http://www.example.com/path" -> "example.com"
def extract_domain(url):
    url = str(url).strip()

    if "://" not in url:
        url = "http://" + url

    parsed = urlparse(url)

    hostname = (parsed.hostname or "").lower().rstrip(".")

    if not hostname:
        return "unknown"

    # Host bir IP adresiyse aynen grup olarak kullan
    try:
        ipaddress.ip_address(hostname)
        return hostname
    except ValueError:
        pass

    extracted = tldextract.extract(hostname)

    domain = extracted.top_domain_under_public_suffix

    return domain if domain else hostname

# Temizlenmiş veri seti üzerinden domain gruplarını oluşturalım
df_clean['DomainGroup'] = df_clean['URL'].apply(extract_domain)

# 2. Özellikler (X), Etiket (y) ve Gruplar (groups) olarak ayıralım
# 'URL' ve 'label' ve 'DomainGroup' sütunlarını X'ten çıkarıyoruz (model sadece sayısal lexical özelliklerle öğrenecek)
X = df_clean.drop(columns=['URL', 'label', 'DomainGroup'])
y = df_clean['label']
groups = df_clean['DomainGroup']
# 4. Label / sınıf dağılımı kontrolü
print("\nGenel veri seti label dağılımı:")

label_counts = y.value_counts().sort_index()
label_ratios = y.value_counts(normalize=True).sort_index()

print("Sayılar:")
print(label_counts)

print("\nOranlar:")
print(label_ratios)

# PhiUSIIL veri setinde:
# 0 = Phishing
# 1 = Legitimate

# 3. GroupShuffleSplit ile %80 Train, %20 Test (Domain bazlı sızdırmasız bölme)
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

train_idx, test_idx = next(gss.split(X, y, groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
# Train ve Test sınıf dağılımlarını kontrol edelim
print("\nTrain label dağılımı:")
print(y_train.value_counts(normalize=True).sort_index())

print("\nTest label dağılımı:")
print(y_test.value_counts(normalize=True).sort_index())

# Her iki kümede de iki sınıfın bulunduğunu doğrulayalım
assert y_train.nunique() == 2, (
    "HATA: Train kümesinde iki sınıf da bulunmuyor!"
)

assert y_test.nunique() == 2, (
    "HATA: Test kümesinde iki sınıf da bulunmuyor!"
)

print(
    "DOĞRULAMA BAŞARILI: "
    "Train ve Test kümelerinde phishing ve legitimate sınıfları mevcut."
)

train_domains = set(groups.iloc[train_idx])
test_domains = set(groups.iloc[test_idx])

print("\nTrain label dağılımı:")
print(y_train.value_counts(normalize=True).sort_index())

print("\nTest label dağılımı:")
print(y_test.value_counts(normalize=True).sort_index())

domain_overlap = train_domains.intersection(test_domains)

print(
    f"Train/Test ortak domain sayısı: {len(domain_overlap)}"
)

assert len(domain_overlap) == 0, (
    "HATA: Train ve Test arasında domain sızıntısı var!"
)

print(
    "DOĞRULAMA BAŞARILI: "
    "Train ve Test arasında domain overlap yok."
)
print(f"Eğitim (Train) kümesi satır sayısı: {len(X_train)}")
print(f"Test kümesi satır sayısı: {len(X_test)}")
print("BAŞARILI: Domain-aware split (gruplu veri bölünmesi) tamamlandı! Hiçbir domain iki tarafa da aynı anda sızmadı.")

