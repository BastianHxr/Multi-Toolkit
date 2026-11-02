# BASTIAN

**BASTIAN // SENTINEL** — toolkit riset keamanan interaktif untuk menganalisis satu atau banyak target sekaligus.

Tiga modul terintegrasi:

| Modul | Isi pemeriksaan |
| --- | --- |
| **Analysis** | HTTP headers, security headers, rantai redirect, SSL/TLS + sertifikat, DNS (A/AAAA/CNAME/MX/NS/TXT), WHOIS, fingerprint teknologi, `robots.txt` / `sitemap.xml` / `security.txt` |
| **Scanning** | TCP port scan, directory/file brute-force, pengecekan file sensitif (`.env`, `.git`, backup, dsb.) |
| **Reputation** | Geolokasi IP, DNSBL, URLhaus, serta lookup opsional VirusTotal / AbuseIPDB / Google Safe Browsing |

> ⚠️ **Hanya untuk penggunaan yang sah.** Uji hanya aset milik Anda atau yang Anda punya izin tertulis untuk diuji. Pemindaian tanpa izin bisa melanggar hukum.

---

## 1. Kebutuhan

- **Python 3.8+** (disarankan 3.10 atau lebih baru)
- **Tanpa dependency eksternal** — seluruh toolkit memakai standard library Python
- Koneksi internet untuk modul Analysis, Scanning, dan Reputation
- Terminal yang mendukung Unicode (Windows Terminal / PowerShell 7 disarankan)

Cek versi Python:

```powershell
python --version
```

---

## 2. Menjalankan

Masuk ke folder BASTIAN, lalu jalankan:

```powershell
cd C:\Users\user\BASTIAN
python bs.py
```

Di Windows bisa juga:

```powershell
py bs.py
```

Tanpa argumen, BASTIAN langsung membuka **console interaktif**. `main.py` hanya entry point lama dan tetap bisa dipakai, tetapi disarankan `bs.py`.

### Opsi command line

```text
python bs.py -h            # bantuan
python bs.py --help        # bantuan
python bs.py -v            # versi
python bs.py --version     # versi
```

Semua pengaturan (target, modul, opsi scan) diisi lewat menu interaktif, bukan lewat argumen.

---

## 3. Alur pemakaian

```text
1. CONFIGURE      → isi target, pilih modul, atur opsi
2. RUN MODULES    → jalankan pemindaian
3. VIEW CONFIG    → cek pengaturan aktif
4. ABOUT / HELP   → info & disclaimer
0. EXIT           → keluar
```

### Langkah pertama kali

1. Jalankan `python bs.py`.
2. Pilih **`1` (CONFIGURE)**.
3. Isi target, misalnya `example.com` atau `example.com, 1.1.1.1`.
4. Pilih modul (`4` = semua modul).
5. Tekan Enter untuk memakai nilai default pada opsi lain.
6. Pilih **`3` (VIEW CONFIG)** untuk memastikan konfigurasi sudah benar.
7. Pilih **`2` (RUN MODULES)** lalu jawab `y` saat diminta konfirmasi.

Contoh sesi:

```text
❯ select an operation  1        # CONFIGURE
❯ Target(s)            example.com
❯ Select modules       4        # ALL MODULES
❯ Threads              40
❯ Timeout              10
❯ Ports                top100
❯ Save reports         y
❯ Output directory     C:\Users\user\BASTIAN\reports
```

Lalu:

```text
❯ select an operation  2
❯ run with this configuration? (y/n) [y]  y
```

---

## 4. Format target

Target bisa berupa domain, IP, URL, atau beberapa target sekaligus.

| Contoh input | Target yang dipakai |
| --- | --- |
| `example.com` | `https://example.com` |
| `http://example.com` | `http://example.com` |
| `example.com:8443` | `https://example.com:8443` |
| `https://example.com/path?x=1` | `https://example.com` (path dibuang) |
| `1.2.3.4` | `https://1.2.3.4` |
| `example.com, test.org 1.1.1.1` | tiga target terpisah (dipisah koma/spasi/baris baru) |
| `C:\Users\user\BASTIAN\target.txt` | semua target dari file |

Skema default adalah **HTTPS** (port default 443). Kalau ingin HTTP, tulis `http://...` secara eksplisit.

