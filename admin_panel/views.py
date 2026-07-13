from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
import csv
import logging
from functools import wraps
from accounts.models import CustomUser, MasterUniversitas, MasterJurusan
from logbook.models import Logbook, Tugas
from portfolio.models import Portfolio
from documents.models import Sertifikat
from accounts.utils import catat_log
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from firebase_admin import auth as firebase_auth
import string
import random

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser)

def admin_required(view_func):
    """
    Decorator khusus admin:
    - Jika belum login  → redirect ke halaman login
    - Jika sudah login tapi bukan admin → return 403 (TIDAK redirect ke login
      agar tidak menghapus sesi user di tab lain di browser yang sama)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not is_admin(request.user):
            return HttpResponseForbidden(
                '<h1>403 – Akses Ditolak</h1>'
                '<p>Halaman ini hanya untuk admin. '
                '<a href="/">Kembali ke Dashboard</a></p>'
            )
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    from logbook.models import Logbook, Tugas
    recent_logbooks = Logbook.objects.all().select_related('user').order_by('-created_at')[:10]
    total_mahasiswa = CustomUser.objects.filter(role='MAHASISWA').count()
    antrian_validasi = Logbook.objects.filter(status='MENUNGGU').count()
    tugas_tertunda = Tugas.objects.filter(status='PENDING').count()
    context = {
        'recent_logbooks': recent_logbooks,
        'total_mahasiswa': total_mahasiswa,
        'antrian_validasi': antrian_validasi,
        'tugas_tertunda': tugas_tertunda,
    }
    return render(request, 'admin/admin_dashboard.html', context)

@admin_required
def admin_data_mahasiswa(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            nama = request.POST.get('nama')
            nim = request.POST.get('nim')
            univ_name = request.POST.get('universitas', '').strip()
            email = request.POST.get('email')
            no_telp = request.POST.get('no_telp')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar.')
            else:
                karakter = string.ascii_letters + string.digits
                sandi_sementara = ''.join(random.choices(karakter, k=8))

                univ_obj = None
                if univ_name:
                    univ_obj, _ = MasterUniversitas.objects.get_or_create(nama=univ_name)

                user = CustomUser.objects.create_user(
                    username=email, email=email, password=sandi_sementara,
                    first_name=nama, role='MAHASISWA', is_mahasiswa=True,
                    nim=nim, universitas=univ_obj, no_telp=no_telp
                )
                
                catat_log(request.user, f"Menambahkan data mahasiswa baru: {nama}", "CREATE")
                
                judul_email = 'Pemberitahuan Aktivasi Akun Magang Diskominfosantik'

                pesan_email = f"""Yth. {nama},

Data pendaftaran magang Anda telah berhasil diverifikasi dan dimasukkan ke dalam sistem SIM-MPP oleh Administrator Diskominfosantik Kabupaten Bekasi.

PERHATIAN KEAMANAN: Untuk melindungi integritas data peserta, akun Anda saat ini berada dalam status terkunci. Anda harus melakukan aktivasi mandiri dengan membuat kata sandi pribadi sebelum dapat mengakses dasbor utama.

AKTIVASI AKUN ANDA
Silakan buka portal masuk melalui komputer instansi dan gunakan kredensial berikut:
Email: {email}
Kata Sandi Sementara: {sandi_sementara}

Langkah Aktivasi:

Buka halaman masuk SIM-MPP pada peramban web instansi.

Masukkan email dan kata sandi sementara di atas.

Sistem akan otomatis meminta Anda membuat kata sandi baru.

Masukkan dan konfirmasi kata sandi baru Anda.

Simpan kata sandi baru Anda di tempat yang aman.

Akun Anda akan aktif dan siap digunakan.

Jika Anda tidak mendaftar dalam program magang ini atau ada pertanyaan, hubungi Administrator SIM-MPP.

