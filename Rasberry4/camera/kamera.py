import cv2

from ..config import (
    CAMERA_INDEX_EXTERNAL,
    CAMERA_INDEX_INTERNAL
)


# ============================================================
# VARIABEL KAMERA
# ============================================================

kamera = None
kamera_index = None


# ============================================================
# MEMBUKA KAMERA
# ============================================================

def buka_kamera():

    global kamera, kamera_index

    print("--------------------------------")
    print("Mencari kamera EXTERNAL...")
    print("--------------------------------")

    # --------------------------------------------------------
    # PRIORITAS KAMERA USB EXTERNAL
    # --------------------------------------------------------

    for index in CAMERA_INDEX_EXTERNAL:

        print(f"Mencoba kamera external index: {index}")

        cap = cv2.VideoCapture(index)

        if cap.isOpened():

            berhasil, frame = cap.read()

            if berhasil:

                kamera = cap
                kamera_index = index

                # Resolusi kamera
                kamera.set(
                    cv2.CAP_PROP_FRAME_WIDTH,
                    640
                )

                kamera.set(
                    cv2.CAP_PROP_FRAME_HEIGHT,
                    480
                )

                print("--------------------------------")
                print("KAMERA EXTERNAL BERHASIL")
                print(f"Index : {index}")
                print("Resolusi : 640x480")
                print("--------------------------------")

                return True

        cap.release()


    # --------------------------------------------------------
    # JIKA EXTERNAL TIDAK ADA
    # COBA KAMERA INTERNAL
    # --------------------------------------------------------

    print("--------------------------------")
    print("Kamera external tidak ditemukan")
    print("Mencoba kamera INTERNAL...")
    print("--------------------------------")

    cap = cv2.VideoCapture(
        CAMERA_INDEX_INTERNAL
    )

    if cap.isOpened():

        berhasil, frame = cap.read()

        if berhasil:

            kamera = cap
            kamera_index = CAMERA_INDEX_INTERNAL

            kamera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                640
            )

            kamera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                480
            )

            print("--------------------------------")
            print("KAMERA INTERNAL BERHASIL")
            print("--------------------------------")

            return True

        cap.release()


    print("--------------------------------")
    print("TIDAK ADA KAMERA YANG DITEMUKAN")
    print("--------------------------------")

    return False


# ============================================================
# MEMBACA FRAME
# ============================================================

def baca_frame():

    if kamera is None:
        return None

    berhasil, frame = kamera.read()

    if not berhasil:
        return None

    return frame


# ============================================================
# TAMPILAN REALTIME RASPBERRY
# ============================================================

"""
BAGIAN INI SENGAJA TIDAK DIJALANKAN.

Raspberry tidak menampilkan kamera secara langsung.

Kalau suatu saat ingin testing menggunakan monitor Raspberry,
hapus tanda komentar pada bagian ini.

def tampilkan_realtime(frame):

    if frame is None:
        return False

    cv2.imshow(
        "Raspberry 4 - Kamera",
        frame
    )

    tombol = cv2.waitKey(1) & 0xFF

    if tombol == ord("q"):
        return False

    return True

"""


# ============================================================
# MENUTUP KAMERA
# ============================================================

def tutup_kamera():

    global kamera, kamera_index

    if kamera is not None:

        kamera.release()

        kamera = None
        kamera_index = None

    print("Kamera ditutup")