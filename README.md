# CareerMatch AI 
**Sistem Rekomendasi ATS CV Berbasis Natural Language Processing**

Repositori ini merupakan ruang kerja utama untuk proyek Capstone tim **PJK-RM119** pada program Pijak x IBM SkillsBuild 2026. "CareerMatch AI" dibangun untuk mengotomatisasi pencocokan keahlian (*skills*) dari dokumen CV pelamar dengan deskripsi pekerjaan (*Job Postings*) menggunakan algoritma NLP.

## Tim Pengembang (PJK-RM119)
- **Armand Al-Farizy** (Lead AI Engineer & Project Manager)
- **Aisyah Ridhalillah Putri** (Data Analyst)
- **Islahul Hadi** (UI/UX & Documentation)
- **Faber Dui Nababan** (QA Tester)

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

## Tech Stack & Minimum Viable Product (MVP)
Sistem ini memproses data secara tidak terstruktur (PDF) menjadi representasi vektor yang terstruktur.
- **Data Processing:** `PyPDF2`, `Pandas`, `NLTK`, `SpaCy`
- **Machine Learning:** `Scikit-Learn` (TF-IDF, Cosine Similarity), `TensorFlow`
- **MLOps:** `MLflow` (Untuk *tracking* eksperimen & model)
- **Deployment Interface:** `Streamlit`

## Technical Documentation & Architecture

Sistem *CareerMatch AI* beroperasi menggunakan arsitektur pemrosesan data linier. Fokus utamanya adalah transformasi data tidak terstruktur menjadi representasi matematis yang dapat dibandingkan.

### 1. High-Level Workflow
Sistem mengikuti alur kerja (pipeline) sebagai berikut:
1. **Extraction:** Dokumen PDF dibaca secara mentah halaman demi halaman.
2. **Purification:** Teks "disucikan" dari artefak digital (URL, Email, Simbol) tanpa menghilangkan terminologi IT (Alfanumerik).
3. **Vectorization:** Teks bersih dikonversi menjadi matriks numerik menggunakan TF-IDF.
4. **Scoring:** Menghitung jarak kosinus antara vektor CV dan vektor Lowongan Kerja untuk menentukan peringkat kecocokan.

### 2. Data Extraction Layer (Tugas 1.1)
* **Library:** `PyPDF2`
* **Logika:** Fungsi `extract_pdf_text` melakukan iterasi pada setiap objek halaman PDF. Sistem dirancang untuk hanya menerima teks ATS-friendly. Jika teks tidak terdeteksi (PDF berbasis gambar), sistem akan memberikan nilai `None` sebagai pemicu (trigger) untuk fungsi *Error Handling* di sisi UI.

### 3. NLP Preprocessing Pipeline (Tugas 2.2)
* **Library:** `spaCy` (Model: `en_core_web_sm`), `re`.
* **Strategi:** * **Lemmatization:** Berbeda dengan *stemming*, kami menggunakan Lemmatization untuk menjaga makna kata (e.g., *developed* -> *develop*).
    * **Stopwords Filtering:** Menggabungkan daftar kata umum NLTK dengan *Custom Universal CV Stopwords* untuk memastikan hanya kata kunci kompetensi yang diproses oleh model.

### 4. Machine Learning & MLOps
* **Core Logic:** Menggunakan **Cosine Similarity** untuk mencari kemiripan arah vektor. Hal ini lebih efektif daripada pencarian kata kunci biasa karena mempertimbangkan bobot kepentingan sebuah kata (TF-IDF) dalam seluruh korpus data.
* **Tracking:** Setiap eksperimen tuning (seperti penentuan `ngram_range`) dicatat secara otomatis menggunakan **MLflow**.
  
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
