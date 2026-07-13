from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, MasterUniversitas, MasterJurusan
from .forms import LoginForm, RegisterForm
import json
import logging
from django.conf import settings as django_settings
from firebase_admin import auth as firebase_auth
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from firebase_admin import app_check

logger = logging.getLogger(__name__)


# ─── APP CHECK (reCAPTCHA v3) HELPER ────────────────────────────────────────

def _verify_appcheck(request):
    """
    Verifikasi Firebase App Check token dari header request.
    Returns (True, None) jika valid, (False, error_message) jika gagal.
    """
    token = request.META.get('HTTP_X_FIREBASE_APPCHECK', '')
    if not token:
        return False, 'Token keamanan reCAPTCHA tidak ditemukan.'
    try:
        app_check.verify_token(token)
        return True, None
    except Exception as e:
        logger.warning(f'App Check verification failed: {e}')
        return False, 'Verifikasi keamanan gagal. Silakan muat ulang halaman.'


# ─── FIREBASE SYNC HELPER ───────────────────────────────────────────────────

def _sync_to_firebase(user, password=None):
    """
    Sinkronisasi user Django ke Firebase Auth.
    - Jika user belum ada di Firebase → buat baru.
    - Jika sudah ada → update display name.
    - Simpan firebase_uid di database lokal.
    """
    if user.firebase_uid:
        # User sudah punya UID Firebase, update display name saja
        try:
            firebase_auth.update_user(
                user.firebase_uid,
                display_name=user.get_full_name() or user.username,
            )
        except Exception as e:
            logger.warning(f'Firebase update gagal untuk {user.email}: {e}')
        return

    # Cek apakah email sudah ada di Firebase
    try:
        fb_user = firebase_auth.get_user_by_email(user.email)
        # Sudah ada di Firebase, simpan UID-nya
        user.firebase_uid = fb_user.uid
        user.save(update_fields=['firebase_uid'])
        logger.info(f'Firebase UID linked untuk {user.email}: {fb_user.uid}')
        return
    except firebase_auth.UserNotFoundError:
        pass  # Belum ada, lanjut buat baru

    # Buat user baru di Firebase
    try:
        create_kwargs = {
            'email': user.email,
            'email_verified': True,
            'display_name': user.get_full_name() or user.username,
            'disabled': False,
        }
        if password:
            create_kwargs['password'] = password

        fb_user = firebase_auth.create_user(**create_kwargs)
        user.firebase_uid = fb_user.uid
        user.save(update_fields=['firebase_uid'])
        logger.info(f'Firebase user dibuat untuk {user.email}: {fb_user.uid}')
    except Exception as e:
        logger.error(f'Gagal membuat Firebase user untuk {user.email}: {e}')

# ─── ROOT REDIRECT ──────────────────────────────────────────────────────────

