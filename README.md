# Panic-Trap: Behavioral Biometrics IDS 🛡️⌨️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-success.svg)](#)

*(Türkçe açıklamalar aşağıdadır / Scroll down for Turkish)*

## 🇺🇸 English

**Panic-Trap** is an advanced Behavioral Biometric Intrusion Detection System (IDS). It continuously authenticates the user based on their unique typing rhythm (Keystroke Dynamics) using a custom Press-to-Press (P2P) N-Gram architectural model. 

If an unauthorized user (intruder) takes over an unlocked workstation, their erratic or unfamiliar typing rhythm instantly triggers the defense mechanisms.

### Core Features
- **Continuous Authentication:** Zero-friction monitoring without interrupting the actual user.
- **N-Gram Baseline Profiling:** Learns the user's inherent cognitive pauses and typing speed.
- **Multi-Stage Defense System:**
  - **Risk > 50 (Silent Recon):** Silently logs active windows and clipboard data.
  - **Risk > 75 (Honeypot Trap):** Deploys a fake 2FA screen to capture the intruder's panic passwords and sends a real-time **Telegram Alert**.
  - **Risk > 90 (Nuclear Lockdown):** Cuts off the network connection (IP release) to prevent data exfiltration and locks the Windows workstation.

### Architecture
- `listener.py`: Captures P2P flight times, eliminating roll-over typing errors.
- `ngram_engine.py`: Builds a statistical baseline utilizing dynamic standard deviations.
- `risk_manager.py`: Calculates deviations from the baseline and controls the state machine.
- `honeypot_ui.py`: Renders a tamper-proof, CustomTkinter-based fake 2FA lock screen.
- `system_lockdown.py`: Handles OS-level network isolation (IP release) and workstation locking.
- `telegram_alert.py`: Manages REST API integration for real-time remote alerts.
- `main.py`: The orchestrator handling cross-thread communication and trigger thresholds.

---

## 🇹🇷 Türkçe

**Panic-Trap**, klavye yazım dinamiklerine (Keystroke Dynamics) dayalı, gelişmiş bir Davranışsal Biyometrik Saldırı Tespit Sistemidir (IDS). Press-to-Press (P2P) N-Gram mimarisi kullanarak bilgisayar başındaki kişinin gerçek sahibi olup olmadığını sürekli olarak doğrular.

Yetkisiz bir kişi (saldırgan) açık bırakılmış bir bilgisayara oturduğunda, farklı yazım ritmi anında tespit edilir ve savunma mekanizmaları tetiklenir.

### Temel Özellikler
- **Sürekli Doğrulama:** Gerçek kullanıcının işini bölmeden arka planda sıfır sürtünmeyle çalışır.
- **N-Gram Profil Çıkarma:** Kullanıcının kognitif (zihinsel) duraksamalarını ve yazım hızını öğrenir.
- **Çok Aşamalı Savunma Sistemi:**
  - **Risk > 50 (Sessiz İstihbarat):** Aktif pencereleri ve pano (clipboard) verilerini sessizce loglar.
  - **Risk > 75 (Honeypot Tuzağı):** Saldırganı sahte bir 2FA şifre ekranına hapseder, girdiği şifreleri kaydeder ve **Telegram** üzerinden gerçek zamanlı uyarı gönderir.
  - **Risk > 90 (Nükleer Kilit):** Veri sızıntısını engellemek için internet bağlantısını keser ve bilgisayarı kilitler.

### Mimari
- `listener.py`: Örtüşen tuş (roll-over) hatalarını engelleyen P2P uçuş sürelerini yakalar.
- `ngram_engine.py`: Dinamik standart sapma kullanarak istatistiksel profil oluşturur.
- `risk_manager.py`: Puan sapmalarını hesaplar ve risk durum makinesini yönetir.
- `honeypot_ui.py`: CustomTkinter tabanlı, atlatılamaz sahte bir 2FA kilit ekranı çizer.
- `system_lockdown.py`: İşletim sistemi düzeyinde ağ izolasyonu ve ekran kilitleme işlemlerini yürütür.
- `telegram_alert.py`: Gerçek zamanlı uzaktan uyarılar için REST API entegrasyonunu yönetir.
- `main.py`: Çapraz iş parçacığı iletişimini sağlayan ve eşikleri tetikleyen ana orkestratör.