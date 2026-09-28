import re

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
    
    # 7. IP Adresi var mı?
    ip_deseni = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ozellikler["ip_varmi"] = 1 if re.search(ip_deseni, url) else 0
    
    # 8. Şüpheli kelimeler var mı? (login, verify, update, security vb.)
    supheli_kelimeler = ["login", "verify", "update", "security", "account", "banking", "confirm"]
    # URL içinde bu kelimelerden biri geçiyorsa 1, geçmiyorsa 0 yazalım
    ozellikler["supheli_kelime_varmi"] = 1 if any(kelime in url.lower() for kelime in supheli_kelimeler) else 0
    
    return ozellikler

# Test edelim
ornek_guvenli = "https://www.istinye.edu.tr"
ornek_supheli = "http://netflix-hesap-dogrulama-99.xyz/login@update"

print("--- 1. Normal URL Analizi ---")
print(url_ozelliklerini_cikar(ornek_guvenli))

print("\n--- 2. Şüpheli URL Analizi ---")
print(url_ozelliklerini_cikar(ornek_supheli))