def root_split_view(request):
    """
    Pengontrol rute root ('/'):
    - User belum login  → redirect ke halaman login
    - Admin/superuser   → redirect ke admin dashboard
    - Mahasiswa          → redirect ke user dashboard
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.role == 'ADMIN' or request.user.is_superuser:
            return redirect('/admin-panel/dashboard/')
        return redirect('dashboard')
    return redirect('login_peserta')


# ─── USER VIEWS ─────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    # Halaman user dashboard — bisa diakses oleh siapapun yang login.
    # Admin yang membuka halaman ini TIDAK di-redirect agar tidak mengganggu tab lain.
    from django.utils import timezone
    from logbook.models import Tugas, Logbook
    tugas_list = Tugas.objects.filter(mahasiswa=request.user).order_by('-deadline')[:5]
    total_logbook = Logbook.objects.filter(user=request.user, status='DISETUJUI').count()
    total_logbook_menunggu = Logbook.objects.filter(user=request.user, status='MENUNGGU').count()
    total_tugas_selesai = Tugas.objects.filter(mahasiswa=request.user, status='SELESAI').count()
    total_tugas_aktif = Tugas.objects.filter(mahasiswa=request.user, status='PENDING').count()
    context = {
        'page_title': 'Dashboard',
        'tugas_list': tugas_list,
        'total_logbook': total_logbook,
        'total_logbook_menunggu': total_logbook_menunggu,
        'total_tugas_selesai': total_tugas_selesai,
        'total_tugas_aktif': total_tugas_aktif,
        'today': timezone.localdate(),
    }
    return render(request, 'user/user_dashboard.html', context)

@login_required
def profile_view(request):
    # Halaman profil — hanya untuk MAHASISWA.
    # Admin yang membuka halaman ini diarahkan ke pengaturan admin.
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        return redirect('admin_pengaturan')

    if request.method == 'POST':
        current_user = CustomUser.objects.get(pk=request.user.pk)
        nama_baru     = request.POST.get('nama', '').strip()
        nim_baru      = request.POST.get('nim', '').strip()
        univ_baru     = request.POST.get('universitas', '').strip()
        jurusan_baru  = request.POST.get('jurusan', '').strip()
        no_telp_baru  = request.POST.get('no_telp', '').strip()
        banner_color_baru = request.POST.get('banner_color', '').strip()
        tempat_lahir_baru = request.POST.get('tempat_lahir', '').strip()
        tanggal_lahir_baru = request.POST.get('tanggal_lahir', '').strip()
        jenis_kelamin_baru = request.POST.get('jenis_kelamin', '').strip()

        # Bangun update_fields secara dinamis — hanya field yang diisi
        fields_to_update = []
        if nama_baru:
            current_user.first_name = nama_baru
            fields_to_update.append('first_name')
        if nim_baru:
            current_user.nim = nim_baru
            fields_to_update.append('nim')
        if univ_baru:
            univ_obj, _ = MasterUniversitas.objects.get_or_create(nama=univ_baru)
            current_user.universitas = univ_obj
            fields_to_update.append('universitas')
        if jurusan_baru:
            jurusan_obj, _ = MasterJurusan.objects.get_or_create(nama=jurusan_baru)
            current_user.jurusan = jurusan_obj
            fields_to_update.append('jurusan')
        if no_telp_baru:
            current_user.no_telp = no_telp_baru
            fields_to_update.append('no_telp')
        if banner_color_baru:
            current_user.banner_color = banner_color_baru
            fields_to_update.append('banner_color')
        if tempat_lahir_baru:
            current_user.tempat_lahir = tempat_lahir_baru
            fields_to_update.append('tempat_lahir')
        if tanggal_lahir_baru:
            current_user.tanggal_lahir = tanggal_lahir_baru
            fields_to_update.append('tanggal_lahir')
        if jenis_kelamin_baru:
            # Map display text ke kode DB
            jk_map = {'Laki-laki': 'L', 'Perempuan': 'P', 'L': 'L', 'P': 'P'}
            current_user.jenis_kelamin = jk_map.get(jenis_kelamin_baru, jenis_kelamin_baru)
            fields_to_update.append('jenis_kelamin')

        delete_avatar = request.POST.get('delete_avatar')
        if delete_avatar == 'true':
            if current_user.avatar:
                current_user.avatar.delete(save=False)
            current_user.avatar = None
            fields_to_update.append('avatar')
        else:
            avatar = request.FILES.get('avatar')
            if avatar:
                if avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if current_user.avatar:
                        current_user.avatar.delete(save=False)
                    current_user.avatar = avatar
                    fields_to_update.append('avatar')
                else:
                    messages.error(request, 'Format foto tidak valid. Hanya menerima .jpg dan .png')

        if fields_to_update:
            current_user.save(update_fields=fields_to_update)

        old_pass     = request.POST.get('old_password')
        new_pass     = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        password_changed = False
        if old_pass or new_pass or confirm_pass:
            if not current_user.check_password(old_pass):
                messages.error(request, 'Password lama tidak sesuai!')
            elif new_pass != confirm_pass:
                messages.error(request, 'Konfirmasi password tidak cocok!')
            elif len(new_pass) < 8:
                messages.error(request, 'Password baru minimal 8 karakter.')
            else:
                from django.contrib.auth import update_session_auth_hash
                current_user.set_password(new_pass)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, 'Password berhasil diperbarui!')
                password_changed = True

        if not password_changed and not (old_pass or new_pass or confirm_pass):
            messages.success(request, 'Profil Anda berhasil diperbarui!')

        return redirect('profile')

    # GET — hitung statistik untuk ringkasan status
    from logbook.models import Logbook, Tugas
    total_logbook = Logbook.objects.filter(user=request.user, status='DISETUJUI').count()
    total_tugas_selesai = Tugas.objects.filter(mahasiswa=request.user, status='SELESAI').count()
    total_tugas = Tugas.objects.filter(mahasiswa=request.user).count()

    admin_user = CustomUser.objects.filter(role='ADMIN').first()
    if not admin_user:
        admin_user = CustomUser.objects.filter(is_superuser=True).first()
    admin_name = admin_user.get_full_name() if admin_user and admin_user.get_full_name() else 'Admin'

    context = {
        'page_title': 'Profil & Pengaturan',
        'total_logbook': total_logbook,
        'total_tugas_selesai': total_tugas_selesai,
        'total_tugas': total_tugas,
        'admin_name': admin_name,
    }
    return render(request, 'user/user_profile.html', context)

@login_required
def update_banner_color(request):
    """Endpoint untuk memperbarui warna banner secara asinkron."""
    if request.method == 'POST':
        color = request.POST.get('banner_color')
        if color:
            request.user.banner_color = color
            request.user.save(update_fields=['banner_color'])
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# ─── AUTH VIEWS ─────────────────────────────────────────────────────────────

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.decorators.cache import never_cache
from captcha.models import CaptchaStore
from django.conf import settings as django_settings
from accounts.utils import catat_log


def _generate_captcha():
    """Generate captcha key dan image URL baru."""
    key = CaptchaStore.generate_key()
    image_url = captcha_image_url(key)
    return key, image_url


@never_cache
def login_peserta_page(request):
    """
    Halaman login khusus peserta — autentikasi Django + captcha gambar + Firebase App Check.
    """
    recaptcha_key = django_settings.RECAPTCHA_V3_SITE_KEY
    firebase_config = django_settings.FIREBASE_WEB_CONFIG



    def _login_ctx(**extra):
        """Helper: buat context tanpa captcha gambar."""
        ctx = {
            'recaptcha_key': recaptcha_key,
            'firebase_config': json.dumps(firebase_config),
        }
        ctx.update(extra)
        return ctx

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email dan password wajib diisi.')
            return render(request, 'login_peserta.html', _login_ctx())

        # Verifikasi App Check (reCAPTCHA v3) — background
        appcheck_ok, appcheck_err = _verify_appcheck(request)
        if not appcheck_ok:
            logger.warning(f'App Check gagal saat login: {email} — {appcheck_err}')

        # Autentikasi Django
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Akun tidak ditemukan.')
            return render(request, 'login_peserta.html', _login_ctx())

        if not user.is_active:
            messages.error(request, 'Akun Anda dinonaktifkan. Hubungi admin.')
            return render(request, 'login_peserta.html', _login_ctx())
            
        if user.is_staff:
            messages.error(request, 'Admin tidak diizinkan masuk melalui portal peserta.')
            return render(request, 'login_peserta.html', _login_ctx())

        if user.check_password(password):
            login(request, user)
            catat_log(request.user, "Berhasil masuk ke dasbor peserta", "LOGIN")
            _sync_to_firebase(user, password=password)
            
            if request.user.wajib_ganti_sandi:
                return redirect('halaman_ubah_sandi_wajib')
                
            next_url = request.POST.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email atau password salah.')
            return render(request, 'login_peserta.html', _login_ctx())

    return render(request, 'login_peserta.html', _login_ctx(next=request.GET.get('next', '')))


@never_cache
def logout_view(request):
    """
    Log out pengguna dan alihkan ke halaman login yang sesuai dengan role terakhirnya.
    """
    from django.contrib.auth import logout
    is_admin = False
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.role == 'ADMIN' or request.user.is_superuser:
            is_admin = True
    logout(request)
    if is_admin:
        return redirect('login_admin')
    return redirect('login_peserta')


@never_cache
def login_admin_page(request):
    """
    Halaman login khusus admin — autentikasi Django + Firebase App Check.
    """
    recaptcha_key = django_settings.RECAPTCHA_V3_SITE_KEY
    firebase_config = django_settings.FIREBASE_WEB_CONFIG

    def _login_ctx(**extra):
        """Helper: buat context tanpa captcha gambar."""
        ctx = {
            'recaptcha_key': recaptcha_key,
            'firebase_config': json.dumps(firebase_config),
        }
        ctx.update(extra)
        return ctx

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email dan password wajib diisi.')
            return render(request, 'login_admin.html', _login_ctx())

        # Verifikasi App Check (reCAPTCHA v3) — background
        appcheck_ok, appcheck_err = _verify_appcheck(request)
        if not appcheck_ok:
            logger.warning(f'App Check gagal saat login admin: {email} — {appcheck_err}')

        # Autentikasi Django
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Akun tidak ditemukan.')
            return render(request, 'login_admin.html', _login_ctx())

        if not user.is_active:
            messages.error(request, 'Akun Anda dinonaktifkan. Hubungi superadmin.')
            return render(request, 'login_admin.html', _login_ctx())

        if not user.is_staff:
            messages.error(request, 'Peserta tidak diizinkan mengakses portal admin.')
            return render(request, 'login_admin.html', _login_ctx())

        if user.check_password(password):
            login(request, user)
            _sync_to_firebase(user, password=password)
            next_url = request.POST.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('/admin-panel/dashboard/')
        else:
            messages.error(request, 'Email atau password salah.')
            return render(request, 'login_admin.html', _login_ctx())

    return render(request, 'login_admin.html', _login_ctx(next=request.GET.get('next', '')))


@never_cache
def register_peserta_page(request):
    form_data = {}
    recaptcha_v3_key = django_settings.RECAPTCHA_V3_SITE_KEY
    recaptcha_v2_key = django_settings.GOOGLE_CAPTCHA_V2_SITE_KEY
    firebase_config = django_settings.FIREBASE_WEB_CONFIG

    def _register_ctx(**extra):
        ctx = {
            'form_data': form_data,
            'recaptcha_key': recaptcha_v3_key,
            'recaptcha_v2_key': recaptcha_v2_key,
            'firebase_config': json.dumps(firebase_config),
        }
        ctx.update(extra)
        return ctx

    if request.method == 'POST':
        form_data = {
            'nama_lengkap': request.POST.get('nama_lengkap', '').strip(),
            'nim':          request.POST.get('nim', '').strip(),
            'universitas':  request.POST.get('universitas', '').strip(),
            'email':        request.POST.get('email', '').strip(),
        }
        password         = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        recaptcha_response = request.POST.get('g-recaptcha-response', '')

        # Verifikasi Google reCAPTCHA v2 (Backend)
        captcha_valid = False
        if recaptcha_response:
            import urllib.request, urllib.parse
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': django_settings.GOOGLE_CAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            try:
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                captcha_valid = result.get('success', False)
            except Exception as e:
                logger.error(f'reCAPTCHA verification failed: {e}')
                captcha_valid = False

        if not captcha_valid:
            messages.error(request, 'Verifikasi reCAPTCHA gagal atau kedaluwarsa. Silakan coba lagi.')
            return render(request, 'register_peserta.html', _register_ctx())

        # Verifikasi App Check (reCAPTCHA v3) — background
        appcheck_ok, appcheck_err = _verify_appcheck(request)
        if not appcheck_ok:
            logger.warning(f'App Check gagal saat register: {form_data["email"]} — {appcheck_err}')

        if password != password_confirm:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
        elif len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
        elif CustomUser.objects.filter(email=form_data['email']).exists():
            messages.error(request, 'Email sudah terdaftar. Gunakan email lain.')
        else:
            univ_obj = None
            if form_data['universitas']:
                univ_obj, _ = MasterUniversitas.objects.get_or_create(nama=form_data['universitas'])

            user = CustomUser.objects.create_user(
                username=form_data['email'],
                email=form_data['email'],
                password=password,
                first_name=form_data['nama_lengkap'],
                nim=form_data['nim'],
                universitas=univ_obj,
                role='MAHASISWA',
            )
            catat_log(user, "Melakukan pendaftaran akun sistem", "CREATE")
            # Buat user di Firebase Auth
            _sync_to_firebase(user, password=password)
            messages.success(request, 'Akun berhasil dibuat. Silakan masuk.')
            return redirect('login_peserta')

    return render(request, 'register_peserta.html', _register_ctx())


@never_cache
def register_admin_page(request):
    form_data = {}
    recaptcha_v3_key = django_settings.RECAPTCHA_V3_SITE_KEY
    recaptcha_v2_key = django_settings.GOOGLE_CAPTCHA_V2_SITE_KEY
    firebase_config = django_settings.FIREBASE_WEB_CONFIG

    def _register_ctx(**extra):
        ctx = {
            'form_data': form_data,
            'recaptcha_key': recaptcha_v3_key,
            'recaptcha_v2_key': recaptcha_v2_key,
            'firebase_config': json.dumps(firebase_config),
        }
        ctx.update(extra)
        return ctx

    if request.method == 'POST':
        form_data = {
            'nama_lengkap': request.POST.get('nama_lengkap', '').strip(),
            'email':        request.POST.get('email', '').strip(),
        }
        password         = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        recaptcha_response = request.POST.get('g-recaptcha-response', '')

        # Verifikasi Google reCAPTCHA v2 (Backend)
        captcha_valid = False
        if recaptcha_response:
            import urllib.request, urllib.parse
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': django_settings.GOOGLE_CAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            try:
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                captcha_valid = result.get('success', False)
            except Exception as e:
                logger.error(f'reCAPTCHA verification failed: {e}')
                captcha_valid = False

        if not captcha_valid:
            messages.error(request, 'Verifikasi reCAPTCHA gagal atau kedaluwarsa. Silakan coba lagi.')
            return render(request, 'register_admin.html', _register_ctx())

        # Verifikasi App Check (reCAPTCHA v3) — background
        appcheck_ok, appcheck_err = _verify_appcheck(request)
        if not appcheck_ok:
            logger.warning(f'App Check gagal saat register admin: {form_data["email"]} — {appcheck_err}')

        if password != password_confirm:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
        elif len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
        elif CustomUser.objects.filter(email=form_data['email']).exists():
            messages.error(request, 'Email sudah terdaftar. Gunakan email lain.')
        else:
            user = CustomUser.objects.create_user(
                username=form_data['email'],
                email=form_data['email'],
                password=password,
                first_name=form_data['nama_lengkap'],
                role='ADMIN',
                is_staff=True,
                is_superuser=True,
            )
            catat_log(user, "Melakukan pendaftaran akun admin sistem", "CREATE")
            # Buat user di Firebase Auth
            _sync_to_firebase(user, password=password)
            messages.success(request, 'Akun admin berhasil dibuat. Silakan masuk.')
            return redirect('login_admin')

    return render(request, 'register_admin.html', _register_ctx())


@csrf_exempt
def sync_firebase_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            email = data.get('email')
            role = data.get('role', 'MAHASISWA')

            user, created = CustomUser.objects.get_or_create(
                firebase_uid=uid,
                defaults={'email': email, 'username': email, 'role': role}
            )

            if not created:
                user.email = email
                if 'role' in data:
                    user.role = data.get('role')
                user.save()

            login(request, user)
            return JsonResponse({'status': 'success', 'role': user.role})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# ─── FIREBASE TOKEN LOGIN ───────────────────────────────────────────────────

def api_login_peserta(request):
    """
    Endpoint: POST /accounts/api/login/peserta/
    Menerima Firebase ID Token dari frontend, memvalidasinya,
    lalu membuat session Django lokal jika user adalah peserta.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    try:
        from firebase_admin import app_check
        app_check_token = request.headers.get('X-Firebase-AppCheck')
        if not app_check_token:
            return JsonResponse({'status': 'error', 'message': 'Akses ditolak. Token keamanan hilang.'}, status=403)
        app_check.verify_token(app_check_token)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Akses ilegal. Validasi App Check gagal.'}, status=403)

    try:
        body = json.loads(request.body)
        id_token = body.get('id_token', '')

        if not id_token:
            return JsonResponse({'status': 'error', 'message': 'Token tidak ditemukan.'}, status=400)

        import firebase_admin.auth as fb_auth
        decoded_token = fb_auth.verify_id_token(id_token)
        email = decoded_token.get('email', '')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email tidak ditemukan dalam token.'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User tidak terdaftar di SIM-MPP. Silakan registrasi terlebih dahulu.'
            }, status=400)

        if user.is_staff:
            return JsonResponse({
                'status': 'error',
                'message': 'Admin tidak diizinkan masuk melalui portal peserta.'
            }, status=403)

        login(request, user)
        if request.user.wajib_ganti_sandi:
            return JsonResponse({'status': 'success', 'redirect': '/accounts/ubah-sandi-wajib/'})
        from django.urls import reverse
        return JsonResponse({'status': 'success', 'redirect': reverse('dashboard')})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Request body tidak valid.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Verifikasi gagal: {str(e)}'}, status=400)


