# Python Penataan Data Multirespon Ikutan

Pembuatan dokumen ini dilakukan dibuat pada OS Fedora 34 menggunakan package:
1. jupyterlab==3.1.13
2. python==3.9.7
3. pandas==1.3.3
4. numpy==1.21.2

<i>Note : data yang digunakan sebagai contoh adalah data fiktif</i>

## Ketentuan penggunaan multirespon_ikutan.py
1. User setidaknya harus menentukan kolom yang akan digunakan sebagain acuan penataan / reassign dan kolom mana saja yang akna mengikuti pola penataan pada kolom acuan.
2. Modul program ini belum dapat dengan baik menangani kolom multirespon dan kolom lainnya dengan jawaban yang masih memiliki nilai seperti "99, Jepara", "99, tidak tahu", atau "99, ..." lainnya (asumsi penggunaan modul program ini ketika data sudah <i>clean</i>).
3. Modul program ini dapat menangani <i>reassign value</i> kolom jawaban yang pola penempatan jawabannya mengikuti/mengacu pada kolom multirespon tertentu (perbaikan ketentuan poin 5 pada <b>reassign_into_spss.py</b>)
