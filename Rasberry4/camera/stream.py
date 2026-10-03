import cv2
import time

from flask import Flask, Response

from ..config import STREAM_FPS


# ============================================================
# FLASK CAMERA SERVER
# ============================================================

app = Flask(__name__)


# ============================================================
# FRAME TERBARU
# ============================================================

frame_terbaru = None


# ============================================================
# UPDATE FRAME
# ============================================================

def update_frame(frame):

    global frame_terbaru

    frame_terbaru = frame


# ============================================================
# GENERATOR VIDEO
# ============================================================

def generate_frame():

    waktu_tunggu = 1 / STREAM_FPS

    while True:

        # Ambil frame terbaru
        frame = frame_terbaru

        if frame is None:

            time.sleep(0.1)

            continue


        # ----------------------------------------------------
        # UBAH FRAME MENJADI JPG
        # ----------------------------------------------------

        berhasil, buffer = cv2.imencode(
            ".jpg",
            frame,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                70
            ]
        )

        if not berhasil:

            continue


        gambar = buffer.tobytes()


        # ----------------------------------------------------
        # KIRIM KE BROWSER
        # ----------------------------------------------------

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + gambar
            + b"\r\n"
        )


        time.sleep(
            waktu_tunggu
        )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return "Raspberry Camera Server berjalan"


# ============================================================
# LIVE CAMERA
# ============================================================

@app.route("/video")
def video():

    return Response(
        generate_frame(),
        mimetype=(
            "multipart/x-mixed-replace; "
            "boundary=frame"
        )
    )


# ============================================================
# JALANKAN SERVER CAMERA
# ============================================================

def jalankan_stream():

    print("--------------------------------")
    print("LIVE CAMERA SERVER")
    print("--------------------------------")
    print("Port : 8000")
    print("--------------------------------")

    app.run(
        host="0.0.0.0",
        port=8000,
        threaded=True,
        debug=False,
        use_reloader=False
    )