def api_login_admin(request):
    """
    Endpoint: POST /accounts/api/login/admin/
    Menerima Firebase ID Token dari frontend, memvalidasinya,
    lalu membuat session Django lokal jika user adalah admin.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    try:
        from firebase_admin import app_check
        app_check_token = request.headers.get('X-Firebase-AppCheck')
        if not app_check_token:
            return JsonResponse({'status': 'error', 'message': 'Akses ditolak. Token keamanan hilang.'}, status=403)
        app_check.verify_token(app_check_token)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Akses ilegal. Validasi App Check gagal.'}, status=403)

    try:
        body = json.loads(request.body)
        id_token = body.get('id_token', '')

        if not id_token:
            return JsonResponse({'status': 'error', 'message': 'Token tidak ditemukan.'}, status=400)

        import firebase_admin.auth as fb_auth
        decoded_token = fb_auth.verify_id_token(id_token)
        email = decoded_token.get('email', '')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email tidak ditemukan dalam token.'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Admin tidak terdaftar.'
            }, status=400)

        if not user.is_staff:
            return JsonResponse({
                'status': 'error',
                'message': 'Peserta tidak diizinkan mengakses portal admin.'
            }, status=403)

        login(request, user)
        return JsonResponse({'status': 'success', 'redirect': '/admin-panel/dashboard/'})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Request body tidak valid.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Verifikasi gagal: {str(e)}'}, status=400)

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

@login_required
def halaman_ubah_sandi_wajib(request):
    # Jika tidak wajib ganti sandi, alihkan ke dashboard
    if not request.user.wajib_ganti_sandi:
        return redirect('dashboard')
        
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if len(password) < 8:
            messages.error(request, 'Kata sandi minimal 8 karakter.')
        elif password != confirm_password:
            messages.error(request, 'Kata sandi dan konfirmasi tidak cocok.')
        else:
            # Perbarui kata sandi di Firebase
            try:
                if request.user.firebase_uid:
                    firebase_auth.update_user(request.user.firebase_uid, password=password)
                else:
                    _sync_to_firebase(request.user, password=password)
            except Exception as e:
                logger.error(f'Gagal update password Firebase untuk {request.user.email}: {e}')
                messages.error(request, 'Terjadi kesalahan sistem saat memperbarui kredensial Firebase.')
                return render(request, 'ubah_sandi_wajib.html')
            
            # Perbarui kata sandi di MySQL lokal
            request.user.set_password(password)
            
            # Ubah status wajib_ganti_sandi
            request.user.wajib_ganti_sandi = False
            request.user.save()
            
            # Login ulang setelah ubah password agar session tidak kedaluwarsa
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Kata sandi berhasil diperbarui. Selamat datang di SIM-MPP!')
            return redirect('dashboard')
            
    return render(request, 'ubah_sandi_wajib.html')


def lupa_password_view(request):
    """
    Halaman Permintaan Lupa Password dengan Verifikasi OTP.
    Tidak memerlukan pengalihan link eksternal (sangat cocok untuk development lokal offline).
    """
    import random
    from django.utils import timezone

    # Ambil status form dari session
    step = request.session.get('reset_step', 1)
    email = request.session.get('reset_email', '')

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'kirim_email':
            email = request.POST.get('email', '').strip()
            if not email:
                messages.error(request, 'Alamat email wajib diisi.')
                return render(request, 'lupa_password.html', {'step': 1})

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Demi keamanan, tetap tampilkan seolah-olah sukses dikirim
                request.session['reset_step'] = 2
                request.session['reset_email'] = email
                # Buat dummy OTP agar session tetap valid
                request.session['reset_otp'] = "999999"
                request.session['reset_otp_expiry'] = (timezone.now() + timezone.timedelta(minutes=10)).timestamp()
                messages.success(request, 'Kode verifikasi OTP telah dikirimkan ke email Anda.')
                return render(request, 'lupa_password.html', {'step': 2, 'email': email})

            # Generate OTP 6-digit
            otp = f"{random.randint(100000, 999999)}"
            request.session['reset_step'] = 2
            request.session['reset_email'] = email
            request.session['reset_otp'] = otp
            request.session['reset_otp_expiry'] = (timezone.now() + timezone.timedelta(minutes=10)).timestamp()

            # Kirim email berisi OTP
            subject = 'Kode Verifikasi Reset Kata Sandi SIM-MPP'
            message = f"""Yth. {user.first_name or 'Pengguna'},

