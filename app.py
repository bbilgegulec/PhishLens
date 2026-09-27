import re  # Python'un metin içinde kalıp arama kütüphanesi

def url_ozelliklerini_cikar(url):
    ozellikler = {}
    
    # 1. URL Uzunluğu
    ozellikler["uzunluk"] = len(url)
    
    # 2. HTTPS protokolü var mı? (1: Evet, 0: Hayır)
    ozellikler["https_varmi"] = 1 if url.startswith("https://") else 0
    
    # 3. Nokta sayısı
    ozellikler["nokta_sayisi"] = url.count(".")
    
    # 4. '@' işareti var mı?
    ozellikler["at_isareti"] = 1 if "@" in url else 0
    
    # 5. Tire (-) sayısı
    ozellikler["tire_sayisi"] = url.count("-")
    
    # 6. Rakam sayısı
    ozellikler["rakam_sayisi"] = sum(c.isdigit() for c in url)
    
    # 7. IP Adresi var mı? (Standart IP formatı arıyoruz: örn. 192.168.1.1)
    ip_deseni = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ozellikler["ip_varmi"] = 1 if re.search(ip_deseni, url) else 0
    
    return ozellikler

# Test edelim: Biri normal site, diğeri doğrudan IP adresli şüpheli site
ornek_guvenli = "https://www.istinye.edu.tr"
ornek_ip_li = "http://192.168.1.50/netflix/login.html"

print("--- 1. Normal URL Analizi ---")
print(ornek_guvenli)
print(url_ozelliklerini_cikar(ornek_guvenli))

print("\n--- 2. IP Adresi İçeren Şüpheli URL Analizi ---")
print(ornek_ip_li)
print(url_ozelliklerini_cikar(ornek_ip_li))