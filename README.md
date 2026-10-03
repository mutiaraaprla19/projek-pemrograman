# Ayo Belajar Teks Anekdot

## Menjalankan aplikasi
1. Buka folder proyek di VS Code.
2. Buka Terminal.
3. Jalankan:
   pip install -r requirements.txt
4. Jalankan:
   streamlit run app.py

## Struktur fitur
Beranda → Tutorial → Materi → Tanya AI → Latihan PG → Evaluasi Esai → Progress → Dashboard Guru.

## Catatan penting
- Tutor AI pada versi ini adalah tutor berbasis knowledge base lokal, jadi tidak memerlukan API key.
- Evaluasi esai memakai pencocokan konsep/inti makna agar siswa bisa menjawab dengan bahasa sendiri.
- Riwayat chat aktif disimpan maksimal 100 interaksi per siswa.
- Data tersimpan lokal pada folder data_app/users.
- Untuk penggunaan kelas nyata skala besar, sebaiknya pindahkan penyimpanan ke database online dan gunakan autentikasi guru yang lebih kuat.
