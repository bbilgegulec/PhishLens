import pandas as pd

print("Veri seti yükleniyor...")
# Büyük veri setini test etmek için ilk 5000 satırı okuyoruz
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv", nrows=5000)

print(f"Toplam {len(df)} satır yüklendi. Sütunlar:")
print(df.columns)