Email Pemberitahuan Otomatis
Pesan ini dibuat dan dikirim secara otomatis oleh Sistem Informasi Manajemen Magang (SIM-MPP).
Jangan membalas email ini. Hubungi Administrator untuk bantuan teknis.
Dinas Komunikasi dan Informatika Kabupaten Bekasi | 2026"""

                try:
                    send_mail(
                        subject=judul_email,
                        message=pesan_email,
                        from_email=None,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.warning(request, f'Mahasiswa berhasil ditambahkan, namun gagal mengirim email: {str(e)}')
                else:
                    messages.success(request, f'Mahasiswa berhasil ditambahkan dan email aktivasi telah dikirim ke {email}.')
        elif action == 'edit':
            user_id = request.POST.get('user_id')
            nama = request.POST.get('nama', '').strip()
            nim = request.POST.get('nim', '').strip()
            univ_name = request.POST.get('universitas', '').strip()
            email = request.POST.get('email', '').strip()
            no_telp = request.POST.get('no_telp', '').strip()

            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Peserta tidak ditemukan.')
                return redirect('admin_data_mahasiswa')

            if not nama or not email:
                messages.error(request, 'Nama dan Email wajib diisi.')
                return redirect('admin_data_mahasiswa')

            email_diubah = False
            old_email = user.email
            if email != user.email:
                if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
                    messages.error(request, 'Email baru sudah digunakan oleh pengguna lain.')
                    return redirect('admin_data_mahasiswa')

                if user.firebase_uid:
                    try:
                        firebase_auth.update_user(user.firebase_uid, email=email)
                        logger.info(f'Firebase email updated for user {user.firebase_uid} from {old_email} to {email}')
                    except Exception as e:
                        logger.error(f'Gagal memperbarui email di Firebase untuk UID {user.firebase_uid}: {e}')
                        messages.warning(request, f'Peringatan: Gagal memperbarui email di Firebase: {str(e)}')
                else:
                    try:
                        fb_user = firebase_auth.get_user_by_email(email)
                        user.firebase_uid = fb_user.uid
                    except firebase_auth.UserNotFoundError:
                        try:
                            fb_user_old = firebase_auth.get_user_by_email(old_email)
                            firebase_auth.update_user(fb_user_old.uid, email=email)
                            user.firebase_uid = fb_user_old.uid
                        except Exception as ex:
                            logger.warning(f'Could not sync firebase user on email edit for {old_email}: {ex}')

                user.email = email
                user.username = email
                email_diubah = True

            user.first_name = nama
            user.nim = nim
            user.no_telp = no_telp

            if univ_name:
                univ_obj, _ = MasterUniversitas.objects.get_or_create(nama=univ_name)
                user.universitas = univ_obj
            else:
                user.universitas = None

            user.save()
            
            if email_diubah:
                try:
                    judul_email = "Pembaruan Email Akun SIM Magang Portofolio"
                    pesan_email = (
                        f"Halo {user.first_name},\n\n"
                        f"Email login untuk akun SIM Magang Portofolio Anda telah diubah oleh Admin.\n\n"
                        f"Detail Akun Baru:\n"
                        f"- Nama: {user.first_name}\n"
                        f"- Email Baru: {email}\n\n"
                        f"Mulai saat ini, silakan gunakan email baru tersebut untuk login. Kata sandi (password) Anda tetap sama.\n\n"
                        f"Salam,\nTim Admin"
                    )
                    send_mail(
                        subject=judul_email,
                        message=pesan_email,
                        from_email=None,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    
                    pesan_email_lama = (
                        f"Halo {user.first_name},\n\n"
                        f"Kami menginformasikan bahwa email login akun Anda telah diubah oleh Admin dari {old_email} menjadi {email}.\n\n"
                        f"Jika Anda tidak merasa mengajukan perubahan ini, harap hubungi Admin segera.\n\n"
                        f"Salam,\nTim Admin"
                    )
                    send_mail(
                        subject=judul_email,
                        message=pesan_email_lama,
                        from_email=None,
                        recipient_list=[old_email],
                        fail_silently=True,
                    )
                    messages.success(request, f'Data peserta berhasil diperbarui dan notifikasi email telah dikirim ke {email}.')
                except Exception as e:
                    logger.error(f"Gagal mengirim email notifikasi perubahan email: {e}")
                    messages.warning(request, f'Data peserta diperbarui, namun gagal mengirim notifikasi email: {str(e)}')
            else:
                messages.success(request, 'Data peserta berhasil diperbarui.')

            catat_log(request.user, f"Memperbarui data mahasiswa: {nama} ({email})", "UPDATE")
            return redirect('admin_data_mahasiswa')
        elif action == 'delete':
            user_id = request.POST.get('user_id')
            try:
                user_to_delete = CustomUser.objects.get(id=user_id)
                email_to_delete = user_to_delete.email

                # Coba hapus dari Firebase terlebih dahulu
                try:
                    fb_user = firebase_auth.get_user_by_email(email_to_delete)
                    firebase_auth.delete_user(fb_user.uid)
                except firebase_auth.UserNotFoundError:
                    # Abaikan jika user tidak ada di Firebase, lanjutkan hapus di lokal
                    pass

                # Jika berhasil di Firebase, hapus di database MySQL lokal
                user_to_delete.delete()
                messages.success(request, 'Mahasiswa berhasil dihapus dari sistem.')

            except Exception as e:
                # Tangkap jika ada error koneksi Firebase atau error lainnya
                messages.error(request, f'Gagal menghapus data peserta: {str(e)}')
        return redirect('admin_data_mahasiswa')

    query = request.GET.get('q', '')
    mahasiswa_list = CustomUser.objects.filter(role='MAHASISWA')
    if query:
        mahasiswa_list = mahasiswa_list.filter(first_name__icontains=query) | mahasiswa_list.filter(nim__icontains=query)

    context = {
        'mahasiswa_list': mahasiswa_list,
        'query': query,
    }
    return render(request, 'admin/admin_data_mahasiswa.html', context)

@admin_required
def admin_catatan_sistem(request):
    from accounts.models import LogAktivitas
    qs = LogAktivitas.objects.select_related('aktor').all()

    # Filter berdasarkan tipe (GET param)
    tipe_filter = request.GET.getlist('tipe')
    if tipe_filter:
        query_types = list(tipe_filter)
        if 'SYSTEM' in query_types:
            query_types.append('LOGIN')
        qs = qs.filter(tipe__in=query_types)

    # Urutan
    urutan = request.GET.get('urutan', 'terbaru')
    if urutan == 'lama':
        qs = qs.order_by('waktu')
    else:
        qs = qs.order_by('-waktu')

    context = {
        'catatan_list': qs,
        'tipe_filter': tipe_filter,
        'urutan': urutan,
    }
    return render(request, 'admin/admin_catatan_sistem.html', context)

@admin_required
def admin_laporan(request):
    mahasiswa_list = CustomUser.objects.filter(role='MAHASISWA').order_by('first_name')
    data = []
    for idx, m in enumerate(mahasiswa_list, 1):
        logbook_disetujui = Logbook.objects.filter(user=m, status='DISETUJUI').count()
        logbook_menunggu  = Logbook.objects.filter(user=m, status='MENUNGGU').count()
        tugas_total   = Tugas.objects.filter(mahasiswa=m).count()
        tugas_selesai = Tugas.objects.filter(mahasiswa=m, status='SELESAI').count()
        persen = int((tugas_selesai / tugas_total * 100)) if tugas_total > 0 else 0
        if persen >= 75:
            performa = 'Baik'
        elif persen >= 40:
            performa = 'Cukup'
        else:
            performa = 'Kurang'
        data.append({
            'no': idx,
            'nama': m.first_name,
            'nim': m.nim or '-',
            'logbook_disetujui': logbook_disetujui,
            'logbook_menunggu': logbook_menunggu,
            'persen_tugas': persen,
            'performa': performa,
        })
    return render(request, 'admin/admin_laporan.html', {'data': data})

@admin_required
def export_laporan_excel(request):
    """Export laporan progres peserta magang sebagai CSV (kompatibel Excel)."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="laporan_progres_peserta.csv"'
    response.write('\ufeff')  # BOM agar Excel baca UTF-8 dengan benar

    writer = csv.writer(response)
    writer.writerow(['No', 'Nama', 'NIM', 'Logbook Disetujui', 'Logbook Menunggu', 'Penyelesaian Tugas', 'Performa'])

    mahasiswa_list = CustomUser.objects.filter(role='MAHASISWA').order_by('first_name')
    for idx, m in enumerate(mahasiswa_list, 1):
        logbook_disetujui = Logbook.objects.filter(user=m, status='DISETUJUI').count()
        logbook_menunggu  = Logbook.objects.filter(user=m, status='MENUNGGU').count()
        tugas_total   = Tugas.objects.filter(mahasiswa=m).count()
        tugas_selesai = Tugas.objects.filter(mahasiswa=m, status='SELESAI').count()
        persen = int((tugas_selesai / tugas_total * 100)) if tugas_total > 0 else 0
        if persen >= 75:
            performa = 'Baik'
        elif persen >= 40:
            performa = 'Cukup'
        else:
            performa = 'Kurang'
        writer.writerow([idx, m.first_name, m.nim or '-', logbook_disetujui, logbook_menunggu, f'{persen}%', performa])

    return response


