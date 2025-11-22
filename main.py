import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# =============================================================================
# PROJE: Endüstriyel Üretim Hattı Simülasyonu (Dijital İkiz)
# YAZAN: [EFE BEKTAŞ]
# AÇIKLAMA: Monte Carlo yöntemi ile üretim hattı darboğaz, kapasite ve finansal risk analizi.
# =============================================================================

# --- SİMÜLASYON PARAMETRELERİ ---
SIMULASYON_GUN_SAYISI = 1000
VARDIYA_SURESI_DK = 480
URUN_SATIS_FIYATI = 150
HAMMADDE_MALIYETI = 40
ISLETME_MALIYETI_SAATLIK = 500
ARIZA_BAKIM_MALIYETI = 200


# ==========================================
# 1. CLASS YAPISI (OOP - Dijital İkiz)
# ==========================================
class Makine:
    def __init__(self, isim, islem_suresi, ariza_ihtimali, tamir_suresi):
        self.isim = isim
        self.islem_suresi = islem_suresi
        self.ariza_ihtimali = ariza_ihtimali
        self.tamir_suresi = tamir_suresi

        # Durum Değişkenleri (State)
        self.kalan_sure = 0
        self.arizali_mi = False
        self.tamir_kalan = 0
        self.toplam_ariza_sayisi = 0

    def dakika_ilerlet(self, hammadde_var_mi):
        # 1. Durum: Arıza
        if self.arizali_mi:
            self.tamir_kalan -= 1
            if self.tamir_kalan <= 0:
                self.arizali_mi = False
            return 0

        # 2. Durum: Yeni İş Alma
        if self.kalan_sure <= 0:
            if hammadde_var_mi:
                # Stokastik Arıza Kontrolü
                if random.random() < self.ariza_ihtimali:
                    self.arizali_mi = True
                    self.toplam_ariza_sayisi += 1
                    self.tamir_kalan = self.tamir_suresi
                    return 0
                else:
                    self.kalan_sure = self.islem_suresi
                    return 0
            else:
                return 0  # Hammadde yok, bekleme (Starvation)

        # 3. Durum: Çalışma
        else:
            self.kalan_sure -= 1
            if self.kalan_sure <= 0:
                return 1  # Üretim Bitti
            else:
                return 0


# ==========================================
# 2. SİMÜLASYON MOTORU
# ==========================================
def gunluk_simulasyon_yap():
    # Senaryo: Hızlı (4dk) ama Hassas Hat
    m1 = Makine("Kesim", islem_suresi=4, ariza_ihtimali=0.02, tamir_suresi=15)
    m2 = Makine("Montaj", islem_suresi=5, ariza_ihtimali=0.01, tamir_suresi=10)

    ara_stok = 0
    biten_urun = 0

    for _ in range(VARDIYA_SURESI_DK):
        # M1 Aksiyonu
        if m1.dakika_ilerlet(hammadde_var_mi=True) == 1:
            ara_stok += 1

        # M2 Aksiyonu (Ara stok kontrolü)
        hammadde_var = True if ara_stok > 0 else False

        # Blocking/Starvation Mantığı
        if not m2.arizali_mi and m2.kalan_sure <= 0 and hammadde_var:
            ara_stok -= 1

        if m2.dakika_ilerlet(hammadde_var_mi=hammadde_var) == 1:
            biten_urun += 1

    return {
        "Uretim_Adedi": biten_urun,
        "M1_Ariza_Sayisi": m1.toplam_ariza_sayisi,
        "M2_Ariza_Sayisi": m2.toplam_ariza_sayisi
    }


# ==========================================
# 3. MONTE CARLO VE VERİ ANALİZİ
# ==========================================
if __name__ == "__main__":
    print(f" Simülasyon Başlatılıyor... ({SIMULASYON_GUN_SAYISI} Gün)")

    veri_listesi = []

    for i in range(SIMULASYON_GUN_SAYISI):
        sonuc = gunluk_simulasyon_yap()

        # Finansal Hesaplamalar
        gelir = sonuc["Uretim_Adedi"] * URUN_SATIS_FIYATI
        gider_hammadde = sonuc["Uretim_Adedi"] * HAMMADDE_MALIYETI
        gider_isletme = (VARDIYA_SURESI_DK / 60) * ISLETME_MALIYETI_SAATLIK
        gider_ariza = (sonuc["M1_Ariza_Sayisi"] + sonuc["M2_Ariza_Sayisi"]) * ARIZA_BAKIM_MALIYETI

        toplam_gider = gider_hammadde + gider_isletme + gider_ariza
        net_kar = gelir - toplam_gider

        veri_listesi.append({
            "Gun_ID": i + 1,
            "Uretim": sonuc["Uretim_Adedi"],
            "Gelir": gelir,
            "Gider": toplam_gider,
            "Net_Kar": net_kar,
            "Ariza_Toplami": sonuc["M1_Ariza_Sayisi"] + sonuc["M2_Ariza_Sayisi"]
        })

    df = pd.DataFrame(veri_listesi)

    # --- EXCEL ÇIKTISI ---
    try:
        df.to_excel("Simulasyon_Raporu.xlsx", index=False)
        print(" Excel raporu oluşturuldu.")
    except:
        print(" Excel kütüphanesi eksik olabilir, atlanıyor.")

    # --- SQL ENTEGRASYONU ---
    print(" Veriler SQL Veritabanına (SQLite) işleniyor...")
    baglanti = sqlite3.connect('fabrika_loglari.db')
    imlec = baglanti.cursor()

    imlec.execute("""
        CREATE TABLE IF NOT EXISTS Gunluk_Uretim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gun_no INTEGER,
            uretim_adedi INTEGER,
            net_kar REAL,
            durum TEXT
        )
    """)
    imlec.execute("DELETE FROM Gunluk_Uretim")  # Temiz başlangıç

    for index, satir in df.iterrows():
        durum = "KAR" if satir["Net_Kar"] > 0 else "ZARAR"
        imlec.execute("""
            INSERT INTO Gunluk_Uretim (gun_no, uretim_adedi, net_kar, durum)
            VALUES (?, ?, ?, ?)
        """, (satir["Gun_ID"], satir["Uretim"], satir["Net_Kar"], durum))

    baglanti.commit()
    baglanti.close()
    print(" SQL Kaydı Tamamlandı.")

    # --- GÖRSELLEŞTİRME ---
    print(" Grafikler oluşturuluyor...")
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.hist(df["Uretim"], color='#3498db', edgecolor='black', bins=20)
    plt.axvline(df["Uretim"].mean(), color='red', linestyle='dashed', label='Ortalama')
    plt.title(f'Üretim Dağılımı (Ort: {df["Uretim"].mean():.1f})')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.scatter(df.index, df["Net_Kar"], c=['red' if x < 0 else 'green' for x in df["Net_Kar"]], s=10, alpha=0.6)
    plt.axhline(0, color='black', linestyle='--')
    plt.title('Finansal Risk Analizi (Kâr/Zarar)')

    plt.tight_layout()
    plt.show()

