document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('enter-btn');
    if (btn) {
        btn.addEventListener('click', function() {
            alert('Tombol ENTER berfungsi!');
        });
    } else {
        alert('Tombol ENTER tidak ditemukan!');
    }
});
