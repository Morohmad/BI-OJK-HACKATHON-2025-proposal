// ==========================================
// 1. Deklarasi Elemen UI / DOM Selector
// ==========================================
const previewVideo = document.getElementById("preview-video");
const cameraFrame = document.querySelector(".camera-frame");
const toggleCameraBtn = document.getElementById("toggle-camera-btn");
const verifyFaceBtn = document.getElementById("verify-face-btn");
const refreshCameraBtn = document.getElementById("refresh-camera-btn"); // Tombol Refresh Baru

// Panel Hasil Pemindaian Wajah
const faceResultName = document.getElementById("face-result-name");
const faceResultStatus = document.getElementById("face-result-status");
const faceResultConfidence = document.getElementById("face-result-confidence");
const faceResultNote = document.getElementById("face-result-note");

// Panel Validasi Lokasi
const locResultStatus = document.getElementById("loc-result-status");
const locResultPoint = document.getElementById("loc-result-point");
const locResultDistance = document.getElementById("loc-result-distance");
const locResultNote = document.getElementById("loc-result-note");

// Container Log Audit
const faceLogContainer = document.getElementById("face-log-container");
const locLogContainer = document.getElementById("loc-log-container");

let currentStream = null;

// ==========================================
// 2. Fungsi Manajemen Kamera & Stream
// ==========================================

// Fungsi Hidupkan Kamera
async function startCamera() {
  try {
    // Reset informasi visual di UI saat kamera dinyalakan lagi
    faceResultStatus.textContent = "Menunggu Pemindaian...";
    faceResultNote.textContent = "Silakan posisikan wajah Anda tepat di depan kamera.";
    
    currentStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 }
    });
    previewVideo.srcObject = currentStream;
    previewVideo.play();
    cameraFrame.classList.add("active");
    toggleCameraBtn.textContent = "Matikan Kamera";
    refreshCameraBtn.style.display = "none"; // Sembunyikan tombol ulangi saat aktif
  } catch (error) {
    alert("Gagal mengakses kamera: " + error.message);
  }
}

// Fungsi Matikan Kamera Manual
function stopCamera() {
  if (currentStream) {
    const tracks = currentStream.getTracks();
    tracks.forEach(track => track.stop());
  }
  previewVideo.srcObject = null;
  cameraFrame.classList.remove("active");
  toggleCameraBtn.textContent = "Aktifkan Kamera";
  currentStream = null;
  refreshCameraBtn.style.display = "none";
}

// Handler Tombol Utama Toggle Kamera
toggleCameraBtn.addEventListener("click", () => {
  if (currentStream) {
    stopCamera();
  } else {
    startCamera();
  }
});

// Handler Tombol Ulangi Kamera (Refresh)
refreshCameraBtn.addEventListener("click", async () => {
  await startCamera();
});

// Fungsi Mengambil Gambar Singkat dari Aliran Video (Snapshot)
function captureImageFromVideo() {
  const canvas = document.createElement("canvas");
  canvas.width = previewVideo.videoWidth || 640;
  canvas.height = previewVideo.videoHeight || 480;
  
  const ctx = canvas.getContext("2d");
  // Gambar frame video ke canvas saat ini
  ctx.drawImage(previewVideo, 0, 0, canvas.width, canvas.height);
  
  // Ubah menjadi format Data URL Base64
  return canvas.toDataURL("image/png");
}

