from deepface import DeepFace
import cv2
import os
from datetime import datetime

# Path database wajah
database_path = "C:/Users/moh rohmad nur/OneDrive/Documents/UNSRI DOC/BI OJK HACKATHON 2025/Lomba/Face_Recognition/database"
model_name = "Facenet"  # Lebih cepat dari VGG-Face
log_file = "log_verifikasi.txt"

# Inisialisasi webcam
cam = cv2.VideoCapture(0)
cv2.namedWindow("Verifikasi Wajah")

print("Kamera aktif. Silakan tampilkan wajah Anda...")
print("Tekan tombol 'c' untuk verifikasi wajah, atau 'Esc' untuk keluar.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Kamera tidak tersedia.")
        break

    # Tampilkan frame kamera
    cv2.imshow("Verifikasi Wajah", frame)

    key = cv2.waitKey(1)

    if key == 27:  # Tombol Esc
        print("Proses dibatalkan.")
        break

    elif key == ord('c'):  # Tombol 'c' ditekan
        try:
            print("Memproses wajah...")

            # Verifikasi wajah dari frame
            result = DeepFace.find(img_path=frame, db_path=database_path,
                                   model_name=model_name, enforce_detection=False)

            if len(result) > 0 and len(result[0]) > 0:
                identity_path = result[0].iloc[0]["identity"]
                filename = os.path.basename(identity_path)        
                nama = os.path.splitext(filename)[0]              
                label = f"Wajah Terverifikasi: {nama}"
                warna = (0, 255, 0)
                status = "TERVERIFIKASI"
            else:
                label = "Gagal Verifikasi"
                warna = (0, 0, 255)
                nama = "-"
                status = "GAGAL"

            # Tampilkan hasil verifikasi pada frame
            cv2.putText(frame, label, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, warna, 2)
            cv2.imshow("Verifikasi Wajah", frame)
            cv2.waitKey(5000)

            # Simpan log hasil
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a") as f:
                f.write(f"{waktu} | Nama: {nama} | Status: {status}\n")
                print(f"Log disimpan: {nama}, status: {status}")

            break  # Selesai setelah 1 kali verifikasi

        except Exception as e:
            print("Terjadi error:", str(e))
            cv2.putText(frame, "Gagal memproses wajah", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 2)
            cv2.imshow("Verifikasi Wajah", frame)
            cv2.waitKey(5000)
            break

# Tutup kamera dan jendela
cam.release()
cv2.destroyAllWindows()
