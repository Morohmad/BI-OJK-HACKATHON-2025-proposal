# SATUKAN - Sistem Autentikasi Terpadu untuk Penyaluran Bansos

## Deskripsi Proyek

SATUKAN (Sistem Autentikasi Terpadu untuk Penyaluran Bansos) merupakan solusi digital yang dikembangkan dalam rangka **BI-OJK Hackathon 2025** oleh **Tim Hyperion**.

Proyek ini dirancang untuk membantu pemerintah meningkatkan akurasi dan transparansi distribusi bantuan sosial (bansos) melalui kombinasi teknologi **Face Recognition**, **Validasi Lokasi**, dan **Pencatatan Digital**.

Sistem bertujuan mengatasi berbagai permasalahan distribusi bansos seperti:

* Data penerima ganda
* Penerima fiktif
* Manipulasi identitas
* Verifikasi manual yang tidak efisien
* Kesenjangan akses digital bagi masyarakat yang tidak memiliki perangkat pribadi

---

## Latar Belakang

Distribusi bantuan sosial di Indonesia masih menghadapi berbagai tantangan, mulai dari ketidaktepatan sasaran hingga potensi penyalahgunaan data penerima.

SATUKAN menawarkan pendekatan berbasis kecerdasan buatan (Artificial Intelligence) yang memungkinkan proses verifikasi dilakukan secara otomatis menggunakan identitas biometrik dan lokasi penerima secara real-time.

---

## Tujuan Proyek

* Memastikan bantuan diterima oleh penerima yang berhak.
* Mengurangi data penerima ganda dan penerima fiktif.
* Meningkatkan transparansi distribusi bansos.
* Mendukung digitalisasi layanan publik.
* Menyediakan mekanisme verifikasi yang inklusif bagi masyarakat yang tidak memiliki smartphone.

---

## Kompetisi

**BI-OJK Hackathon 2025**

Tema:

**Financial Innovation & Public Service**

Tim:

### Hyperion

* Muhammad Rizki Sepriadi — Project Lead, UI/UX, Mobile Developer
* Denni Setiawan — Web Developer, Data Scientist
* Jimmy Maulana — UI/UX Designer, Cloud Engineer
* Mohammad Rohmad Nur Khoirofiq — Machine Learning & AI Engineer, Data Scientist

---

## Arsitektur Solusi

### 1. Face Recognition

Sistem menggunakan teknologi pengenalan wajah untuk mencocokkan identitas penerima bantuan dengan data yang tersimpan pada database.

Tahapan:

1. Pengambilan gambar wajah melalui kamera.
2. Deteksi wajah.
3. Ekstraksi fitur wajah.
4. Pembentukan embedding wajah.
5. Pencocokan dengan database penerima.
6. Hasil verifikasi.

### 2. Validasi Lokasi

Setelah wajah berhasil diverifikasi, sistem melakukan pemeriksaan lokasi pengguna.

Proses:

1. Mengambil lokasi pengguna.
2. Mendapatkan koordinat lokasi.
3. Membandingkan dengan lokasi distribusi yang telah ditentukan.
4. Menentukan status valid atau tidak valid.

### 3. Pencatatan Digital

Seluruh hasil verifikasi disimpan ke dalam sistem untuk kebutuhan audit dan monitoring.

Data yang dicatat:

* Identitas penerima
* Status verifikasi
* Waktu verifikasi
* Lokasi verifikasi

---

## Teknologi dan Metode

### Artificial Intelligence

#### Face Recognition

Model yang digunakan:

* FaceNet
* DeepFace

Alasan penggunaan:

* Akurasi tinggi untuk pencocokan wajah.
* Mendukung verifikasi real-time.
* Tidak memerlukan pelatihan ulang dari awal karena menggunakan model pretrained.

### Geolocation

Metode:

* IP Geolocation
* GPS Validation

Digunakan untuk memastikan penerima berada pada lokasi distribusi yang telah ditentukan.

---

## Dataset

Dataset yang digunakan dalam tahap simulasi terdiri dari:

### Data Wajah

* Foto wajah anggota tim sebagai data simulasi penerima bansos.
* Digunakan untuk proses autentikasi wajah.

### Data Lokasi

* Data lokasi diperoleh dari perangkat masing-masing anggota tim.
* Digunakan untuk validasi lokasi penerima.

### Proses Pengumpulan Data

1. Pengambilan foto wajah.
2. Verifikasi identitas berdasarkan data pribadi.
3. Pengambilan koordinat lokasi.
4. Penyimpanan ke database lokal.
5. Pengujian berulang untuk memastikan konsistensi sistem.

---

## Alur Sistem

```text
Penerima Bansos
       │
       ▼
Pengambilan Foto Wajah
       │
       ▼
Face Recognition
       │
       ▼
Verifikasi Identitas
       │
       ▼
Validasi Lokasi
       │
       ▼
Pencatatan Hasil Verifikasi
       │
       ▼
Dashboard Monitoring
```

---

## Implementasi Prototype

Prototype AI dibangun menggunakan Python dengan memanfaatkan:

* DeepFace
* FaceNet
* OpenCV

Fitur yang telah diimplementasikan:

* Verifikasi wajah melalui webcam.
* Pencocokan wajah dengan database.
* Pencatatan hasil verifikasi secara otomatis.
* Penyimpanan log verifikasi.

---

## Teknologi yang Digunakan

### Backend & AI

* Python
* TensorFlow
* DeepFace
* FaceNet
* OpenCV

### Mobile & Web

* React Native
* Expo
* Express.js
* TypeScript

### Database

* Supabase

### Tools

* GitHub
* Figma

---

## Struktur Repository

```text
.
├── face_recog.py
├── facenet_weights.h5
├── ds_model_facenet_detector_opencv_aligned_normalization_base_expand_0.pkl
├── log_verifikasi.txt
├── Proposal BI-OJK Hackathon 2025.pdf
└── README.md
```

---

## Status Proyek

Tahap: Prototype & Proposal Kompetisi

Proyek ini dikembangkan sebagai solusi konseptual dan prototype awal untuk BI-OJK Hackathon 2025. Sistem masih dapat dikembangkan lebih lanjut melalui integrasi dengan database resmi pemerintah, peningkatan keamanan biometrik, serta dashboard monitoring skala nasional.

---

## Kontribusi Saya

Sebagai Machine Learning & AI Engineer, kontribusi yang saya kerjakan meliputi:

* Pengembangan modul Face Recognition.
* Implementasi DeepFace dan FaceNet.
* Pengujian model autentikasi wajah.
* Integrasi proses verifikasi AI dengan alur sistem.
* Analisis kebutuhan data dan validasi identitas.