### Target dari file

Buat file teks berisi satu target per baris:

```text
# komentar diawali tanda #
example.com
test.org
1.1.1.1
https://app.example.com:8443
```

Lalu isi field target dengan **path file itu saja** (bukan dicampur target lain), contoh:

```text
C:\Users\user\BASTIAN\target.txt
```

Contoh file `target.txt` sudah disertakan di folder ini.

> Target duplikat otomatis dibuang, dan baris yang diawali `#` diabaikan.

---

## 5. Detail form CONFIGURE

### 5.1 Target setup

| Field | Keterangan |
| --- | --- |
| `Target(s)` | **Wajib.** Domain / IP / URL, dipisah koma atau spasi, atau path file target |

### 5.2 Module selection

| Kode | Modul |
| --- | --- |
| `1` | Analysis |
| `2` | Scanning |
| `3` | Reputation |
| `4` | All modules (default) |

### 5.3 Performance & network

| Field | Default | Rentang | Keterangan |
| --- | --- | --- | --- |
| `Threads` | `40` | 1–200 | Jumlah worker paralel. Nilai di luar rentang otomatis disesuaikan |
| `Timeout` | `10` | 1–120 detik | Timeout per request/koneksi |
| `Proxy` | kosong | — | Contoh `http://127.0.0.1:8080`; kosongkan untuk koneksi langsung |

### 5.4 Scan options (hanya jika modul Scanning aktif)

**Ports** menerima format berikut:

| Input | Arti |
| --- | --- |
| `top100` atau `top` | 100 port paling umum (default) |
| `common` atau `top10` | 20 port umum |
| `80,443,8080` | daftar port |
| `1-1024` | rentang port |
| `22,80,8000-8100` | kombinasi daftar + rentang |

> Scanning memindai **maksimal 100 port pertama** dari daftar yang dipilih.

**Directory wordlist** — path file wordlist kustom (satu kata/path per baris). Kosongkan untuk memakai daftar bawaan.

### 5.5 API keys (opsional, hanya jika modul Reputation aktif)

| Key | Fungsi |
| --- | --- |
| `VirusTotal API key` | Reputasi domain/IP di VirusTotal |
| `AbuseIPDB API key` | Skor abuse IP |
| `Google Safe Browsing API key` | Cek ancaman malware/phishing |

Kosongkan jika tidak punya. Lookup geolokasi, DNSBL, dan URLhaus tetap berjalan tanpa key.

> Key hanya disimpan di memori selama sesi berjalan — tidak ditulis ke disk dan harus diisi ulang saat program dijalankan lagi.

### 5.6 Output

| Field | Keterangan |
| --- | --- |
| `Save reports to files?` | `y` / `n` |
| `Output directory` | Default `reports` di folder kerja saat ini |

---

## 6. Hasil dan laporan

Setiap target menghasilkan laporan dengan bagian seperti:

```text
TARGET 1/1 · example.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ RUN] analysis  : example.com
[ RUN] scanning  : example.com
[ RUN] reputation: example.com
...
```

Laporan **selalu ditampilkan di terminal**. Jika `Save reports` aktif, file teks juga disimpan ke:

```text
reports/<target>_<timestamp>.txt
```

Contoh:

```text
reports\example.com_1793478770.txt
reports\1.1.1.1_1793478801.txt
```

Karakter selain huruf/angka/`.`/`-`/`_` pada nama target diganti `_`.

Laporan di disk berupa teks polos (tanpa kode warna), cocok untuk diarsipkan atau dilampirkan.

### Ringkasan bagian laporan

| Modul | Bagian |
| --- | --- |
| Analysis | `REDIRECT CHAIN`, `HTTP RESPONSE HEADERS`, `SECURITY HEADERS`, `TECHNOLOGY STACK`, `SSL / TLS`, `DNS RECORDS`, `WHOIS`, `WELL-KNOWN RESOURCES` |
| Scanning | `OPEN PORTS`, `DIRECTORY / FILE FUZZ`, `SENSITIVE FILES` |
| Reputation | `GEOLOCATION`, `DNS BLACKLISTS`, `URLHAUS (HOST)`, `URLHAUS (URL)`, plus `VIRUSTOTAL`, `ABUSEIPDB`, `GOOGLE SAFE BROWSING` bila key diisi |

