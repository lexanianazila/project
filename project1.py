
import os
import random
import time
import keyboard
from termcolor import colored, cprint

# Minta pemain memasukkan ukuran puzzle sampai benar
while True:
    n = int(input("Input ukuran puzzle nxn yang km maw (n≥3) : "))
    if n < 3:
        cprint("Ukuran puzzle minimal 3x3, input ulang ya bestie", 'red')
    else :
        break

# Simpan skor di file yang pasti bisa diakses
skor_tertinggi = "highscores.txt"

# Membuat papan puzzle yang acak dan valid
def papan_puzzlenya(n):
    angka = list(range(n * n))
    while True:
        random.shuffle(angka)
        inversi = 0
        for i in range(len(angka)):
            for j in range(i + 1, len(angka)):
                if angka[i] != 0 and angka[j] != 0 and angka[i] > angka[j]:
                    inversi += 1
        baris_kosong = n - (angka.index(0) // n)
        if n % 2 == 1:
            if inversi % 2 == 0:
                break
        else:
            if (baris_kosong % 2 == 1 and inversi % 2 == 0) or (baris_kosong % 2 == 0 and inversi % 2 == 1):
                break
    return [angka[i*n:(i+1)*n] for i in range(n)]

# nampilin papan ke layar
def tampilkan_papan(papan):
    os.system('cls')  # atau 'clear' di Linux/Mac
    print("==== Numeric Shuffle ====")
    for baris in papan:
        for angka in baris:
            if angka == 0:
                print(colored("   ", 'white', 'on_white'), end=" ")
            else:
                print(colored(f"{angka:2}", 'magenta'), end=" ")
        print()  
    print()

# Cari posisi si kotak kosong (angka nol) di papan
def cari_kotak_kosong(papan):
    for baris_ke, baris in enumerate(papan):
        if 0 in baris:
            return baris_ke, baris.index(0)

# Mengecek apakah puzzle sudah selesai
def terselesaikan(papan):
    return [num for row in papan for num in row] == list(range(1, n*n)) + [0]

# Fungsi buat geser kotak kosong sesuai tombol panah
def gerak(papan, arah):
    baris, kolom = cari_kotak_kosong(papan)
    gerak = {
        'up': (1, 0),
        'down': (-1, 0),
        'left': (0, 1),
        'right': (0, -1)
    }
    if arah not in gerak:
        return False
    pindah_baris, pindah_kolom = gerak[arah]
    tujuan_baris = baris + pindah_baris
    tujuan_kolom = kolom + pindah_kolom
    if 0 <= tujuan_baris < len(papan) and 0 <= tujuan_kolom < len(papan):
        papan[baris][kolom], papan[tujuan_baris][tujuan_kolom] = papan[tujuan_baris][tujuan_kolom], papan[baris][kolom]
        return True
    return False

# Menyimpan skor ke file
def simpan_skor(nama, langkah, durasi):
    print(f"Menyimpan skor ke: {os.path.abspath(skor_tertinggi)}")
    with open(skor_tertinggi, "a", encoding="utf-8") as f:
        f.write(f"{nama},{langkah},{durasi:.2f}\n")

# Untuk mengambil nilai durasi dari sebuah data skor.
def ambildurasi(data):
    return data[2]

# Buat nampilin skor-skor tertinggi
def tampilkan_skor():
    print(colored("=== Skor Tertinggi ===", 'blue'))
    with open(skor_tertinggi, encoding="utf-8") as file:
        daftar_skor = []
        for baris in file:
            if not baris.strip():
                continue
            nama, langkah, waktu = baris.strip().split(",")
            daftar_skor.append((nama, int(langkah), float(waktu)))
        daftar_skor.sort(key=ambildurasi)
        for urut, (nama, langkah, waktu) in enumerate(daftar_skor, 1):
            print(f"{urut}. {nama} - {langkah} langkah, {waktu} detik")
    print()

# Permainan utama
def program_utama():
    nama = input("Nama km sp seng? : ")
    board = papan_puzzlenya(n)
    langkah = 0
    start = time.time()
    print("Pake tombol panah ni yaa ngegeser2 nya : ↑ ↓ ← →. Tar kalo muak mainnya tekan ESC ajaa untuk keluar ^^")
    time.sleep(4.5)
    while True:
        tampilkan_papan(board)
        print(f"Langkah: {langkah}")
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "up":
                    arah = "up"
                    break
                elif event.name == "down":
                    arah = "down"
                    break
                elif event.name == "left":
                    arah = "left"
                    break
                elif event.name == "right":
                    arah = "right"
                    break
                elif event.name == "esc":
                    print("muak kh maininnya? xixixi dh kluar dr game, tks yh")
                    return
            time.sleep(0.01)
        if gerak(board, arah):
            langkah += 1
        if terselesaikan(board):
            durasi = time.time() - start
            tampilkan_papan(board)
            print(colored(f"asikk congrats yhh {nama}, km dh kelarin game naik tensi dengan tingkat kesulitan {n}x{n} ini dalam {langkah} langkah trs cuma {durasi:.2f} detik. gacor sie >~<", 'green'))
            simpan_skor(nama, langkah, durasi)
            tampilkan_skor()
            break
program_utama()