// ==========================================
// 3. Fungsi Core API: Verifikasi Wajah
// ==========================================
async function verifyFace() {
  try {
    if (!currentStream) {
      faceResultNote.textContent = "Aktifkan kamera terlebih dahulu.";
      return;
    }

    faceResultStatus.textContent = "Memproses...";
    verifyFaceBtn.disabled = true;

    // A. Ambil potret gambar saat ini
    const imageData = captureImageFromVideo();

    // B. LANGSUNG BERHENTIKAN KAMERA (Efek 'Cekrek' / Freeze)
    const tracks = currentStream.getTracks();
    tracks.forEach(track => track.stop());
    
    previewVideo.srcObject = null;
    cameraFrame.classList.remove('active');
    currentStream = null;

    // C. Munculkan tombol Ulangi (Refresh) & ganti teks toggle utama
    refreshCameraBtn.style.display = "inline-flex";
    toggleCameraBtn.textContent = "Aktifkan Kamera";

    // D. Kirim gambar ke API Backend Flask
    const response = await fetch("/api/verify-face", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData }),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Pencocokan wajah gagal.");
    }

    // E. Render Hasil Recognisi ke UI Halaman Web
    faceResultName.textContent = result.name || "Tidak Dikenal";
    faceResultStatus.textContent = result.verified ? "Terverifikasi" : "Ditolak";
    faceResultConfidence.textContent = result.distance ? `${result.distance.toFixed(4)}` : "-";
    faceResultNote.textContent = result.verified ? "Identitas KPM sesuai." : "Wajah tidak cocok.";

    // Perbarui tabel log audit log setelah pemindaian berhasil
    await fetchAuditLog();

  } catch (error) {
    faceResultName.textContent = "-";
    faceResultStatus.textContent = "Gagal Sistem";
    faceResultConfidence.textContent = "-";
    faceResultNote.textContent = error.message; 
  } finally {
    verifyFaceBtn.disabled = false;
  }
}

verifyFaceBtn.addEventListener("click", verifyFace);

// ==========================================
// 4. Fungsi Core API: Validasi Lokasi GPS
// ==========================================
async function validateLocation() {
  locResultStatus.textContent = "Mencari Koordinat...";
  locResultNote.textContent = "Meminta izin GPS perangkat Anda...";

  if (!navigator.geolocation) {
    locResultStatus.textContent = "Gagal";
    locResultNote.textContent = "Fitur Geolocation tidak didukung oleh browser ini.";
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      try {
        const { latitude, longitude } = position.coords;
        locResultStatus.textContent = "Memvalidasi...";

        const response = await fetch("/api/validate-location", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ latitude, longitude }),
        });

        const result = await response.json();

        if (!response.ok) {
          throw new Error(result.error || "Validasi lokasi gagal.");
        }

        // Render hasil validasi lokasi ke UI
        locResultPoint.textContent = result.point_name || "-";
        locResultStatus.textContent = result.valid ? "Sesuai Radius" : "Di Luar Radius";
        locResultDistance.textContent = result.distance ? `${result.distance.toFixed(2)} meter` : "-";
        
        locResultNote.textContent = result.valid 
          ? "Lokasi penyaluran valid dan masuk dalam batas aman." 
          : `Jarak terlalu jauh dari titik sasaran (Maksimal ${result.max_distance}m).`;

        await fetchAuditLog();
      } catch (error) {
        locResultStatus.textContent = "Gagal Sistem";
        locResultNote.textContent = error.message;
      }
    },
    (error) => {
      locResultStatus.textContent = "Akses Ditolak";
      locResultNote.textContent = "Gagal mengambil lokasi: " + error.message;
    },
    { enableHighAccuracy: true, timeout: 10000 }
  );
}

document.getElementById("validate-loc-btn").addEventListener("click", validateLocation);

// ==========================================
// 5. Polling & Render Log Audit Tabel
// ==========================================
async function fetchAuditLog() {
  try {
    const response = await fetch("/api/audit-log");
    if (!response.ok) return;

    const data = await response.json();

    // Render Log Verifikasi Wajah
    faceLogContainer.innerHTML = data.face_log.length 
      ? data.face_log.map(log => `<div class="audit-row"><div>${log}</div></div>`).join("")
      : '<div class="audit-row" style="color:#94a3b8; text-align:center;">Belum ada riwayat verifikasi.</div>';

    // Render Log Validasi Lokasi
    locLogContainer.innerHTML = data.location_log.length 
      ? data.location_log.map(log => `<div class="audit-row"><div>${log}</div></div>`).join("")
      : '<div class="audit-row" style="color:#94a3b8; text-align:center;">Belum ada riwayat lokasi.</div>';

  } catch (e) {
    console.error("Gagal memperbarui log audit:", e);
  }
}

// Muat log audit pertama kali saat halaman web dibuka
window.addEventListener("DOMContentLoaded", fetchAuditLog);