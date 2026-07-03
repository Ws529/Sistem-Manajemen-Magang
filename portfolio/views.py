from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .models import Portfolio, MasterKategori
from accounts.utils import catat_log


@login_required
def daftar_portfolio(request):
    if request.method == 'POST':
        action = request.POST.get('action', 'add')

        if action == 'delete':
            portfolio_id = request.POST.get('portfolio_id')
            Portfolio.objects.filter(id=portfolio_id, user=request.user).delete()
            messages.success(request, 'Proyek berhasil dihapus.')
            return redirect('daftar_portfolio')

        elif action == 'edit':
            portfolio_id = request.POST.get('portfolio_id')
            judul = request.POST.get('judul', '').strip()
            deskripsi = request.POST.get('deskripsi', '').strip()
            teknologi = request.POST.get('teknologi', '').strip()
            database = request.POST.get('database', '').strip()
            kategori_name = request.POST.get('kategori', '').strip()
            link = request.POST.get('link', '').strip()
            gambar = request.FILES.get('gambar_sampul')
            if gambar and gambar.size > 5 * 1024 * 1024:
                messages.error(request, 'Ukuran gambar cover maksimal 5MB.')
                return redirect('daftar_portfolio')

            portfolio = Portfolio.objects.filter(id=portfolio_id, user=request.user).first()
            if portfolio:
                if judul and deskripsi and teknologi and kategori_name:
                    slug = slugify(kategori_name)
                    kategori_obj = MasterKategori.objects.filter(nama__iexact=kategori_name).first()
                    if not kategori_obj:
                        kategori_obj = MasterKategori.objects.filter(slug=slug).first()
                    if not kategori_obj:
                        kategori_obj = MasterKategori.objects.create(nama=kategori_name, slug=slug)

                    portfolio.judul_proyek = judul
                    portfolio.deskripsi = deskripsi
                    portfolio.teknologi = teknologi
                    portfolio.database = database
                    portfolio.kategori = kategori_obj
                    portfolio.tautan_repository = link or None
                    if gambar:
                        portfolio.gambar_sampul = gambar
                    portfolio.save()
                    catat_log(request.user, f"Memperbarui portofolio proyek '{judul}'", "UPDATE")
                    messages.success(request, 'Proyek berhasil diperbarui.')
                else:
                    messages.error(request, 'Judul, deskripsi, teknologi, dan kategori wajib diisi.')
            else:
                messages.error(request, 'Proyek tidak ditemukan.')
            return redirect('daftar_portfolio')

        # Default: tambah proyek baru
        judul = request.POST.get('judul', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()
        teknologi = request.POST.get('teknologi', '').strip()
        database = request.POST.get('database', '').strip()
        kategori_name = request.POST.get('kategori', '').strip()
        link = request.POST.get('link', '').strip()
        gambar = request.FILES.get('gambar_sampul')
        if gambar and gambar.size > 5 * 1024 * 1024:
            messages.error(request, 'Ukuran gambar cover maksimal 5MB.')
            return redirect('daftar_portfolio')

        if judul and deskripsi and teknologi and kategori_name:
            slug = slugify(kategori_name)
            kategori_obj = MasterKategori.objects.filter(nama__iexact=kategori_name).first()
            if not kategori_obj:
                kategori_obj = MasterKategori.objects.filter(slug=slug).first()
            if not kategori_obj:
                kategori_obj = MasterKategori.objects.create(nama=kategori_name, slug=slug)

            Portfolio.objects.create(
                user=request.user,
                judul_proyek=judul,
                deskripsi=deskripsi,
                teknologi=teknologi,
                database=database,
                kategori=kategori_obj,
                tautan_repository=link or None,
                gambar_sampul=gambar,
            )
            catat_log(request.user, "Mengunggah portofolio proyek baru", "CREATE")
            messages.success(request, 'Proyek berhasil ditambahkan.')
        else:
            messages.error(request, 'Judul, deskripsi, teknologi, dan kategori wajib diisi.')
        return redirect('daftar_portfolio')

    query = request.GET.get('q', '')
    portfolio_qs = Portfolio.objects.filter(user=request.user)
    if query:
        portfolio_qs = portfolio_qs.filter(
            Q(judul_proyek__icontains=query) |
            Q(deskripsi__icontains=query) |
            Q(teknologi__icontains=query)
        )
    portfolio_qs = portfolio_qs.order_by('-created_at')

    context = {
        'page_title': 'Portofolio Proyek',
        'portfolio_list': portfolio_qs,
        'total': portfolio_qs.count(),
        'query': query,
    }
    return render(request, 'user/user_portfolio.html', context)