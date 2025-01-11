// Animasi untuk gambar produk
document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.add('clicked');
        setTimeout(() => {
            card.classList.remove('clicked');
        }, 300);
    });
});

// Smooth scroll untuk tombol yang mengarah ke bagian tertentu di halaman
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animasi untuk tombol "Lihat Produk" dan "Hubungi Kami"
document.querySelectorAll('.button-animation').forEach(button => {
    button.addEventListener('click', function (e) {
        // Mencegah default behavior
        e.preventDefault();

        // Tambahkan class untuk animasi
        this.classList.add('clicked');

        // Hapus class setelah animasi selesai
        setTimeout(() => {
            this.classList.remove('clicked');
        }, 300);

        // Jika tombol "Lihat Produk", periksa status login
        if (this.textContent.includes("Lihat Produk")) {
            checkLoginStatus();
        }
    });
});

// Fungsi untuk memeriksa status login
function checkLoginStatus() {
    // Gunakan localStorage untuk menyimpan status login
    const isLoggedIn = localStorage.getItem('isLoggedIn');

    if (!isLoggedIn) {
        // Jika belum login, arahkan ke halaman login dengan Flask route
        window.location.href = '/login';
    } else {
        // Jika sudah login, arahkan ke halaman produk dengan Flask route
        window.location.href = '/market';
    }
}

// Simpan status login setelah pengguna berhasil login
function login() {
    localStorage.setItem('isLoggedIn', 'true');
    window.location.href = '/market';
}

// Logout
function logout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = '/';
}

// Event listener untuk tombol logout di market.html
if (window.location.pathname.includes('/market')) {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function (e) {
            e.preventDefault();
            logout();
        });
    }
}
