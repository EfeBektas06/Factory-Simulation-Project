\# Endüstriyel Üretim Hattı Simülasyonu ve Finansal Analiz 🏭



Bu proje, stokastik (rastgele) süreçlere sahip bir üretim hattını simüle etmek ve finansal risk analizleri gerçekleştirmek için geliştirilmiştir. \*\*Endüstri Mühendisliği\*\* prensipleri (Yöneylem Araştırması) ile \*\*Veri Bilimi\*\* tekniklerini birleştirir.



\##  Projenin Amacı

Geleneksel deterministik (sabit) hesaplamalar, makinelerin arıza yapma olasılıklarını ve üretimdeki dalgalanmaları göz ardı eder. Bu proje:

\* \*\*Monte Carlo Simülasyonu\*\* kullanarak 1000 günlük sanal üretim gerçekleştirir.

\* Makinelerin arıza ve tamir sürelerini \*\*Stokastik\*\* olarak modelleler.

\* Darboğaz (Bottleneck) ve Ara Stok (Buffer) analizleri yapar.

\* Sonuçları \*\*SQL veritabanına\*\* kaydeder ve \*\*Excel\*\* raporu oluşturur.



\##  Kullanılan Teknolojiler

\* \*\*Python\*\* (Ana Programlama Dili)

\* \*\*OOP (Nesne Yönelimli Programlama):\*\* Makinelerin dijital ikizlerinin oluşturulması.

\* \*\*Pandas \& NumPy:\*\* Veri analizi ve istatistiksel hesaplamalar.

\* \*\*SQLite:\*\* Simülasyon verilerinin veritabanında saklanması.

\* \*\*Matplotlib:\*\* Üretim dağılımı ve kâr/zarar grafiklerinin görselleştirilmesi.



\##  Örnek Çıktılar

Simülasyon sonucunda sistem şunları üretir:

1\.  \*\*Dağılım Grafiği:\*\* Üretim kapasitesinin histogramı.

2\.  \*\*Finansal Risk Tablosu:\*\* Hangi günlerin kârlı, hangilerinin zararlı olduğunun analizi.

3\.  \*\*Excel Raporu:\*\* `Simulasyon\\\_Raporu.xlsx` dosyası.

4\.  \*\*Veritabanı:\*\* `fabrika\\\_loglari.db` dosyası (SQL sorgulamaları için).



\##  Nasıl Çalıştırılır?



1\. Gerekli kütüphaneleri yükleyin:

   ```bash

   pip install -r requirements.txt

