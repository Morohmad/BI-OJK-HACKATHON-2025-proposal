import base64
import os
import sys
import tempfile
import traceback
from flask import Flask, jsonify, request, send_from_directory

# 1. Pengaturan Path Dasar dan Isolasi Modul Eksplisit
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastikan Root Proyek ada di dalam sys.path agar Absolute Import bekerja
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Tetap definisikan FR_SRC dan LV_SRC di tingkat global agar bisa dibaca oleh rute Audit Log
FR_SRC = os.path.join(ROOT_DIR, "Face_Recognition", "src")
LV_SRC = os.path.join(ROOT_DIR, "Location_Validation", "src")

# 2. Amankan proses import submodul lokal menggunakan gaya Absolute Import
try:
    from Face_Recognition.src.verify import FaceVerifier
except Exception as err:
    import traceback

    traceback.print_exc()      # tampilkan traceback asli
    FaceVerifier = None
    face_verifier_error = str(err)
else:
    face_verifier_error = None

try:
    from Location_Validation.src.validator import LocationValidator
except Exception as err:
    LocationValidator = None
    location_validator_error = str(err)
else:
    location_validator_error = None

# 3. Inisialisasi Aplikasi Flask
app = Flask(__name__, static_folder="web", static_url_path="")

face_verifier = None
location_validator = None
STATIC_FOLDER = os.path.join(ROOT_DIR, "web")


def get_face_verifier():
    global face_verifier
    if face_verifier is None:
        if FaceVerifier is None:
            raise RuntimeError(f"Modul FaceVerifier gagal diinisialisasi: {face_verifier_error}")
        face_verifier = FaceVerifier()
    return face_verifier


def get_location_validator():
    global location_validator
    if location_validator is None:
        if LocationValidator is None:
            raise RuntimeError(f"Modul LocationValidator gagal diinisialisasi: {location_validator_error}")
        location_validator = LocationValidator()
    return location_validator


def decode_data_uri(data_uri):
    try:
        header, encoded = data_uri.split(",", 1)
        return base64.b64decode(encoded)
    except Exception:
        raise ValueError("Format base64 image data URI tidak valid.")


def read_log_lines(path, limit=10):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()][-limit:][::-1]
    except Exception:
        return []


# 4. Routing API Aplikasi
@app.route("/")
def index():
    return send_from_directory(STATIC_FOLDER, "index.html")


@app.route("/api/verify-face", methods=["POST"])
def verify_face():
    try:
        payload = request.get_json(force=True) or {}
        image_data = payload.get("image")

        if not image_data:
            return jsonify(error="Gambar wajah kosong atau tidak terkirim."), 400

        image_bytes = decode_data_uri(image_data)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_path = temp_file.name

        try:
            verifier = get_face_verifier()
            verified, name, distance = verifier.verify(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return jsonify(
            verified=bool(verified),
            name=name,
            distance=distance,
        )
    except Exception as err:
        # PENTING: Ini akan memaksa python mencetak error lengkap ke terminal VS Code Anda
        print("\n=== ERROR DETAIL PADA VERIFY FACE ===")
        traceback.print_exc()
        print("=====================================\n")
        return jsonify(error=f"Internal Server Error: {str(err)}"), 500


@app.route("/api/validate-location", methods=["POST"])
def validate_location():
    try:
        payload = request.get_json(force=True) or {}
        latitude = payload.get("latitude")
        longitude = payload.get("longitude")

        if latitude is None or longitude is None:
            return jsonify(error="Parameter koordinat latitude dan longitude tidak lengkap."), 400

        validator = get_location_validator()
        valid, point_name, distance = validator.validate(float(latitude), float(longitude))

        max_distance = getattr(validator, "MAX_DISTANCE", None)
        if max_distance is None:
            try:
                # Menggunakan import absolut yang aman dari submodul lokasi
                from Location_Validation.src.config import MAX_DISTANCE
                max_distance = MAX_DISTANCE
            except ImportError:
                max_distance = 1000

        return jsonify(
            valid=bool(valid),
            point_name=point_name,
            distance=distance,
            max_distance=max_distance,
        )
    except Exception as err:
        return jsonify(error=f"Internal Server Error: {str(err)}"), 500


@app.route("/api/audit-log", methods=["GET"])
def audit_log():
    # Menggunakan variabel global FR_SRC dan LV_SRC yang sekarang sudah didefinisikan aman di atas
    face_log_path = os.path.join(FR_SRC, "log_verifikasi.txt")
    location_log_path = os.path.join(LV_SRC, "location_log.txt")

    return jsonify(
        face_log=read_log_lines(face_log_path, limit=10),
        location_log=read_log_lines(location_log_path, limit=10),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)