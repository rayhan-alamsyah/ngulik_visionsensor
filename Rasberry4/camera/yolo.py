from ultralytics import YOLO

from ..config import (
    MODEL_PATH,
    JENIS_NG
)


# ============================================================
# LOAD MODEL
# ============================================================

print("--------------------------------")
print("Memuat model YOLO NCNN...")
print("--------------------------------")

model = YOLO(
    str(MODEL_PATH)
)

print("--------------------------------")
print("Model YOLO berhasil dimuat")
print("Class YOLO:")

for nomor, nama in model.names.items():

    print(f"{nomor} = {nama}")

print("--------------------------------")


# ============================================================
# DETEKSI YOLO
# ============================================================

def deteksi(frame):

    # --------------------------------------------------------
    # JALANKAN YOLO
    # --------------------------------------------------------

    results = model(
        frame,
        verbose=False
    )


    # --------------------------------------------------------
    # BUAT GAMBAR DENGAN KOTAK DETEKSI
    #
    # HASIL INI AKAN DITAMPILKAN DI BROWSER
    # DAN JUGA BISA DISIMPAN SEBAGAI FOTO NG
    # --------------------------------------------------------

    hasil_gambar = results[0].plot()


    # Default:
    # Tidak ada NG

    jenis_ng = None


    # --------------------------------------------------------
    # PERIKSA HASIL DETEKSI
    # --------------------------------------------------------

    for box in results[0].boxes:

        class_id = int(
            box.cls[0]
        )

        nama_class = model.names[
            class_id
        ]

        nama_class = nama_class.lower()

        print(
            "Terdeteksi:",
            nama_class
        )


        # ----------------------------------------------------
        # CEK APAKAH CLASS ADALAH NG
        # ----------------------------------------------------

        if nama_class in JENIS_NG:

            jenis_ng = nama_class

            break


    # --------------------------------------------------------
    # KEMBALIKAN
    #
    # hasil_gambar = gambar + kotak YOLO
    # jenis_ng     = jenis NG
    # --------------------------------------------------------

    return hasil_gambar, jenis_ng