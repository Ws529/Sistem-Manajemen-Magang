import os
import sys
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Menghubungkan ke IP eksternal (tanpa kirim data) untuk mendeteksi interface Wi-Fi/LAN yang aktif
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def main():
    local_ip = get_local_ip()
    
    # Cetak banner informasi akses jaringan lokal yang bersih di terminal
    print("\n" + "=" * 65)
    print("           SISTEM INFORMASI MANAJEMEN MAGANG (SIM-MPP)")
    print("                 DEVELOPMENT SERVER JARINGAN LOKAL")
    print("=" * 65)
    print(f" [PC] Akses dari Komputer ini :  http://127.0.0.1:8000/")
    print(f" [HP] Akses dari HP (Wi-Fi)   :  http://{local_ip}:8000/")
    print("-" * 65)
    print(" PENTING:")
    print(" Hubungkan Laptop dan Handphone Anda ke Wi-Fi yang SAMA.")
    print(" Cukup buka URL [HP] di atas pada browser Handphone Anda.")
    print("=" * 65 + "\n")
    
    # Konfigurasi Django dan jalankan server secara otomatis di 0.0.0.0:8000
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Gagal memuat Django. Pastikan virtual environment Anda aktif."
        ) from exc
    
    # Jalankan perintah runserver
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()
