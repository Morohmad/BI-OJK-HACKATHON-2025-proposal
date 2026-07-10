# SATUKAN - Sistem Autentikasi Terpadu untuk Penyaluran Bansos

## Deskripsi Proyek

SATUKAN (Sistem Autentikasi Terpadu untuk Penyaluran Bansos) merupakan solusi digital yang dikembangkan dalam rangka **BI-OJK Hackathon 2025** oleh **Tim Hyperion**.

Proyek ini dirancang untuk membantu pemerintah meningkatkan akurasi, transparansi, dan keamanan proses distribusi bantuan sosial (bansos) melalui kombinasi teknologi **Face Recognition**, **Validasi Lokasi**, dan **Pencatatan Digital**.

Sistem bertujuan mengatasi berbagai permasalahan distribusi bansos seperti:

- Data penerima ganda
- Penerima fiktif
- Manipulasi identitas
- Verifikasi manual yang tidak efisien
- Kesenjangan akses digital bagi masyarakat yang tidak memiliki perangkat pribadi

---

# Latar Belakang

Distribusi bantuan sosial di Indonesia masih menghadapi berbagai tantangan, mulai dari ketidaktepatan sasaran hingga potensi penyalahgunaan identitas penerima.

SATUKAN menawarkan solusi berbasis Artificial Intelligence (AI) yang memanfaatkan teknologi biometrik wajah dan validasi lokasi untuk memastikan bantuan diterima oleh penerima yang berhak.

Dengan pendekatan ini, proses verifikasi dapat dilakukan secara otomatis, cepat, dan terdokumentasi sehingga meningkatkan transparansi serta akuntabilitas penyaluran bansos.

---

# Tujuan Proyek

- Memastikan bantuan diterima oleh penerima yang berhak.
- Mengurangi data penerima ganda dan penerima fiktif.
- Meningkatkan transparansi distribusi bantuan sosial.
- Mendukung digitalisasi layanan publik.
- Menyediakan mekanisme verifikasi yang inklusif.

---

# Kompetisi

**BI-OJK Hackathon 2025**

### Tema

**Financial Innovation & Public Service**

### Tim Hyperion

- Muhammad Rizki Sepriadi — Project Lead, UI/UX, Mobile Developer
- Denni Setiawan — Web Developer, Data Scientist
- Jimmy Maulana — UI/UX Designer, Cloud Engineer
- Mohammad Rohmad Nur Khoirofiq — Machine Learning & AI Engineer, Data Scientist

---

# Arsitektur Solusi

## 1. Face Recognition

Sistem menggunakan teknologi Face Recognition berbasis **FaceNet** untuk melakukan autentikasi penerima bantuan.

### Tahapan

1. Pengambilan gambar wajah melalui webcam.
2. Deteksi wajah menggunakan OpenCV.
3. Ekstraksi Face Embedding menggunakan FaceNet.
4. Proses **Enrollment** untuk membangun database embedding.
5. Pencocokan embedding menggunakan **Cosine Similarity**.
6. Menentukan status **Registered** atau **Not Registered**.
7. Menampilkan hasil verifikasi.

### Face Recognition Pipeline

```text
Database Wajah
        │
        ▼
Enrollment
(Generate Mean Face Embedding)
        │
        ▼
Database Embedding (.pkl)
        │
────────┼────────────────────────
        │
        ▼
Capture Wajah
        │
        ▼
Generate Face Embedding
        │
        ▼
Cosine Similarity Matching
        │
        ▼
Registered / Not Registered
```

---

## 2. Validasi Lokasi

Setelah wajah berhasil diverifikasi, sistem melakukan pemeriksaan lokasi penerima.

### Tahapan

1. Mengambil koordinat GPS perangkat.
2. Membandingkan koordinat dengan lokasi distribusi bantuan.
3. Menentukan apakah lokasi valid.
4. Mengirim hasil validasi ke sistem.

---

## 3. Pencatatan Digital

Seluruh hasil verifikasi disimpan secara otomatis sebagai kebutuhan audit dan monitoring.

Data yang dicatat:

- Identitas penerima
- Status verifikasi
- Waktu verifikasi
- Lokasi verifikasi

---

# Teknologi dan Metode

## Artificial Intelligence

### Face Recognition

Model yang digunakan

- FaceNet (Pre-trained)
- DeepFace

Metode

- Face Embedding
- Mean Face Embedding
- Cosine Similarity

