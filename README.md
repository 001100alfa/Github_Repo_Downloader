```markdown
# GitHub Repo Downloader

Bu uygulama, GitHub API'sını kullanarak belirttiğiniz sorguya göre repo araması yapar, 
arama sonuçlarını bir grafiksel arayüzde listeler ve seçtiğiniz repoları (git clone kullanarak) indirir.

## Özellikler
- GitHub API üzerinden repo araması.
- Arama sorgusuna otomatik olarak "stars:>100" koşulu eklenir.
- Arama sonuçları liste halinde onay kutuları ile sunulur.
- "Tümünü Seç" butonu ile tüm repolar seçilebilir.
- Seçilen repolar, belirlenen dizine klonlanır.
- Üst çubuk üzerinde Dark Theme/Light Theme geçiş butonu.

## Gereksinimler
- Python 3.x
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Requests](https://pypi.org/project/requests/)
- Git komutu (sisteminizde yüklü ve PATH'e ekli olmalı)

## Kurulum
1. Gerekli paketleri kurun:
   ```bash
   pip install PyQt5 requests
   ```
2. Git'in sisteminizde kurulu olduğundan emin olun.

## Kullanım
1. Uygulamayı çalıştırın:
   ```bash
   python3 Github_Repo_Downloader.py
   ```
2. Arama sorgusu alanına örneğin `language:python` gibi sorgunuzu girin. (Arama sorgusuna 
   otomatik olarak "stars:>100" eklenecektir.)
3. "Ara" butonuna basın.
4. Listelenen repoların yanındaki onay kutularını kullanarak seçim yapın veya "Tümünü Seç" 
   butonunu kullanın.
5. "Seçilenleri İndir" butonuna basın. Seçtiğiniz repolar, belirlediğiniz dizine klonlanacaktır.
6. Üst araç çubuğundaki "Dark Theme"/"Light Theme" butonunu kullanarak temayı değiştirebilirsiniz.

## EXE Dosyasına Dönüştürme
Terminal penceresinin görünmemesi için PyInstaller kullanarak uygulamayı EXE'ye dönüştürebilirsiniz. 
Aşağıdaki komut, terminal penceresi olmadan tek dosya halinde `Github_Repo_Downloader.exe` üretilmesini sağlar:

```bash
pyinstaller --noconsole --onefile --name Github_Repo_Downloader.exe Github_Repo_Downloader.py
```

Bu komut çalıştıktan sonra, `dist` klasöründe `Github_Repo_Downloader.exe` dosyasını bulabilirsiniz.
```