Anda menerima pesan ini karena adanya permintaan untuk mengatur ulang kata sandi akun Anda pada Sistem Informasi Manajemen Magang (SIM-MPP).

Kode Verifikasi (OTP) Anda adalah:
{otp}

Masukkan kode di atas pada halaman reset kata sandi di browser PC Anda untuk mengganti kata sandi. Kode ini hanya berlaku selama 10 menit.

Jika Anda merasa tidak melakukan permintaan ini, harap abaikan email ini.

Hormat kami,
Administrator SIM-MPP
Dinas Komunikasi, Informatika, Persandian dan Statistik Kabupaten Bekasi"""

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Kode verifikasi OTP telah berhasil dikirimkan ke email Anda.')
            except Exception as e:
                logger.error(f'Gagal mengirim email OTP ke {email}: {e}')
                messages.error(request, 'Terjadi kesalahan sistem saat mengirim email OTP. Silakan hubungi admin.')
                # Kembalikan ke step 1
                request.session['reset_step'] = 1
                return render(request, 'lupa_password.html', {'step': 1})

            return render(request, 'lupa_password.html', {'step': 2, 'email': email})

        elif action == 'verifikasi_otp':
            input_otp = request.POST.get('otp', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            session_otp = request.session.get('reset_otp')
            session_expiry = request.session.get('reset_otp_expiry', 0)

            # Cek masa berlaku OTP
            if timezone.now().timestamp() > session_expiry:
                messages.error(request, 'Kode OTP telah kedaluwarsa. Silakan minta kode baru.')
                request.session['reset_step'] = 1
                return render(request, 'lupa_password.html', {'step': 1})

            # Validasi OTP
            if not session_otp or input_otp != session_otp:
                messages.error(request, 'Kode OTP yang Anda masukkan salah.')
                return render(request, 'lupa_password.html', {'step': 2, 'email': email})

            # Validasi Password
            if len(password) < 8:
                messages.error(request, 'Kata sandi minimal terdiri dari 8 karakter.')
                return render(request, 'lupa_password.html', {'step': 2, 'email': email})

            if password != confirm_password:
                messages.error(request, 'Konfirmasi kata sandi tidak cocok.')
                return render(request, 'lupa_password.html', {'step': 2, 'email': email})

            # Update password
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Kasus email dummy
                messages.success(request, 'Kata sandi Anda berhasil diperbarui! Silakan masuk kembali.')
                request.session.flush()
                return redirect('login')

            # 1. Perbarui kata sandi di Firebase
            try:
                if user.firebase_uid:
                    firebase_auth.update_user(user.firebase_uid, password=password)
                else:
                    _sync_to_firebase(user, password=password)
            except Exception as e:
                logger.error(f'Gagal update password Firebase saat reset OTP untuk {user.email}: {e}')
                messages.error(request, 'Terjadi kesalahan sistem saat sinkronisasi keamanan Firebase.')
                return render(request, 'lupa_password.html', {'step': 2, 'email': email})

            # 2. Perbarui kata sandi di database MySQL lokal
            user.set_password(password)
            user.wajib_ganti_sandi = False
            user.save()

            # Berhasil! Catat aktivitas & bersihkan session
            catat_log(user, "Melakukan reset kata sandi melalui kode OTP email", "UPDATE")
            request.session.flush()
            
            messages.success(request, 'Kata sandi Anda berhasil diperbarui! Silakan masuk kembali.')
            return redirect('login')

        elif action == 'batal':
            request.session.flush()
            return redirect('login')

    return render(request, 'lupa_password.html', {'step': step, 'email': email})


def reset_password_view(request, uidb64, token):
    """
    Fallback untuk URL lama jika tersisa.
    """
    messages.error(request, 'Gunakan alur reset password berbasis OTP yang baru.')
    return redirect('lupa_password')