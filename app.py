import re
import ipaddress
from urllib.parse import urlparse, parse_qs

import tldextract


def url_ozelliklerini_cikar(url):
    ozellikler = {}

    # URL'nin parse edilebilmesi için protokol yoksa geçici olarak ekliyoruz
    parse_edilecek_url = url if "://" in url else "http://" + url
    parsed = urlparse(parse_edilecek_url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    # -------------------------------------------------
    # 1. TEMEL ÖZELLİKLER
    # -------------------------------------------------

    # 1. URL uzunluğu
    ozellikler["uzunluk"] = len(url)

    # 2. HTTPS var mı?
    ozellikler["https_varmi"] = 1 if parsed.scheme.lower() == "https" else 0

    # 3. URL'nin tamamındaki nokta sayısı
    ozellikler["nokta_sayisi"] = url.count(".")

    # 4. @ işareti var mı?
    ozellikler["at_isareti"] = 1 if "@" in url else 0

    # 5. Tire (-) sayısı
    ozellikler["tire_sayisi"] = url.count("-")

    # 6. URL'nin tamamındaki rakam sayısı
    ozellikler["rakam_sayisi"] = sum(c.isdigit() for c in url)

    # 7. Hostname doğrudan IP adresi mi?
    try:
        ipaddress.ip_address(hostname)
        ozellikler["ip_varmi"] = 1
    except ValueError:
        ozellikler["ip_varmi"] = 0

    # 8. Şüpheli kelime var mı?
    supheli_kelimeler = [
        "login",
        "verify",
        "update",
        "security",
        "account",
        "banking",
        "confirm"
    ]

    url_kucuk = url.lower()

    bulunan_supheli_kelimeler = [
        kelime for kelime in supheli_kelimeler
        if kelime in url_kucuk
    ]

    ozellikler["supheli_kelime_varmi"] = (
        1 if bulunan_supheli_kelimeler else 0
    )

    # YENİ: Kaç tane şüpheli kelime var?
    ozellikler["supheli_kelime_sayisi"] = len(bulunan_supheli_kelimeler)

    # -------------------------------------------------
    # 2. GELİŞMİŞ / ANOMALİ ÖZELLİKLERİ
    # -------------------------------------------------

    # 9. Kısaltılmış URL servisi kullanılmış mı?
    kisa_servisler = [
        "bit.ly",
        "t.co",
        "goo.gl",
        "ow.ly",
        "tinyurl.com"
    ]

    ozellikler["kisa_url_varmi"] = 1 if any(
        hostname == servis or hostname.endswith("." + servis)
        for servis in kisa_servisler
    ) else 0

    # 10. Soru işareti (?) var mı?
    ozellikler["soru_isareti_varmi"] = 1 if "?" in url else 0

    # 11. Eşittir (=) var mı?
    ozellikler["esittir_varmi"] = 1 if "=" in url else 0

    # 12. Protokol dışında çift slash var mı?
    govde = url.split("://", 1)[1] if "://" in url else url
    ozellikler["cift_slash_varmi"] = 1 if "//" in govde else 0

    # 13. Subdomain derinliği
    extracted = tldextract.extract(hostname)

    if extracted.subdomain:
        subdomain_parcalari = [
            parca
            for parca in extracted.subdomain.split(".")
            if parca
        ]
        ozellikler["subdomain_derinligi"] = len(subdomain_parcalari)
    else:
        ozellikler["subdomain_derinligi"] = 0

    # -------------------------------------------------
    # ESMA'NIN EKLEDİĞİ YENİ ÖZELLİKLER :)
    # -------------------------------------------------

    # 14. Path uzunluğu
    ozellikler["path_uzunlugu"] = len(path)

    # 15. Hostname/domain tarafının uzunluğu
    ozellikler["hostname_uzunlugu"] = len(hostname)

    # 16. Query parametre sayısı
    query_parametreleri = parse_qs(query)
    ozellikler["query_parametre_sayisi"] = len(query_parametreleri)

    return ozellikler


# -------------------------------------------------
# TEST
# -------------------------------------------------

ornek_guvenli = "https://www.istinye.edu.tr"

ornek_supheli = (
    "http://login.secure.bank.bit.ly/"
    "3xyz?redirect=//hacker.com"
)

print("--- 1. Normal URL Analizi ---")
print(url_ozelliklerini_cikar(ornek_guvenli))

print("\n--- 2. Şüpheli URL Analizi ---")
print(url_ozelliklerini_cikar(ornek_supheli))