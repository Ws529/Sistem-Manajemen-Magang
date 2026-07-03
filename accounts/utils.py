from .models import LogAktivitas

def catat_log(aktor, aktivitas, tipe):
    """
    Fungsi untuk mencatat aktivitas ke database.
    Jika ini adalah event sistem otomatis, parameter aktor dapat diisi None.
    """
    LogAktivitas.objects.create(
        aktor=aktor,
        aktivitas=aktivitas,
        tipe=tipe
    )
