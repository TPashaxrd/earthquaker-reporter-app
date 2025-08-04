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
pip install requests pystray pillow
```

> Not: `tkinter` çoğu Python kurulumu ile birlikte gelir. Eğer eksikse:  
> **Linux**: `sudo apt install python3-tk`  
> **Windows**: `Add/Remove Programs > Optional Features` kısmından ekleyebilirsin.

## 🔧 Kullanım

1. `deprem.py` → Kandilli veya AFAD gibi kaynaklardan verileri çeker.  
2. `screen.py` → Deprem verisini ekranda gösterir.  
3. `webhook.py` → Discord’a alarm yollar.  
4. `settings.py` → Eşik değeri gibi ayarları saklar.  
5. `DepremApp.py` → Tüm parçaları birleştirir, uygulamayı başlatır.

## ⚙️ Build alma?
1. `pip install pyinstaller`
2. `pyinstaller --onefile main.pyw`

### Başlatmak için:

```bash
python main.pyw
```

## ⚙️ Yapılacaklar

- [ ] Sesli uyarı sistemi  
- [ ] Kaynak seçimi (AFAD / Kandilli)  
- [ ] Harita üzerinde deprem noktası gösterimi  
- [ ] Tray ikon menüsüne gelişmiş ayarlar  

## 📷 Görseller

> Henüz bir ekran görüntüsü eklenmedi.

## 🛠️ Geliştirme

Projeyi fork'la, geliştir, paylaş. Öğrenmek ve öğretmek için açık kaynak güzelliği burada.

---

**Hazırlayan:** [Toprak](https://github.com/TPashaxrd)  
**Yardımcı:** [Batın](https://github.com/Batin-dev)  
**Lisans:** MIT
```