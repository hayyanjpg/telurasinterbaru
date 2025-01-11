# Import Flask, SQLAlchemy, dan dependensi lainnya
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi Aplikasi dan Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_register.db'  # Lokasi file database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Menonaktifkan fitur tracking
app.secret_key = 'supersecretkey'  # Kunci rahasia untuk sesi dan flash messages

# Inisialisasi objek database
db = SQLAlchemy(app)

# Model Database: Menyimpan informasi pengguna
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID unik untuk pengguna
    username = db.Column(db.String(100), unique=True, nullable=False)  # Username pengguna
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email pengguna
    password = db.Column(db.String(150), nullable=False)  # Kata sandi pengguna

# Membuat tabel database jika belum ada
with app.app_context():
    db.create_all()

# Halaman Home
@app.route("/")
def home():
    return render_template("index.html")

# Halaman Registrasi Pengguna
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validasi data
        if len(username) < 6:
            flash("Username harus minimal 6 karakter.", "danger")
            return redirect(url_for("register"))
        if len(password) < 8:
            flash("Password harus minimal 8 karakter.", "danger")
            return redirect(url_for("register"))

        # Periksa apakah username atau email sudah terdaftar
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username atau email sudah terdaftar.", "danger")
            return redirect(url_for("register"))

        # Hash password sebelum disimpan
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registrasi berhasil! Silakan login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Halaman Login Pengguna
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Cari pengguna berdasarkan username
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id  # Simpan ID pengguna di sesi
            session["username"] = user.username  # Simpan username di sesi
            flash(f"Login berhasil. Selamat datang, {user.username}!", "success")
            return redirect(url_for("market"))  # Arahkan ke halaman market
        else:
            flash("Username atau password salah.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Halaman Market (Setelah Login)
@app.route("/market")
def market():
    if "user_id" not in session:
        flash("Silakan login terlebih dahulu.", "danger")
        return redirect(url_for("login"))
    return render_template("market.html", username=session["username"])  # Kirim username ke template

# Halaman Logout
@app.route("/logout")
def logout():
    session.clear()  # Hapus semua data sesi
    flash("Anda telah logout.", "success")
    return redirect(url_for("home"))

# Menjalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
