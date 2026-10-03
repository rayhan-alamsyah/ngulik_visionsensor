# ============================================================
# APP.PY
# PROGRAM UTAMA NGULIK
#
# Urutan:
# 1. Backend / Database
# 2. Camera + YOLO
# 3. FrontEnd
# ============================================================

import subprocess
import sys
import time
import urllib.request
from pathlib import Path


# ============================================================
# FOLDER UTAMA
# ============================================================

ROOT = Path(__file__).resolve().parent


# ============================================================
# MENYIMPAN PROCESS
# ============================================================

proses = []


# ============================================================
# JALANKAN PROGRAM
# ============================================================

def jalankan(nama, command):

    print()
    print("========================================")
    print(f"Menjalankan {nama}...")
    print("========================================")

    try:

        process = subprocess.Popen(
            command,
            cwd=ROOT
        )

        proses.append(process)

        return process

    except Exception as e:

        print(f"[ERROR] Gagal menjalankan {nama}")
        print(e)

        return None


# ============================================================
# MENUNGGU BACKEND READY
# ============================================================

def tunggu_backend():

    print()
    print("Menunggu Backend siap...")

    while True:

        try:

            urllib.request.urlopen(
                "http://127.0.0.1:5000/",
                timeout=1
            )

            print("[OK] Backend sudah READY")

            return True

        except:

            time.sleep(1)


# ============================================================
# MATIKAN SEMUA PROGRAM
# ============================================================

def hentikan_semua():

    print()
    print("Menghentikan semua program...")

    for process in proses:

        if process.poll() is None:

            process.terminate()

    print("Semua program dihentikan")


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():

    print()
    print("========================================")
    print("       SISTEM QUALITY CONTROL")
    print("              NGULIK")
    print("========================================")


    try:

        # ====================================================
        # 1. BACKEND
        # ====================================================

        backend = jalankan(
            "BACKEND / DATABASE",
            [
                sys.executable,
                "-m",
                "BackEnd.app"
            ]
        )


        if backend is None:

            return


        # ----------------------------------------------------
        # TUNGGU BACKEND BENAR-BENAR SIAP
        # ----------------------------------------------------

        if not tunggu_backend():

            print("Backend gagal")

            return


        # ====================================================
        # 2. CAMERA + YOLO
        # ====================================================

        print()
        print("========================================")
        print("Menjalankan CAMERA + YOLO...")
        print("========================================")

        raspberry = jalankan(
            "RASPBERRY CAMERA + YOLO",
            [
                sys.executable,
                "-m",
                "Rasberry4.app"
            ]
        )


        if raspberry is None:

            hentikan_semua()

            return


        # ----------------------------------------------------
        # Beri waktu kamera membuka
        # ----------------------------------------------------

        time.sleep(3)


        # ====================================================
        # 3. FRONTEND
        # ====================================================

        print()
        print("========================================")
        print("Menjalankan FRONTEND...")
        print("========================================")

        frontend = jalankan(
            "FRONTEND",
            [
                sys.executable,
                "FrontEnd/app.py"
            ]
        )


        if frontend is None:

            hentikan_semua()

            return


        # ====================================================
        # SEMUA SUDAH BERJALAN
        # ====================================================

        print()
        print("========================================")
        print("       SEMUA PROGRAM BERHASIL")
        print("========================================")

        print()
        print("Backend  : http://192.168.111.244:5000")
        print("Frontend : http://192.168.111.244:5500")
        print()
        print("Tekan CTRL + C untuk menghentikan.")
        print()


        # ====================================================
        # TUNGGU
        # ====================================================

        while True:

            # Cek apakah salah satu process mati
            for process in proses:

                if process.poll() is not None:

                    print()
                    print("[WARNING] Salah satu program berhenti.")

            time.sleep(2)


    except KeyboardInterrupt:

        print()
        print("CTRL + C diterima")


    finally:

        hentikan_semua()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()