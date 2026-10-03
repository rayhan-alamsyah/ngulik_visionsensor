from flask import Flask, send_from_directory, jsonify, request
from pathlib import Path
from openpyxl import Workbook, load_workbook
import socket


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# QC_OJT/
ROOT_DIR = BASE_DIR.parent.parent

# File Excel
EXCEL_FILE = ROOT_DIR / "data" / "QC.xlsx"

# Folder foto
PHOTO_DIR = ROOT_DIR / "data" / "foto"


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)


# ============================================================
# MEMBUAT FOLDER
# ============================================================

PHOTO_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# MEMBUAT EXCEL JIKA BELUM ADA
# ============================================================

def create_excel_if_not_exists():

    if EXCEL_FILE.exists():
        return

    EXCEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "QC"

    # --------------------------------------------------------
    # REKAP
    # --------------------------------------------------------

    sheet["A1"] = "REKAP"

    sheet["A2"] = "Tanggal"
    sheet["B2"] = "GOOD"
    sheet["C2"] = "NG Upper Kiri"
    sheet["D2"] = "NG Upper Kanan"
    sheet["E2"] = "NG Lower Kiri"
    sheet["F2"] = "NG Lower Kanan"

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    sheet["H1"] = "DATA"

    headers = [
        "ID",
        "No",
        "Tanggal",
        "Waktu",
        "Foto",
        "Tinggi Kiri",
        "Tinggi Kanan",
        "Upper Kiri",
        "Lower Kiri",
        "Upper Kanan",
        "Lower Kanan",
        "Hasil"
    ]

    for column, header in enumerate(headers, start=8):

        sheet.cell(
            row=2,
            column=column
        ).value = header

    workbook.save(EXCEL_FILE)


# ============================================================
# MEMBACA DATA EXCEL
# ============================================================

def read_data():

    create_excel_if_not_exists()

    workbook = load_workbook(
        EXCEL_FILE
    )

    sheet = workbook["QC"]

    data = []

    # Data mulai dari baris 3
    for row in sheet.iter_rows(
        min_row=3,
        values_only=True
    ):

        # Kolom H sampai S
        # H = ID
        # I = No
        # J = Tanggal
        # K = Waktu
        # L = Foto
        # M = Tinggi Kiri
        # N = Tinggi Kanan
        # O = Upper Kiri
        # P = Lower Kiri
        # Q = Upper Kanan
        # R = Lower Kanan
        # S = Hasil

        if row[0] is None:
            continue

        data.append({
            "id": row[0],
            "no": row[1],
            "tanggal": row[2],
            "waktu": row[3],
            "foto": row[4],
            "tinggi_kiri": row[5],
            "tinggi_kanan": row[6],
            "upper_kiri": row[7],
            "lower_kiri": row[8],
            "upper_kanan": row[9],
            "lower_kanan": row[10],
            "hasil": row[11]
        })

    workbook.close()

    return data


# ============================================================
# HALAMAN WEB
# ============================================================

@app.route("/")
def index():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# ============================================================
# CSS
# ============================================================

@app.route("/css/<path:filename>")
def css(filename):

    return send_from_directory(
        BASE_DIR / "css",
        filename
    )


# ============================================================
# JAVASCRIPT
# ============================================================

@app.route("/js/<path:filename>")
def javascript(filename):

    return send_from_directory(
        BASE_DIR / "js",
        filename
    )


# ============================================================
# TEST
# ============================================================

@app.route("/api/test")
def api_test():

    return jsonify({
        "status": "ok",
        "message": "Web QC terhubung ke Raspberry Pi"
    })


# ============================================================
# DATA QC
# ============================================================

@app.route("/api/data")
def api_data():

    data = read_data()

    return jsonify(data)


# ============================================================
# EDIT DATA
# ============================================================

