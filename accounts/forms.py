from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    """Form login dengan validasi captcha."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'name': 'email',
            'placeholder': 'Masukkan Email Anda',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'placeholder': 'Masukkan kata sandi',
            'required': True,
        })
    )
    captcha = CaptchaField(
        error_messages={'invalid': 'Kode captcha salah. Silakan coba lagi.'}
    )


class RegisterForm(forms.Form):
    """Form registrasi mahasiswa dengan validasi captcha."""
    nama_lengkap = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'nama_lengkap',
            'placeholder': 'Masukkan nama lengkap sesuai KTP',
            'required': True,
        })
    )
    nim = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'nim',
            'placeholder': 'Nomor Induk Mahasiswa',
            'required': True,
        })
    )
    universitas = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'universitas',
            'placeholder': 'Nama Perguruan Tinggi',
            'required': True,
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'name': 'email',
            'placeholder': 'Gunakan email aktif',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'placeholder': 'Minimal 8 karakter',
            'required': True,
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'password_confirm',
            'placeholder': 'Ulangi password',
            'required': True,
        })
    )
    captcha = CaptchaField(
        error_messages={'invalid': 'Kode captcha salah. Silakan coba lagi.'}
    )