Alasan penggunaan

- Akurasi tinggi untuk pengenalan wajah.
- Tidak memerlukan pelatihan ulang model.
- Mendukung verifikasi real-time.
- Lebih efisien menggunakan database embedding dibandingkan pencocokan langsung terhadap seluruh gambar.

---

## Geolocation

Metode

- GPS Validation
- IP Geolocation (Opsional)

Digunakan untuk memastikan penerima berada pada lokasi distribusi bantuan yang telah ditentukan.

---

# Dataset

Prototype menggunakan kombinasi dataset publik dan data simulasi.

## Dataset Wajah

- **Labeled Faces in the Wild (LFW)** digunakan sebagai dataset publik untuk simulasi penerima bantuan.
- Foto anggota tim digunakan sebagai data pengujian autentikasi wajah.

## Dataset Lokasi

- Data koordinat GPS diperoleh dari perangkat pengguna.
- Digunakan untuk simulasi validasi lokasi.

---

# Alur Sistem

```text
Penerima Bansos
        │
        ▼
Capture Wajah
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
Pencatatan Digital
        │
        ▼
Dashboard Monitoring
```

---

# Implementasi Prototype

Prototype AI dikembangkan menggunakan Python dengan memanfaatkan:

- DeepFace
- FaceNet
- TensorFlow
- OpenCV

Fitur yang telah diimplementasikan

- Face Enrollment.
- Face Embedding Generation.
- Face Verification.
- Cosine Similarity Matching.
- Verifikasi wajah melalui webcam.
- Penyimpanan database embedding.
- Logging hasil verifikasi.

---

# Teknologi yang Digunakan

## Backend & AI

- Python
- TensorFlow
- DeepFace
- FaceNet
- OpenCV
- NumPy

## Mobile & Web

- React Native
- Expo
- Express.js
- TypeScript

## Database

- Supabase

## Tools

- Git
- GitHub
- VS Code
- Figma

---

# Struktur Repository

```text
Face_Recognition/
│
├── database/
│   ├── Person_001/
│   ├── Person_002/
│   └── ...
│
├── embeddings/
│   └── face_embeddings.pkl
│
├── logs/
│   └── log_verifikasi.txt
│
├── models/
│
├── src/
│   ├── camera.py
│   ├── config.py
│   ├── enroll.py
│   ├── logger.py
│   ├── main.py
│   ├── utils.py
│   └── verify.py
│
├── README.md
└── requirements.txt
```

---

# Cara Menjalankan

## 1. Clone Repository

```bash
git clone https://github.com/username/Face_Recognition.git
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Generate Face Embedding

```bash
python src/enroll.py
```

Perintah ini akan membuat file:

```text
embeddings/
└── face_embeddings.pkl
```

## 4. Jalankan Face Recognition

```bash
python src/main.py
```

Tekan tombol:

- **C** → Verifikasi Wajah
- **ESC** → Keluar

---

# Status Proyek

**Tahap:** Prototype & Proposal Kompetisi

Progress Implementasi

- ✅ Face Enrollment
- ✅ Face Recognition
- ✅ Face Verification
- ✅ Verification Logging
- ⏳ Location Validation
- ⏳ Dashboard Monitoring
- ⏳ Integrasi Supabase

---

# Kontribusi Saya

Sebagai **Machine Learning & AI Engineer**, kontribusi yang saya kerjakan meliputi:

- Merancang arsitektur Face Recognition berbasis Face Embedding.
- Implementasi FaceNet menggunakan DeepFace.
- Pengembangan proses Face Enrollment.
- Pengembangan database Face Embedding.
- Implementasi Face Verification menggunakan Cosine Similarity.
- Pengujian dan evaluasi performa model Face Recognition.
- Integrasi modul AI ke dalam sistem autentikasi.

---

# Pengembangan Selanjutnya

Beberapa pengembangan yang direncanakan meliputi:

- Integrasi dengan database resmi pemerintah.
- Validasi lokasi berbasis GPS.
- Dashboard monitoring real-time.
- Face Liveness Detection.
- Anti-Spoofing Detection.
- Enkripsi data biometrik.
- Deployment berbasis cloud.

---

# Lisensi

Proyek ini dikembangkan sebagai bagian dari **BI-OJK Hackathon 2025** dan ditujukan untuk kebutuhan penelitian, pengembangan prototype, serta demonstrasi solusi digital.
