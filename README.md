# CareerMatch AI 
**Sistem Rekomendasi ATS CV Berbasis Natural Language Processing**

Repositori ini merupakan ruang kerja utama untuk proyek Capstone tim **PJK-RM119** pada program Pijak x IBM SkillsBuild 2026. "CareerMatch AI" dibangun untuk mengotomatisasi pencocokan keahlian (*skills*) dari dokumen CV pelamar dengan deskripsi pekerjaan (*Job Postings*) menggunakan algoritma NLP dan *Business Rule Heuristics*.

## Tim Pengembang (PJK-RM119)
- **Armand Al-Farizy** - `APC012D6Y0488` (Project Manager & Lead AI/ML Engineer)
- **Aisyah Ridhalillah Putri** - `APC284D6X0336` (Data Analyst & Researcher)
- **Islahul Hadi** - `APC308D6Y0437` (UI/UX & Documentation Specialist)
- **Faber Dui Nababan** - `APC528D6Y0493` (QA Tester)

---

## Workspace Kolaborasi (Google Colab)
Selama fase eksperimen (Minggu 1 hingga Minggu 3), seluruh penulisan kode akan difokuskan pada satu *notebook* Google Colab agar mempermudah kolaborasi dan menghindari kendala spesifikasi *hardware* lokal.

🔗 **[KLIK DI SINI UNTUK MEMBUKA GOOGLE COLAB WORKSPACE](https://colab.research.google.com/drive/13hjFnmpNxQ1ay-Vdhrlg3Pv0fYg9JWbI?usp=sharing)**

### SOP WAJIB: Cara Menyimpan Progres Kode (Push ke GitHub)
Google Colab **TIDAK** otomatis menyimpan perubahan ke GitHub. Setiap kali kamu selesai mengerjakan tugasmu di Colab, kamu **WAJIB** menyimpan salinannya kembali ke repositori ini dengan langkah berikut:
1. Di menu atas Google Colab, klik **File**.
2. Pilih **Save a copy in GitHub** (Simpan salinan di GitHub).
3. Pastikan repositori yang terpilih adalah `PJK-RM119-CareerMatch-AI`.
4. Di kolom **Commit message**, tulis apa yang baru saja kamu kerjakan dengan jelas. (Contoh: *"Aisyah: Selesai EDA"* atau *"Armand: Update fungsi PyPDF2"*).
5. Klik **OK**. Versi terbaru kodemu akan langsung ter-update di repositori ini.

---

## Tech Stack & Data Source
Sistem ini memproses data secara tidak terstruktur (PDF) menjadi representasi vektor yang terstruktur.
- **Dataset Utama:** [Online Job Postings (Armenia 2004-2015)](https://www.kaggle.com/datasets/madhab/jobposts) berisi 19.000+ data lowongan kerja.
- **Data Processing:** `PyPDF2`, `Pandas`, `NLTK`, `SpaCy`
- **Machine Learning:** `Scikit-Learn` (TF-IDF, Cosine Similarity)
- **MLOps:** `MLflow` (Untuk *tracking* eksperimen & artefak model)
- **Deployment Interface:** `Streamlit`

---

## Technical Documentation & Architecture

Sistem *CareerMatch AI* beroperasi menggunakan arsitektur pemrosesan data linier yang dimodifikasi dengan logika *Business Rules* untuk mengatasi kesenjangan data historis.

### 1. Data Acquisition & Cleaning Layer (Aisyah Ridhalillah Putri)
* **Library:** `kagglehub`, `Pandas`
* **Logika:** Mengakuisisi dataset secara dinamis ke memori tanpa membebani penyimpanan lokal. Data dibersihkan dengan menyingkirkan *missing values* pada kolom krusial (`Title`, `JobDescription`, `JobRequirment`, `RequiredQual`) dan menghapus data duplikat untuk menjaga keseimbangan vektor.

### 2. Data Extraction Layer (Armand Al-Farizy)
* **Library:** `PyPDF2`
* **Logika:** Fungsi `extract_pdf_text` melakukan iterasi pada setiap objek halaman PDF pelamar. Sistem dirancang untuk hanya menerima teks *ATS-friendly*.

### 3. NLP Preprocessing Pipeline (Armand Al-Farizy)
* **Library:** `spaCy` (Model: `en_core_web_sm`), `re`, `NLTK`.
* **Strategi:** * **Lemmatization:** Menggunakan Lemmatization (bukan *stemming*) untuk menjaga makna gramatikal teks.
    * **Targeted Stopwords:** Menggabungkan *stopwords* NLTK dengan *Custom Universal CV Stopwords* dan *HR Fluff*, untuk mengeliminasi kata-kata pengisi (noise) dan memastikan hanya kompetensi teknis yang diekstrak.

### 4. Machine Learning & MLOps Pipeline (Armand Al-Farizy)
* **Representasi Numerik:** Mengubah korpus teks menjadi matriks menggunakan **TF-IDF Vectorizer** (Unigram & Bigram).
* **Kalkulasi Jarak:** Menggunakan **Cosine Similarity** untuk menghitung kedekatan vektor CV dan vektor lowongan.
* **Algoritma Optimasi (Business Rule Heuristics):**
    * **Umbrella Terms Alignment:** Menyelaraskan istilah modern di CV (*e.g., Next.js, React*) ke istilah historis di dataset (*e.g., Web Development*) agar TF-IDF tidak kehilangan konteks.
    * **Anti-Mismatch (Negative Filter):** Aturan pemblokiran lintas-domain (e.g., CV *Software Engineer* tidak akan direkomendasikan lowongan *Customs/Logistics*).
    * **Title Boosting:** Mengalikan skor akhir jika judul lowongan cocok secara eksplisit dengan rumpun keahlian utama pelamar.
    * **YoE Penalty:** Memberikan pemotongan skor 15% jika *Years of Experience* pelamar di bawah syarat lowongan.
* **Tracking & Artifacts:** Menyimpan metrik evaluasi ke **MLflow** dan membungkus hasil pelatihan menjadi artefak `.joblib` untuk dideploy secara statis di *Streamlit*.

---

## Cara Menjalankan Proyek di Lokal (Untuk Minggu 4 & 5)
Ketika proyek mulai memasuki fase pembuatan antarmuka UI (Streamlit), kode akan dijalankan di komputer lokal masing-masing.

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/ArcVielLouvent/PJK-RM119-CareerMatch-AI.git
2. **Masuk ke direktori proyek:**
   ```bash
   cd PJK-RM119-CareerMatch-AI
3. **Buat Virtual Environment (Opsional tapi disarankan):**
   ```bash
   python -m venv env
   env\Scripts\activate  # Untuk Windows pengguna CMD
4. **Install semua library yang dibutuhkan:**
   ```bash
   pip install -r requirements.txt
