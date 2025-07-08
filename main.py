import csv, os

csv_file = 'keuangan.csv'
transaksi = []

def muat_data():
    if not os.path.isfile(csv_file): return
    with open(csv_file, 'r') as f:
        for row in csv.DictReader(f):
            row['Nominal'] = int(row['Nominal'])
            transaksi.append(row)

def tambah_transaksi():
    while True:
        tgl = input("Tanggal (YYYY-MM-DD): ")
        tipe = input("Tipe (Pemasukan/Pengeluaran): ").capitalize()
        kategori = input("Kategori: ")
        try:
            nominal = int(input("Nominal: "))
        except: print("Harus angka!"); continue
        ket = input("Keterangan: ")
        transaksi.append({
            'Tanggal': tgl, 'Tipe': tipe, 'Kategori': kategori,
            'Nominal': nominal, 'Keterangan': ket
        })
        if input("Tambah lagi? (y/n): ").lower() != 'y': break

def tampilkan_transaksi():
    if not transaksi: print("\nBelum ada data."); return
    print("\n=== Semua Transaksi ===")
    for i, t in enumerate(transaksi, 1):
        print(f"{i}. {t['Tanggal']} | {t['Tipe']} | {t['Kategori']} | Rp{t['Nominal']} | {t['Keterangan']}")

def tampilkan_laporan():
    masuk = sum(t['Nominal'] for t in transaksi if t['Tipe'].lower() == 'pemasukan')
    keluar = sum(t['Nominal'] for t in transaksi if t['Tipe'].lower() == 'pengeluaran')
    saldo = masuk - keluar
    print("\n=== Ringkasan Keuangan ===")
    print(f"Total Pemasukan  : Rp{masuk}")
    print(f"Total Pengeluaran: Rp{keluar}")
    print(f"Saldo Akhir      : Rp{saldo}")

    # Laporan per kategori
    print("\n=== Pengeluaran per Kategori ===")
    kategori = {}
    for t in transaksi:
        if t['Tipe'].lower() == 'pengeluaran':
            k = t['Kategori']
            kategori[k] = kategori.get(k, 0) + t['Nominal']
    if kategori:
        for k, total in kategori.items():
            print(f"{k}: Rp{total}")
    else:
        print("Belum ada pengeluaran.")

def simpan_data():
    header = ['Tanggal', 'Tipe', 'Kategori', 'Nominal', 'Keterangan']
    tulis_header = not os.path.isfile(csv_file) or os.stat(csv_file).st_size == 0
    with open(csv_file, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=header)
        if tulis_header: w.writeheader()
        for t in transaksi[-len(tambah):]: w.writerow(t)

def simpan_laporan():
    masuk = sum(t['Nominal'] for t in transaksi if t['Tipe'].lower() == 'pemasukan')
    keluar = sum(t['Nominal'] for t in transaksi if t['Tipe'].lower() == 'pengeluaran')
    saldo = masuk - keluar
    kategori = {}
    for t in transaksi:
        if t['Tipe'].lower() == 'pengeluaran':
            kategori[t['Kategori']] = kategori.get(t['Kategori'], 0) + t['Nominal']
    with open("laporan.csv", 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["Laporan", "Nominal"])
        w.writerow(["Total Pemasukan", masuk])
        w.writerow(["Total Pengeluaran", keluar])
        w.writerow(["Saldo Akhir", saldo])
        w.writerow([]); w.writerow(["Pengeluaran per Kategori", ""])
        for k, total in kategori.items():
            w.writerow([k, total])

            

# === MAIN ===
if __name__ == "__main__":
    muat_data()
    tambah = []
    tambah_transaksi(); tambah = transaksi.copy()  # Simpan hanya data baru
    tampilkan_transaksi()
    tampilkan_laporan()
    simpan_data()
    simpan_laporan()
