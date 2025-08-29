#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBFS Predictor – Prediksi 6 Digit untuk Pola Tarung Togel
Author : You
Python : 3.7+
Fitur  : BBFS 6 Digit, Histori, Backtest, Statistik
"""

import itertools
import os
import sys
import time
from collections import Counter
from typing import List, Dict

# ──────────────────────────────────────────────────────────────
# ANSI color & style helpers
# ──────────────────────────────────────────────────────────────
RESET = "\033[0m"

def colored(text: str, color: str = "white", style: str = "normal") -> str:
    styles = {
        "normal": 0,
        "bold": 1,
        "dim": 2,
        "italic": 3,
        "underline": 4,
    }
    colors = {
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "bright_red": 91,
        "bright_green": 92,
        "bright_yellow": 93,
        "bright_blue": 94,
        "bright_magenta": 95,
        "bright_cyan": 96,
    }
    s = styles.get(style, 0)
    c = colors.get(color, 37)
    return f"\033[{s};{c}m{text}{RESET}"

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# ──────────────────────────────────────────────────────────────
# Banner ASCII
# ──────────────────────────────────────────────────────────────
BANNER = colored(
    r"""
  ____  _                           _   _ 
 |  _ \| |__  _ __ ___   ___     __| | | |
 | |_) | '_ \| '_ ` _ \ / _ \   / _` | | |
 |  __/| | | | | | | | | (_) | | (_| | |_|
 |_|   |_| |_|_| |_| |_|\___/   \__,_| (_)
 
         BBFS PREDICTOR v1.0
     6 Digit untuk Pola Tarung
""",
    "cyan",
    "bold",
)

# ──────────────────────────────────────────────────────────────
# Data Mistik (bisa Anda sesuaikan)
# ──────────────────────────────────────────────────────────────
mistik_baru = {0: 8, 1: 7, 2: 6, 3: 9, 4: 5}
mistik_lama = {0: 1, 2: 5, 3: 8, 4: 7, 6: 9}

tabel_ekor_abadi = {
    0: [4, 6, 8, 1, 3, 7],
    1: [3, 5, 9, 2, 4, 8],
    2: [0, 6, 4, 7, 5, 9],
    3: [1, 7, 2, 8, 9, 0],
    4: [0, 2, 6, 1, 5, 9],
    5: [1, 3, 6, 4, 0, 2],
    6: [0, 4, 8, 1, 7, 9],
    7: [1, 3, 5, 2, 4, 8],
    8: [0, 6, 4, 7, 5, 9],
    9: [1, 5, 7, 0, 2, 6],
}

HISTORY_FILE = "history.txt"

# ──────────────────────────────────────────────────────────────
# Load & Save Histori
# ──────────────────────────────────────────────────────────────
def load_history() -> List[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            lines = [line.strip() for line in f if line.strip().isdigit() and len(line.strip()) == 4]
        return lines
    except:
        return []

def save_history(history: List[str]) -> None:
    with open(HISTORY_FILE, "w") as f:
        f.write("\n".join(history))

# ──────────────────────────────────────────────────────────────
# Prediksi BBFS 6 Digit
# ──────────────────────────────────────────────────────────────
def generate_bbfs_6_digit(previous: str, history: List[str]) -> List[str]:
    candidates = Counter()

    a, k, e = int(previous[0]), int(previous[1]), int(previous[3])
    total_4d = sum(int(d) for d in previous) % 10
    total_ak = (a + k) % 10

    # 1. Mistik
    for d in [a, k, e]:
        if d in mistik_baru: candidates[mistik_baru[d]] += 4
        if d in mistik_lama: candidates[mistik_lama[d]] += 4

    # 2. Ekor abadi → digit yang sering muncul setelah ekor
    ekor_next = tabel_ekor_abadi.get(e, [])
    for digit in ekor_next:
        candidates[digit] += 3

    # 3. Tesson 2 & 3
    tesson2 = (e * e) % 10
    tesson3 = (e * e * e) % 10
    candidates[tesson2] += 2
    candidates[tesson3] += 2

    # 4. Digit dari 4D sebelumnya
    for d_char in previous:
        d = int(d_char)
        candidates[d] += 1

    # 5. Total a+k dan total 4D
    candidates[total_ak] += 3
    candidates[total_4d] += 2

    # 6. Frekuensi historis (angka dingin dapat bonus)
    freq = Counter()
    for res in history:
        for char in res:
            freq[int(char)] += 1

    for digit in range(10):
        if freq[digit] == 0:
            candidates[digit] += 5  # sangat dingin
        elif freq[digit] < 2:
            candidates[digit] += 2

    # Ambil 6 digit terkuat
    top_6 = [str(item[0]) for item in candidates.most_common(6)]
    return sorted(top_6, key=lambda x: int(x))

# ──────────────────────────────────────────────────────────────
# Hitung kombinasi unik dari BBFS
# ──────────────────────────────────────────────────────────────
def count_combinations(bbfs: List[str]) -> int:
    combos = itertools.product(bbfs, repeat=4)
    return len(set(combos))

# ──────────────────────────────────────────────────────────────
# Backtest BBFS
# ──────────────────────────────────────────────────────────────
def backtest(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data untuk backtest!", "red"))
        input(colored("\nTekan Enter...", "dim"))
        return

    benar = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST BBFS ({total} putaran)", "bright_yellow", "bold"))

    for i in range(total):
        prev = history[i]
        actual = history[i + 1]
        actual_digits = set(actual)

        bbfs = generate_bbfs_6_digit(prev, history[:i+1])
        bbfs_set = set(bbfs)

        # Cek apakah semua digit di actual ada di BBFS (ideal)
        match_count = len([d for d in actual_digits if d in bbfs_set])
        full_match = match_count == 4
        partial_match = match_count >= 2

        if full_match:
            status = "✅"
            benar += 1
        elif partial_match:
            status = "🟡"
        else:
            status = "❌"

        print(f"{status} {prev} → {actual} | Match: {match_count}/4 | BBFS: {''.join(bbfs)}")

    akurasi = (benar / total) * 100
    warna = "green" if akurasi >= 70 else "yellow" if akurasi >= 50 else "red"
    print(colored(f"\n📊 Akurasi Full Match: {benar}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter untuk kembali...", "dim"))

# ──────────────────────────────────────────────────────────────
# Statistik Frekuensi Digit
# ──────────────────────────────────────────────────────────────
def show_stats(history: List[str]) -> None:
    freq = Counter()
    for result in history:
        for char in result:
            freq[char] += 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1])

    print(colored(f"\n🔥 5 Digit Terpanas:", "bright_red", "bold"))
    for digit, cnt in sorted_freq[-5:]:
        print(f"  {colored(digit, 'bright_red')} → {cnt}x")

    print(colored(f"\n❄️ 5 Digit Terdingin:", "bright_cyan", "bold"))
    for digit, cnt in sorted_freq[:5]:
        print(f"  {colored(digit, 'bright_cyan')} → {cnt}x")

    input(colored("\nTekan Enter untuk kembali...", "dim"))

# ──────────────────────────────────────────────────────────────
# Animasi loading
# ──────────────────────────────────────────────────────────────
def loading_animation(duration: float = 1.2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(int(duration * 10)):
        sys.stdout.write("\r" + colored(frames[_ % len(frames)], "cyan") + " Analisis pola...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ──────────────────────────────────────────────────────────────
# Menu Utama
# ──────────────────────────────────────────────────────────────
def menu() -> None:
    history = load_history()
    while True:
        clear_screen()
        print(BANNER)
        print(colored(f"\n📁 Histori: {len(history)} data", "blue", "dim"))
        print(colored("\n [1] Prediksi BBFS 6 Digit", "bright_green"))
        print(colored(" [2] Tambah Histori Manual", "cyan"))
        print(colored(" [3] Backtest Otomatis", "bright_yellow"))
        print(colored(" [4] Statistik Frekuensi", "magenta"))
        print(colored(" [5] Hapus Semua Histori", "red"))
        print(colored(" [6] Keluar\n", "bright_red"))

        choice = input(colored("Pilih menu: ", "yellow")).strip()

        if choice == "1":
            previous = input(colored("\nMasukkan 4 digit hasil sebelumnya (contoh 5287): ", "cyan")).strip()
            if not previous.isdigit() or len(previous) != 4:
                print(colored("Input harus 4 digit angka!", "red"))
                input(colored("\nTekan Enter...", "dim"))
                continue
            loading_animation()
            bbfs = generate_bbfs_6_digit(previous, history)
            combo_count = count_combinations(bbfs)

            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 BBFS 6 DIGIT (Pola Tarung):", "bright_magenta", "bold"))
            print(" → " + colored("  ".join(bbfs), "bright_yellow", "bold"))
            print(colored(f"\n🔢 Total kombinasi unik: {combo_count:,}", "cyan"))
            print(colored(f"\n💡 Tips:\n   • Gunakan untuk BBFS 6 digit\n   • Cocok untuk colok bebas & 4D\n   • Filter dengan ekor jitu", "dim"))
            input(colored("\n\nTekan Enter untuk kembali...", "dim"))

        elif choice == "2":
            print(colored("\nMasukkan hasil 4D (misal: 5287). Kosongkan untuk selesai.", "cyan"))
            added = 0
            while True:
                inp = input(f"Hasil {len(history) + added + 1}: ").strip()
                if not inp:
                    break
                if inp.isdigit() and len(inp) == 4:
                    history.append(inp)
                    added += 1
                    print(colored("✓ Ditambahkan", "green"))
                else:
                    print(colored("✗ Harus 4 digit angka!", "red"))
            if added > 0:
                save_history(history)

        elif choice == "3":
            backtest(history)

        elif choice == "4":
            show_stats(history)

        elif choice == "5":
            if input(colored("\nYakin hapus semua histori? (y/t): ", "red")).lower() == 'y':
                history = []
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                print(colored("📁 Histori dihapus.", "green"))
                time.sleep(1)

        elif choice == "6":
            print(colored("\nTerima kasih! Semoga JP besar! 🍀", "bright_yellow"))
            break

        else:
            print(colored("Pilihan tidak valid!", "red"))
            input(colored("\nTekan Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Jalankan aplikasi
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(colored("\n\nProgram dihentikan paksa.", "red"))
