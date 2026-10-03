from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from pathlib import Path

from .db_sql import (
    buat_tabel,
    simpan_hasil,
    baca_rekap
)

from .crud import (
    read_ng_tanggal,
    delete_ng
)


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)

# Izinkan FrontEnd mengakses Backend
CORS(app)


# ============================================================
# WEBSOCKET
# ============================================================

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


# ============================================================
# DATABASE
# ============================================================

buat_tabel()


# ============================================================
# FOLDER GAMBAR
# ============================================================

ROOT = Path(__file__).resolve().parent

FOLDER_GAMBAR = ROOT / "gambar_ng"

FOLDER_GAMBAR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return "Backend berjalan"


# ============================================================
# TERIMA HASIL NG DARI RASPBERRY
# ============================================================

@app.route("/api/hasil", methods=["POST"])
def terima_hasil():

    jenis_ng = request.form.get("jenis_ng")

    gambar = request.files.get("gambar")


    # --------------------------------------------------------
    # CEK JENIS NG
    # --------------------------------------------------------

    if not jenis_ng:

        return jsonify({
            "status": "error",
            "pesan": "Jenis NG tidak ada"
        }), 400


    # --------------------------------------------------------
    # CEK GAMBAR
    # --------------------------------------------------------

    if not gambar:

        return jsonify({
            "status": "error",
            "pesan": "Gambar tidak ada"
        }), 400


    # --------------------------------------------------------
    # BUAT FOLDER SESUAI JENIS NG
    # --------------------------------------------------------

    nama_folder = jenis_ng.lower().replace(
        " ",
        "_"
    )

    folder = FOLDER_GAMBAR / nama_folder

    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------------
    # SIMPAN GAMBAR
    # --------------------------------------------------------

    nama_file = gambar.filename

    lokasi_gambar = folder / nama_file

    gambar.save(lokasi_gambar)


    # --------------------------------------------------------
    # PATH GAMBAR UNTUK DATABASE
    # --------------------------------------------------------

    path_database = (
        f"gambar_ng/{nama_folder}/{nama_file}"
    )


    # --------------------------------------------------------
    # SIMPAN NG KE DATABASE
    # --------------------------------------------------------

    simpan_hasil(
        jenis_ng=jenis_ng,
        gambar=path_database
    )


    # --------------------------------------------------------
    # KIRIM HASIL NG KE WEBSITE
    # --------------------------------------------------------

    socketio.emit(
        "hasil_baru",
        {
            "status": "ng",
            "jenis_ng": jenis_ng
        }
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "status": "success",

        "jenis_ng": jenis_ng,

        "gambar": path_database

    })


# ============================================================
# TERIMA HASIL GOOD DARI RASPBERRY
# ============================================================

@app.route("/api/status", methods=["POST"])
def terima_status():

    status = request.form.get("status")


    # --------------------------------------------------------
    # CEK STATUS
    # --------------------------------------------------------

    if not status:

        return jsonify({
            "status": "error",
            "pesan": "Status tidak ada"
        }), 400


    # --------------------------------------------------------
    # CEK GOOD
    # --------------------------------------------------------

    if status.lower() != "good":

        return jsonify({
            "status": "error",
            "pesan": "Status harus GOOD"
        }), 400


    # --------------------------------------------------------
    # SIMPAN GOOD
    #
    # Tidak membuat data NG.
    #
    # Database akan:
    #
    # TOTAL +1
    #
    # GOOD dihitung:
    #
    # GOOD = TOTAL - TOTAL NG
    # --------------------------------------------------------

    simpan_hasil(
        jenis_ng=None,
        gambar=None
    )


    # --------------------------------------------------------
    # KIRIM GOOD KE WEBSITE
    # --------------------------------------------------------

    socketio.emit(
        "hasil_baru",
        {
            "status": "good",
            "jenis_ng": None
        }
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "status": "success",

        "hasil": "good"

    })


# ============================================================
# API REKAP HARIAN
# ============================================================

@app.route("/api/rekap", methods=["GET"])
def api_rekap():

    data = baca_rekap()

    return jsonify(data)


# ============================================================
# API DATA NG BERDASARKAN TANGGAL
# ============================================================

@app.route("/api/ng/<tanggal>", methods=["GET"])
def api_ng_tanggal(tanggal):

    data = read_ng_tanggal(tanggal)

    return jsonify(data)


# ============================================================
# API HAPUS DATA NG
# ============================================================

@app.route("/api/ng/<int:id_ng>", methods=["DELETE"])
def api_hapus_ng(id_ng):

    berhasil = delete_ng(id_ng)


    if not berhasil:

        return jsonify({
            "status": "error",
            "pesan": "Data tidak ditemukan"
        }), 404


    return jsonify({

        "status": "success",

        "pesan": "Data berhasil dihapus"

    })


# ============================================================
# GAMBAR NG
# ============================================================

@app.route("/gambar_ng/<path:nama_file>")
def gambar_ng(nama_file):

    return send_from_directory(
        FOLDER_GAMBAR,
        nama_file
    )


# ============================================================
# JALANKAN BACKEND
# ============================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("       BACKEND QUALITY CONTROL")
    print("========================================")
    print("Backend  : http://0.0.0.0:5000")
    print("WebSocket: AKTIF")
    print("========================================")
    print()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False
    )