@app.route("/api/edit", methods=["POST"])
def edit_data():

    create_excel_if_not_exists()

    request_data = request.json

    data_id = request_data.get("id")

    if not data_id:

        return jsonify({
            "status": "error",
            "message": "ID data tidak ditemukan"
        }), 400


    workbook = load_workbook(
        EXCEL_FILE
    )

    sheet = workbook["QC"]


    # Cari ID
    target_row = None

    for row in range(3, sheet.max_row + 1):

        excel_id = sheet.cell(
            row=row,
            column=8
        ).value

        if str(excel_id) == str(data_id):

            target_row = row
            break


    if target_row is None:

        workbook.close()

        return jsonify({
            "status": "error",
            "message": "Data tidak ditemukan"
        }), 404


    # --------------------------------------------------------
    # Update data
    # --------------------------------------------------------

    sheet.cell(
        target_row,
        10
    ).value = request_data.get("tanggal")

    sheet.cell(
        target_row,
        11
    ).value = request_data.get("waktu")

    sheet.cell(
        target_row,
        13
    ).value = request_data.get("tinggi_kiri")

    sheet.cell(
        target_row,
        14
    ).value = request_data.get("tinggi_kanan")

    sheet.cell(
        target_row,
        15
    ).value = request_data.get("upper_kiri")

    sheet.cell(
        target_row,
        16
    ).value = request_data.get("lower_kiri")

    sheet.cell(
        target_row,
        17
    ).value = request_data.get("upper_kanan")

    sheet.cell(
        target_row,
        18
    ).value = request_data.get("lower_kanan")

    sheet.cell(
        target_row,
        19
    ).value = request_data.get("hasil")


    workbook.save(EXCEL_FILE)

    workbook.close()


    return jsonify({
        "status": "ok",
        "message": "Data berhasil diubah"
    })


# ============================================================
# HAPUS DATA
# ============================================================

@app.route("/api/delete", methods=["POST"])
def delete_data():

    create_excel_if_not_exists()

    request_data = request.json

    data_id = request_data.get("id")

    if not data_id:

        return jsonify({
            "status": "error",
            "message": "ID data tidak ditemukan"
        }), 400


    workbook = load_workbook(
        EXCEL_FILE
    )

    sheet = workbook["QC"]


    target_row = None
    photo_name = None


    # Cari ID
    for row in range(3, sheet.max_row + 1):

        excel_id = sheet.cell(
            row=row,
            column=8
        ).value

        if str(excel_id) == str(data_id):

            target_row = row

            photo_name = sheet.cell(
                row=row,
                column=12
            ).value

            break


    if target_row is None:

        workbook.close()

        return jsonify({
            "status": "error",
            "message": "Data tidak ditemukan"
        }), 404


    # --------------------------------------------------------
    # Hapus baris Excel
    # --------------------------------------------------------

    sheet.delete_rows(
        target_row,
        1
    )


    workbook.save(
        EXCEL_FILE
    )

    workbook.close()


    # --------------------------------------------------------
    # Hapus foto jika ada
    # --------------------------------------------------------

    if photo_name:

        photo_path = PHOTO_DIR / str(photo_name)

        if photo_path.exists():

            photo_path.unlink()


    return jsonify({
        "status": "ok",
        "message": "Data berhasil dihapus"
    })


# ============================================================
# MENCARI IP
# ============================================================

def get_ip_address():

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        sock.connect(
            ("8.8.8.8", 80)
        )

        ip = sock.getsockname()[0]

        sock.close()

        return ip

    except Exception:

        return "127.0.0.1"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    create_excel_if_not_exists()

    ip = get_ip_address()

    print()
    print("=" * 55)
    print("              SISTEM QUALITY CONTROL")
    print("=" * 55)
    print()
    print("Web server aktif")
    print()
    print("Raspberry Pi:")
    print("http://localhost:5000")
    print()
    print("HP / Laptop:")
    print(f"http://{ip}:5000")
    print()
    print("Excel:")
    print(EXCEL_FILE)
    print()
    print("=" * 55)
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )