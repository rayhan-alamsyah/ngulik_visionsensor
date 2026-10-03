import cv2
import requests

from datetime import datetime

from ..config import BACKEND_URL


# ============================================================
# KIRIM FOTO NG KE BACKEND
# ============================================================

def kirim_ng(frame, jenis_ng):

    try:

        print("--------------------------------")
        print(
            f"Mengirim NG: {jenis_ng}"
        )
        print("--------------------------------")


        # ----------------------------------------------------
        # NAMA FILE
        # ----------------------------------------------------

        waktu = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        nama_file = (
            f"{jenis_ng}_{waktu}.jpg"
        )


        # ----------------------------------------------------
        # UBAH GAMBAR MENJADI JPG
        # ----------------------------------------------------

        berhasil, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not berhasil:

            print(
                "[ERROR] Gagal membuat JPG"
            )

            return False


        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        data = {
            "jenis_ng": jenis_ng
        }


        files = {

            "gambar": (
                nama_file,
                buffer.tobytes(),
                "image/jpeg"
            )

        }


        # ----------------------------------------------------
        # KIRIM KE BACKEND
        # ----------------------------------------------------

        response = requests.post(

            f"{BACKEND_URL}/api/hasil",

            data=data,

            files=files,

            timeout=5

        )


        # ----------------------------------------------------
        # HASIL
        # ----------------------------------------------------

        if response.status_code == 200:

            print(
                f"[OK] {jenis_ng} berhasil dikirim"
            )

            return True


        print(
            "[ERROR] Backend:",
            response.text
        )

        return False


    except requests.exceptions.ConnectionError:

        print(
            "[ERROR] Backend tidak dapat dihubungi"
        )

        return False


    except requests.exceptions.Timeout:

        print(
            "[ERROR] Koneksi Backend timeout"
        )

        return False


    except Exception as e:

        print(
            "[ERROR]",
            e
        )

        return False