```markdown
# 📡 DepremApp - Son Depremleri Anlık Takip Et!

**DepremApp**, Türkiye'de meydana gelen son depremleri masaüstünde mini bir widget olarak gösteren şık ve kullanışlı bir Python uygulamasıdır. Kullanıcı dostu arayüzü ve hızlı uyarı sistemiyle, önemli depremleri kaçırmazsın.

## 🚀 Özellikler

- ⏱️ Anlık deprem verisi güncellemesi
- 🖥️ Masaüstü mini widget (şeffaf & çerçevesiz)
- 🔔 Discord Webhook ile alarm sistemi
- 🎛️ Ayarlanabilir şiddet eşik değeri
- 🧪 Hafif ve modüler yapı

## 🧰 Gereksinimler

Aşağıdaki Python kütüphanelerini yüklemen gerekiyor:

```bash
pip install requests tkinter pystray pillow
```

> Not: `tkinter` çoğu Python kurulumu ile gelir. Hata alırsan `sudo apt install python3-tk` (Linux) veya `Add/Remove Programs > Optional Features` (Windows) ile yükleyebilirsin.

## 🔧 Kullanım

1. `deprem.py` dosyası: Kandilli veya AFAD gibi bir kaynaktan verileri çeker.
2. `screen.py`: Deprem verisini ekranda gösterir.
3. `webhook.py`: Discord'a alarm yollar.
4. `settings.py`: Eşik değeri gibi ayarlar burada saklanır.
5. `DepremApp.py`: Tüm parçaları birleştirip uygulamayı çalıştırır.

Uygulamayı başlatmak için:

```bash
python DepremApp.py
```

## ⚙️ Yapılacaklar

- [ ] Sesli uyarı sistemi
- [ ] Kaynak seçme (AFAD / Kandilli)
- [ ] Harita üzerinde gösterim
- [ ] Tray ikon menüsüne daha fazla özellik

## 📷 Görseller

(Not yet any picture.)

## 🛠️ Geliştirme

İstersen bu projeyi fork'la, değiştir, paylaş. Öğrenmek ve öğretmek için buradayız.

---

Hazırlayan: [Toprak](https://github.com/TPashaxrd)
Yardımcı: [Batın](https://github.com/Batin-dev)
İzin: MIT  
```