@admin_required
def export_portfolio_excel(request):
    """Export portofolio proyek peserta magang sebagai CSV (kompatibel Excel)."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="portofolio_proyek_peserta.csv"'
    response.write('\ufeff')  # BOM agar Excel baca UTF-8 dengan benar

    writer = csv.writer(response)
    writer.writerow([
        'No', 'Nama Peserta', 'Universitas', 'NIM', 'Judul Proyek', 
        'Kategori', 'Teknologi', 'Tautan Repository', 'Tanggal Dibuat', 'Deskripsi'
    ])

    portfolio_list = Portfolio.objects.select_related('user').all().order_by('-created_at')

    for idx, p in enumerate(portfolio_list, 1):
        writer.writerow([
            idx,
            p.user.get_full_name() or p.user.username,
            p.user.universitas or '-',
            p.user.nim or '-',
            p.judul_proyek,
            p.kategori or '-',
            p.teknologi or '-',
            p.tautan_repository or '-',
            p.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            p.deskripsi
        ])

    return response


@admin_required
def admin_logbook(request):
    if request.method == 'POST':
        logbook_id = request.POST.get('logbook_id')
        status = request.POST.get('status')
        catatan = request.POST.get('catatan')
        keterangan_file = request.POST.get('keterangan_file', '')
        file_pembimbing = request.FILES.get('file_pembimbing')
        
        if logbook_id:
            try:
                logbook = Logbook.objects.get(id=logbook_id)
                logbook.status = status
                logbook.catatan_pembimbing = catatan
                logbook.keterangan_file = keterangan_file
                
                if file_pembimbing:
                    if file_pembimbing.size > 10 * 1024 * 1024:
                        messages.error(request, 'Gagal unggah: Ukuran file melebihi batas maksimal 10MB.')
                        referer = request.META.get('HTTP_REFERER')
                        return redirect(referer if referer else 'admin_logbook')
                    logbook.file_pembimbing = file_pembimbing
                
                logbook.save()
                if status == 'DISETUJUI':
                    catat_log(request.user, f"Menyetujui Logbook mahasiswa ID {logbook.user.nim}", "UPDATE")
                messages.success(request, 'Feedback logbook berhasil disimpan.')
            except Logbook.DoesNotExist:
                messages.error(request, 'Logbook tidak ditemukan.')
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer if referer else 'admin_logbook')

    query = request.GET.get('q', '')
    filter_status = request.GET.get('status', 'SEMUA')
    
    logbooks = Logbook.objects.all().order_by('-tanggal')
    if query:
        logbooks = logbooks.filter(user__first_name__icontains=query) | logbooks.filter(judul__icontains=query)
    
    if filter_status != 'SEMUA':
        logbooks = logbooks.filter(status=filter_status)
        
    context = {
        'logbooks': logbooks,
        'query': query,
        'filter_status': filter_status,
    }
    return render(request, 'admin/admin_logbook.html', context)

@admin_required
def admin_portofolio(request):
    if request.method == 'POST':
        portfolio_id = request.POST.get('portfolio_id')
        if portfolio_id:
            try:
                p = Portfolio.objects.get(pk=portfolio_id)
                p.delete()
                messages.success(request, 'Data portofolio berhasil dihapus.')
            except Portfolio.DoesNotExist:
                messages.error(request, 'Data tidak ditemukan.')
        return redirect('admin_portofolio')

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'desc')
    
    order_prefix = '' if sort_by == 'asc' else '-'
    
    portofolios = Portfolio.objects.all().order_by(f'{order_prefix}created_at')
    if query:
        portofolios = portofolios.filter(judul_proyek__icontains=query) | \
                      Portfolio.objects.filter(user__first_name__icontains=query)
        portofolios = portofolios.order_by(f'{order_prefix}created_at')
        
    context = {
        'portofolios': portofolios,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'admin/admin_portofolio.html', context)

@admin_required
def admin_penugasan(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            mahasiswa_id = request.POST.get('mahasiswa_id')
            judul_tugas = request.POST.get('judul_tugas')
            deskripsi_tugas = request.POST.get('deskripsi_tugas')
            deadline = request.POST.get('deadline')
            
            mahasiswa = CustomUser.objects.get(id=mahasiswa_id)
            Tugas.objects.create(
                mahasiswa=mahasiswa,
                judul_tugas=judul_tugas,
                deskripsi_tugas=deskripsi_tugas,
                deadline=deadline,
                pembimbing=request.user.first_name,
                status='PENDING'
            )
            messages.success(request, 'Tugas berhasil diberikan.')
        elif action == 'delete':
            tugas_id = request.POST.get('tugas_id')
            Tugas.objects.filter(id=tugas_id).delete()
            messages.success(request, 'Tugas berhasil dihapus.')
        return redirect('admin_penugasan')
        
    from django.utils import timezone
    tugas_list = Tugas.objects.all().order_by('-deadline')
    mahasiswa_list = CustomUser.objects.filter(role='MAHASISWA')
    
    context = {
        'tugas_list': tugas_list,
        'mahasiswa_list': mahasiswa_list,
        'today': timezone.localdate(),
    }
    return render(request, 'admin/admin_penugasan.html', context)

@admin_required
def admin_sertifikat(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            mahasiswa_id = request.POST.get('mahasiswa_id')
            nomor_sertifikat = request.POST.get('nomor_sertifikat')
            file_sertifikat = request.FILES.get('file_sertifikat')
            
            try:
                mahasiswa = CustomUser.objects.get(id=mahasiswa_id)
                # Check if already has sertifikat
                if hasattr(mahasiswa, 'sertifikat'):
                    sertifikat = mahasiswa.sertifikat
                    sertifikat.nomor_sertifikat = nomor_sertifikat
                    if file_sertifikat:
                        sertifikat.file_sertifikat = file_sertifikat
                    sertifikat.save()
                    messages.success(request, 'Sertifikat berhasil diperbarui.')
                else:
                    Sertifikat.objects.create(
                        user=mahasiswa,
                        nomor_sertifikat=nomor_sertifikat,
                        file_sertifikat=file_sertifikat,
                        is_verified=True
                    )
                    messages.success(request, 'Sertifikat berhasil diunggah.')
            except Exception as e:
                messages.error(request, f'Gagal mengunggah sertifikat: {str(e)}')
        elif action == 'delete':
            sertifikat_id = request.POST.get('sertifikat_id')
            Sertifikat.objects.filter(id=sertifikat_id).delete()
            messages.success(request, 'Sertifikat berhasil dihapus.')
        return redirect('admin_sertifikat')

    sertifikat_list = Sertifikat.objects.all().order_by('-tanggal_terbit')
    mahasiswa_list = CustomUser.objects.filter(role='MAHASISWA')
    
    context = {
        'sertifikat_list': sertifikat_list,
        'mahasiswa_list': mahasiswa_list,
    }
    return render(request, 'admin/admin_sertifikat.html', context)

@admin_required
def export_mahasiswa_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_mahasiswa.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nama', 'NIM', 'Universitas', 'Email', 'No. Telp'])
    
    mahasiswa = CustomUser.objects.filter(role='MAHASISWA')
    for m in mahasiswa:
        writer.writerow([m.first_name, m.nim, m.universitas, m.email, m.no_telp])
        
    return response

@admin_required
def admin_pengaturan(request):
    if request.method == 'POST':
        # Update HANYA field milik admin yang sedang login via PK spesifik
        admin_user   = CustomUser.objects.get(pk=request.user.pk)
        nama_baru    = request.POST.get('nama', '').strip()
        nip_baru     = request.POST.get('nip', '').strip()
        unit_baru    = request.POST.get('unit_kerja', '').strip()
        jabatan_baru = request.POST.get('jabatan', '').strip()
        no_telp_baru = request.POST.get('no_telp', '').strip()
        email_baru   = request.POST.get('email', '').strip()
        banner_color_baru = request.POST.get('banner_color', '').strip()

        # Bangun update_fields secara dinamis — hanya field yang diisi
        fields_to_update = []
        if nama_baru:
            admin_user.first_name = nama_baru
            fields_to_update.append('first_name')
        if nip_baru:
            admin_user.nip = nip_baru
            fields_to_update.append('nip')
        if unit_baru:
            admin_user.unit_kerja = unit_baru
            fields_to_update.append('unit_kerja')
        if jabatan_baru:
            admin_user.jabatan = jabatan_baru
            fields_to_update.append('jabatan')
        if no_telp_baru:
            admin_user.no_telp = no_telp_baru
            fields_to_update.append('no_telp')
        if banner_color_baru:
            admin_user.banner_color = banner_color_baru
            fields_to_update.append('banner_color')

        # Email update & Firebase sync
        if email_baru and email_baru != admin_user.email:
            if CustomUser.objects.filter(email=email_baru).exclude(pk=admin_user.pk).exists():
                messages.error(request, 'Email baru sudah digunakan oleh pengguna lain.')
                return redirect('admin_pengaturan')
            
            if admin_user.firebase_uid:
                try:
                    firebase_auth.update_user(admin_user.firebase_uid, email=email_baru)
                    logger.info(f'Firebase email updated for admin {admin_user.firebase_uid} to {email_baru}')
                except Exception as e:
                    logger.error(f'Gagal memperbarui email admin di Firebase: {e}')
                    messages.warning(request, f'Peringatan: Gagal memperbarui email di Firebase: {str(e)}')
            
            admin_user.email = email_baru
            admin_user.username = email_baru
            fields_to_update.extend(['email', 'username'])

        delete_avatar = request.POST.get('delete_avatar')
        if delete_avatar == 'true':
            if admin_user.avatar:
                admin_user.avatar.delete(save=False)
            admin_user.avatar = None
            fields_to_update.append('avatar')
        else:
            avatar = request.FILES.get('avatar')
            if avatar:
                if avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if admin_user.avatar:
                        admin_user.avatar.delete(save=False)
                    admin_user.avatar = avatar
                    fields_to_update.append('avatar')
                else:
                    messages.error(request, 'Format foto tidak valid. Hanya menerima .jpg dan .png')

        if fields_to_update:
            admin_user.save(update_fields=fields_to_update)

        old_pass     = request.POST.get('old_password')
        new_pass     = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        password_changed = False
        if old_pass or new_pass or confirm_pass:
            if not admin_user.check_password(old_pass):
                messages.error(request, 'Password lama tidak sesuai!')
            elif new_pass != confirm_pass:
                messages.error(request, 'Konfirmasi password tidak cocok!')
            elif len(new_pass) < 8:
                messages.error(request, 'Password baru minimal 8 karakter.')
            else:
                from django.contrib.auth import update_session_auth_hash
                admin_user.set_password(new_pass)
                admin_user.save()
                update_session_auth_hash(request, admin_user)
                messages.success(request, 'Password berhasil diperbarui!')
                password_changed = True

        if not password_changed and not (old_pass or new_pass or confirm_pass):
            messages.success(request, 'Profil berhasil diperbarui!')

        return redirect('admin_pengaturan')

    return render(request, 'admin/admin_pengaturan.html')
