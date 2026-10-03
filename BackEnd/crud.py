# ============================================================
# CRUD.PY
# Mengatur Create, Read, Update, Delete data NG
# ============================================================

import os
from .db_sql import koneksi, simpan_hasil, baca_ng, baca_rekap


# Lokasi folder gambar NG
FOLDER_GAMBAR = "BackEnd/gambar_ng"


# ============================================================
# CREATE
# Menyimpan hasil pemeriksaan
# ============================================================

def create_hasil(jenis_ng=None, gambar=None):
    """
    Menyimpan hasil pemeriksaan ke database.

    jenis_ng:
        None          = GOOD
        short shot
        burn mark
        crack
        flash
    """

    simpan_hasil(
        jenis_ng=jenis_ng,
        gambar=gambar
    )


# ============================================================
# READ
# Membaca semua data NG
# ============================================================

def read_ng():
    return baca_ng()


# ============================================================
# READ
# Membaca rekap harian
# ============================================================

def read_rekap():
    return baca_rekap()


# ============================================================
# READ
# Mencari data NG berdasarkan tanggal
# ============================================================

def read_ng_tanggal(tanggal):
    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM data_ng
        WHERE tanggal = ?
        ORDER BY id DESC
    """, (tanggal,))

    data = cursor.fetchall()

    conn.close()

    return data


# ============================================================
# UPDATE
# Mengubah jenis NG dan/atau gambar
#
# Tanggal dan waktu TIDAK diubah
# ============================================================

def update_ng(id_ng, jenis_ng=None, gambar_baru=None):

    conn = koneksi()
    cursor = conn.cursor()

    # Ambil data lama
    cursor.execute("""
        SELECT tanggal, waktu, jenis_ng, gambar
        FROM data_ng
        WHERE id = ?
    """, (id_ng,))

    data_lama = cursor.fetchone()

    if data_lama is None:
        conn.close()
        return False

    tanggal, waktu, jenis_lama, gambar_lama = data_lama

    # --------------------------------------------------------
    # Kalau jenis NG berubah
    # --------------------------------------------------------

    if jenis_ng is not None and jenis_ng != jenis_lama:

        kolom = {
            "short shot": "short_shot",
            "burn mark": "burn_mark",
            "crack": "crack",
            "flash": "flash"
        }

        # Kurangi jenis NG lama
        cursor.execute(f"""
            UPDATE rekap_harian
            SET {kolom[jenis_lama]} = {kolom[jenis_lama]} - 1
            WHERE tanggal = ?
        """, (tanggal,))

        # Tambahkan jenis NG baru
        cursor.execute(f"""
            UPDATE rekap_harian
            SET {kolom[jenis_ng]} = {kolom[jenis_ng]} + 1
            WHERE tanggal = ?
        """, (tanggal,))

        # Ubah jenis di data NG
        cursor.execute("""
            UPDATE data_ng
            SET jenis_ng = ?
            WHERE id = ?
        """, (jenis_ng, id_ng))

    # --------------------------------------------------------
    # Kalau gambar diganti
    # --------------------------------------------------------

    if gambar_baru is not None:

        cursor.execute("""
            UPDATE data_ng
            SET gambar = ?
            WHERE id = ?
        """, (gambar_baru, id_ng))

        # Hapus gambar lama
        if gambar_lama:
            path_lama = os.path.join(
                FOLDER_GAMBAR,
                os.path.basename(gambar_lama)
            )

            if os.path.exists(path_lama):
                os.remove(path_lama)

    conn.commit()
    conn.close()

    return True


# ============================================================
# DELETE
# Menghapus data NG
# ============================================================

def delete_ng(id_ng):

    conn = koneksi()
    cursor = conn.cursor()

    # Ambil data sebelum dihapus
    cursor.execute("""
        SELECT tanggal, jenis_ng, gambar
        FROM data_ng
        WHERE id = ?
    """, (id_ng,))

    data = cursor.fetchone()

    if data is None:
        conn.close()
        return False

    tanggal, jenis_ng, gambar = data

    kolom = {
        "short shot": "short_shot",
        "burn mark": "burn_mark",
        "crack": "crack",
        "flash": "flash"
    }

    # Hapus data NG
    cursor.execute("""
        DELETE FROM data_ng
        WHERE id = ?
    """, (id_ng,))

    # Kurangi rekap NG
    cursor.execute(f"""
        UPDATE rekap_harian
        SET {kolom[jenis_ng]} = {kolom[jenis_ng]} - 1,
            total_ng = total_ng - 1,
            total_good = total_keseluruhan - (total_ng - 1)
        WHERE tanggal = ?
    """, (tanggal,))

    # Hapus gambar
    if gambar:
        path_gambar = os.path.join(
            FOLDER_GAMBAR,
            os.path.basename(gambar)
        )

        if os.path.exists(path_gambar):
            os.remove(path_gambar)

    conn.commit()
    conn.close()

    return True