Penanda penting:

- `[PRESENT]` / `[MISSING]` — header keamanan ada atau tidak
- `[FLAGGED]` — file sensitif merespons HTTP 200 (berpotensi terekspos)
- `[NOTICE]` — path menarik tetapi bukan 200 (mis. 301/403)

---

## 7. Warna dan tampilan

- Warna aktif otomatis saat output ke terminal (TTY).
- Matikan warna dengan environment variable `NO_COLOR=1`.
- Paksa warna dengan `FORCE_COLOR=1`.
- Lebar panel menyesuaikan lebar terminal (58–92 kolom).
- Saat output dialihkan ke file/pipe, warna otomatis nonaktif.

```powershell
$env:NO_COLOR = "1"
python bs.py

$env:FORCE_COLOR = "1"
python bs.py
```

---

## 8. Tips dan troubleshooting

| Masalah | Solusi |
| --- | --- |
| `no target configured` | Pilih menu `1` dan isi target terlebih dahulu |
| `no valid targets found in input` | Periksa format target; pastikan tidak ada karakter aneh |
| Target dari file tidak terbaca | Isi field target dengan path file saja; pastikan file ada dan satu target per baris |
| Semua port tertutup | Coba `common`, atau rentang/daftar port spesifik; periksa firewall |
| `No TLS ... handshake failed` | Target mungkin hanya HTTP — pakai `http://...` |
| WHOIS kosong | Port 43 diblokir jaringan, atau server WHOIS sedang tidak merespons |
| API `failed` | Periksa key, kuota, dan koneksi; tanpa key lookup tersebut memang dilewati |
| DNSBL terdaftar | Bisa false positive (terutama IP shared/hosting); verifikasi manual |
| Karakter aneh di Windows | Jalankan di Windows Terminal / PowerShell 7; BASTIAN sudah memaksa UTF-8 |
| Scan lambat | Turunkan jumlah port, pakai `common`, atau naikkan `Threads` (maks 200) |
| Ctrl+C saat scan | Dianggap interupsi; target yang sedang berjalan dihentikan, menu kembali tampil |

Catatan perilaku:

- `Threads` dan `Timeout` di luar rentang akan otomatis dijepit ke batas yang diizinkan (dengan peringatan).
- Port yang tidak valid dalam spesifikasi akan diabaikan; jika tidak ada port valid, otomatis kembali ke `top100`.
- Target Analysis bersifat *best effort*: kegagalan satu pemeriksaan (mis. WHOIS) tidak menghentikan bagian lain.
- Sertifikat TLS tidak diverifikasi (koneksi tetap dijalin untuk keperluan inspeksi); jangan gunakan hasilnya sebagai jaminan keamanan koneksi.

---

## 9. Struktur proyek

```text
BASTIAN/
├─ bs.py                  # entry point utama
├─ main.py                # entry point lama (alias)
├─ target.txt             # contoh daftar target
├─ README.md
├─ bastian/
│  ├─ __init__.py         # versi & dokumentasi paket
│  ├─ menu.py             # console interaktif
│  ├─ config.py           # form konfigurasi & Settings
│  ├─ target.py           # normalisasi & load multi-target
│  ├─ runner.py           # orkestrasi modul per target
│  ├─ reporter.py         # builder & penulis laporan teks
│  ├─ http.py             # HTTP client stdlib (proxy, redirect, TLS)
│  ├─ ui.py / logo.py     # tampilan panel & banner
│  ├─ color.py            # helper ANSI/truecolor
│  └─ modules/
│     ├─ analysis.py
│     ├─ scanning.py
│     └─ reputation.py
└─ reports/               # output laporan
```

---

## 10. Disclaimer

BASTIAN dibuat untuk **riset keamanan yang sah**, audit aset sendiri, dan pengujian dengan izin eksplisit. Pengguna bertanggung jawab penuh atas target yang dipindai dan mematuhi hukum yang berlaku. Penulis tidak bertanggung jawab atas penyalahgunaan.

---

**BASTIAN v1.0.0** · coded by [t.me/BastianHxr13](https://t.me/BastianHxr13)
