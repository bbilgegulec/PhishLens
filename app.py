import re

def url_ozelliklerini_cikar(url):
    ozellikler = {}
    
    # --- 1. TEMEL ÖZELLİKLER ---
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
    
    # 8. Şüpheli kelimeler var mı?
    supheli_kelimeler = ["login", "verify", "update", "security", "account", "banking", "confirm"]
    ozellikler["supheli_kelime_varmi"] = 1 if any(kelime in url.lower() for kelime in supheli_kelimeler) else 0

    # --- 2. GELİŞMİŞ / ANOMALİ ÖZELLİKLERİ ---
    # 9. Kısaltılmış URL servisi kullanılmış mı? (bit.ly vb.)
    kisa_servisler = ["bit.ly", "t.co", "goo.gl", "ow.ly", "tinyurl"]
    ozellikler["kisa_url_varmi"] = 1 if any(servis in url.lower() for servis in kisa_servisler) else 0
    
    # 10. Soru işareti (?) var mı? (Veri taşıma/parametre hilesi)
    ozellikler["soru_isareti_varmi"] = 1 if "?" in url else 0
    
    # 11. Eşittir (=) var mı?
    ozellikler["esittir_varmi"] = 1 if "=" in url else 0
    
    # 12. Yan yana çift slash (//) yönlendirme hilesi var mı? (Gövde kısmında)
    govde = url[8:] if url.startswith("https://") else (url[7:] if url.startswith("http://") else url)
    ozellikler["cift_slash_varmi"] = 1 if "//" in govde else 0
    
    # 13. Subdomain (Alt Alan Adı) Derinliği
    # Protokolü temizleyip noktaya göre bölüyoruz, parça sayısı bize derinliği veriyor
    temiz_url = url.replace("https://", "").replace("http://", "")
    parcalar = temiz_url.split("/")[0].split(".") # Önce ana domain/path ayrımını yapıp noktaları sayıyoruz
    ozellikler["subdomain_derinligi"] = len(parcalar)
    
    return ozellikler

# Test edelim
ornek_guvenli = "https://www.istinye.edu.tr"
ornek_supheli = "http://login.secure.bank.bit.ly/3xyz?redirect=//hacker.com"

print("--- 1. Normal URL Analizi ---")
print(url_ozelliklerini_cikar(ornek_guvenli))

print("\n--- 2. Gelişmiş Şüpheli URL Analizi ---")
print(url_ozelliklerini_cikar(ornek_supheli))