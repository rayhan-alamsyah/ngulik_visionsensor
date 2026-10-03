# ============================================================
# DB_SQL.PY
# Database Quality Control
#
# Database tetap menggunakan file data.db yang sama.
# Tidak membuat database baru setiap program dijalankan.
# ============================================================

import sqlite3
from datetime import datetime
from pathlib import Path


# ============================================================
# LOKASI DATABASE
# ============================================================

ROOT = Path(__file__).resolve().parent

DB = ROOT / "data.db"


# ============================================================
# MEMBUAT KONEKSI DATABASE
# ============================================================

def koneksi():

    return sqlite3.connect(DB)


# ============================================================
# MEMBUAT TABEL
#
# IF NOT EXISTS:
# Kalau tabel sudah ada, tidak dibuat ulang.
# Data lama tetap aman.
# ============================================================

def buat_tabel():

    conn = koneksi()
    cursor = conn.cursor()


    # --------------------------------------------------------
    # TABEL DATA NG
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_ng (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            waktu TEXT NOT NULL,
            jenis_ng TEXT NOT NULL,
            gambar TEXT
        )
    """)


    # --------------------------------------------------------
    # TABEL REKAP HARIAN
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rekap_harian (
            tanggal TEXT PRIMARY KEY,
            short_shot INTEGER DEFAULT 0,
            burn_mark INTEGER DEFAULT 0,
            crack INTEGER DEFAULT 0,
            flash INTEGER DEFAULT 0,
            total_ng INTEGER DEFAULT 0,
            total_good INTEGER DEFAULT 0,
            total_keseluruhan INTEGER DEFAULT 0
        )
    """)


    conn.commit()
    conn.close()


# ============================================================
# SIMPAN HASIL PEMERIKSAAN
#
# jenis_ng = None
# berarti GOOD
#
# jenis_ng:
# - short shot
# - burn mark
# - crack
# - flash
# ============================================================

def simpan_hasil(jenis_ng=None, gambar=None):

    sekarang = datetime.now()

    tanggal = sekarang.strftime("%Y-%m-%d")
    waktu = sekarang.strftime("%H:%M:%S")


    conn = koneksi()
    cursor = conn.cursor()


    # --------------------------------------------------------
    # Pastikan tanggal sudah ada
    # --------------------------------------------------------

    cursor.execute("""
        INSERT OR IGNORE INTO rekap_harian
        (tanggal)
        VALUES (?)
    """, (tanggal,))


    # --------------------------------------------------------
    # Tambahkan total barang
    # --------------------------------------------------------

    cursor.execute("""
        UPDATE rekap_harian
        SET total_keseluruhan =
            total_keseluruhan + 1
        WHERE tanggal = ?
    """, (tanggal,))


    # --------------------------------------------------------
    # Kalau NG
    # --------------------------------------------------------

    if jenis_ng in [
        "short shot",
        "burn mark",
        "crack",
        "flash"
    ]:


        # Simpan detail NG

        cursor.execute("""
            INSERT INTO data_ng
            (
                tanggal,
                waktu,
                jenis_ng,
                gambar
            )
            VALUES (?, ?, ?, ?)
        """, (
            tanggal,
            waktu,
            jenis_ng,
            gambar
        ))


        # ----------------------------------------------------
        # Kolom sesuai jenis NG
        # ----------------------------------------------------

        kolom = {

            "short shot": "short_shot",

            "burn mark": "burn_mark",

            "crack": "crack",

            "flash": "flash"
        }


        nama_kolom = kolom[jenis_ng]


        # ----------------------------------------------------
        # Tambahkan jumlah NG
        # ----------------------------------------------------

        cursor.execute(f"""
            UPDATE rekap_harian

            SET {nama_kolom} =
                {nama_kolom} + 1,

                total_ng =
                total_ng + 1

            WHERE tanggal = ?
        """, (tanggal,))


    # --------------------------------------------------------
    # Hitung GOOD
    # --------------------------------------------------------

    cursor.execute("""
        UPDATE rekap_harian

        SET total_good =
            total_keseluruhan - total_ng

        WHERE tanggal = ?
    """, (tanggal,))


    conn.commit()
    conn.close()


# ============================================================
# BACA SEMUA DATA NG
# ============================================================

def baca_ng():

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM data_ng
        ORDER BY id DESC
    """)


    data = cursor.fetchall()

    conn.close()

    return data


# ============================================================
# BACA REKAP HARIAN
# ============================================================

def baca_rekap():

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM rekap_harian
        ORDER BY tanggal DESC
    """)


    data = cursor.fetchall()

    conn.close()

    return data


# ============================================================
# HAPUS DATA NG
# ============================================================

def hapus_ng(id_ng):

    conn = koneksi()
    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM data_ng
        WHERE id = ?
    """, (id_ng,))


    conn.commit()
    conn.close()


# ============================================================
# TEST DATABASE
# ============================================================

if __name__ == "__main__":

    buat_tabel()

    print("================================")
    print("DATABASE SIAP")
    print("================================")
    print(f"Lokasi database: {DB}")