import threading
import time

from .camera.kamera import (
    buka_kamera,
    baca_frame,
    tutup_kamera
)

from .camera.yolo import deteksi

from .camera.stream import (
    jalankan_stream,
    update_frame
)

from .koneksi.backend import kirim_ng


# ============================================================
# PENGATURAN
# ============================================================

# Berapa kali YOLO boleh kehilangan NG
# sebelum dianggap benda sudah keluar.

NG_MISS_LIMIT = 5


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():

    print()
    print("================================")
    print("       RASPBERRY 4 - QC")
    print("================================")
    print()


    # ========================================================
    # BUKA KAMERA
    # ========================================================

    if not buka_kamera():

        print("Kamera tidak ditemukan")

        return


    # ========================================================
    # JALANKAN SERVER LIVE CAMERA
    # ========================================================

    thread_stream = threading.Thread(
        target=jalankan_stream,
        daemon=True
    )

    thread_stream.start()


    print()
    print("--------------------------------")
    print("LIVE CAMERA AKTIF")
    print("Port : 8000")
    print("--------------------------------")
    print()


    # ========================================================
    # STATUS NG
    # ========================================================

    ng_sudah_dikirim = False

    ng_terakhir = None

    jumlah_ng_hilang = 0


    try:

        # ====================================================
        # LOOP UTAMA
        # ====================================================

        while True:


            # ------------------------------------------------
            # BACA KAMERA
            # ------------------------------------------------

            frame = baca_frame()

            if frame is None:

                print(
                    "Gagal membaca kamera"
                )

                time.sleep(0.1)

                continue


            # ------------------------------------------------
            # YOLO
            # ------------------------------------------------

            hasil, jenis_ng = deteksi(
                frame
            )


            # ------------------------------------------------
            # KIRIM HASIL YOLO KE LIVE CAMERA
            #
            # INI YANG MEMBUAT KOTAK DETEKSI
            # MUNCUL DI BROWSER
            # ------------------------------------------------

            update_frame(
                hasil
            )


            # =================================================
            # JIKA ADA NG
            # =================================================

            if jenis_ng is not None:

                print(
                    f"NG ditemukan: {jenis_ng}"
                )


                # ---------------------------------------------
                # NG MASIH SAMA
                # ---------------------------------------------

                if jenis_ng == ng_terakhir:

                    jumlah_ng_hilang = 0


                # ---------------------------------------------
                # NG BARU
                # ---------------------------------------------

                else:

                    ng_terakhir = jenis_ng

                    jumlah_ng_hilang = 0

                    ng_sudah_dikirim = False


                # ---------------------------------------------
                # KIRIM 1X
                # ---------------------------------------------

                if not ng_sudah_dikirim:

                    print("--------------------------------")
                    print(
                        f"Mengirim NG: {jenis_ng}"
                    )
                    print("--------------------------------")


                    # PENTING:
                    #
                    # KIRIM "hasil", BUKAN "frame"
                    #
                    # Karena "hasil" sudah ada
                    # kotak YOLO.
                    #
                    berhasil = kirim_ng(
                        hasil,
                        jenis_ng
                    )


                    if berhasil:

                        ng_sudah_dikirim = True

                        print("--------------------------------")
                        print(
                            f"[OK] {jenis_ng} berhasil dikirim"
                        )
                        print("--------------------------------")


            # =================================================
            # JIKA TIDAK ADA NG
            # =================================================

            else:

                jumlah_ng_hilang += 1


                # ------------------------------------------------
                # JANGAN LANGSUNG RESET
                #
                # YOLO kadang bisa kehilangan objek beberapa frame.
                # ------------------------------------------------

                if jumlah_ng_hilang >= NG_MISS_LIMIT:

                    ng_sudah_dikirim = False

                    ng_terakhir = None

                    jumlah_ng_hilang = 0


            # ------------------------------------------------
            # TIDAK ADA cv2.imshow()
            # TIDAK ADA cv2.waitKey()
            # ------------------------------------------------


    except KeyboardInterrupt:

        print()
        print("Program dihentikan")


    finally:

        tutup_kamera()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()