from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Sertifikat

@login_required
def daftar_dokumen(request):
    sertifikat = None
    try:
        sertifikat = Sertifikat.objects.get(user=request.user)
    except Sertifikat.DoesNotExist:
        pass

    context = {
        'page_title': 'Dokumen Sertifikat',
        'sertifikat': sertifikat,
    }
    return render(request, 'user/user_dokumen.html', context)

@login_required
def support_view(request):
    faq_list = [
        {'pertanyaan': 'Bagaimana cara mengisi logbook?', 'jawaban': 'Klik menu Entri Logbook di sidebar, kemudian klik tombol "Tambah Entri" dan isi formulir yang tersedia.'},
        {'pertanyaan': 'Kapan logbook perlu diisi?', 'jawaban': 'Logbook harus diisi setiap hari kerja selama masa magang berlangsung.'},
        {'pertanyaan': 'Bagaimana cara mengunggah dokumen?', 'jawaban': 'Pergi ke menu Dokumen, klik tombol "Unggah Dokumen", pilih file, kemudian klik Simpan.'},
        {'pertanyaan': 'Apa yang dimaksud status "Menunggu"?', 'jawaban': 'Status "Menunggu" berarti data yang kamu submit sedang dalam proses review oleh pembimbing lapangan.'},
    ]
    context = {
        'page_title': 'Bantuan & Support',
        'faq_list': faq_list,
    }
    return render(request, 'user/user_support.html', context)
