from django import forms
from .models import Logbook

class LogbookForm(forms.ModelForm):
    class Meta:
        model = Logbook
        fields = ['judul', 'tanggal', 'keterangan', 'detail_pekerjaan', 'tautan_pendukung', 'lampiran_gambar', 'lampiran_dokumen']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors', 'placeholder': 'Masukkan judul logbook...'}),
            'tanggal': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'text', 'readonly': 'readonly', 'class': 'w-full bg-gray-50 border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors cursor-pointer', 'placeholder': 'Pilih tanggal...'}),
            'detail_pekerjaan': forms.Textarea(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors', 'rows': 4}),
            'tautan_pendukung': forms.URLInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors', 'placeholder': 'https://...'}),
            'lampiran_gambar': forms.FileInput(attrs={'class': 'w-full bg-white border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors cursor-pointer', 'accept': '.jpg, .jpeg, .png'}),
            'lampiran_dokumen': forms.FileInput(attrs={'class': 'w-full bg-white border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors cursor-pointer', 'accept': '.pdf, .doc, .docx, .xls, .xlsx'}),
            'keterangan': forms.Select(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none focus:border-[#00BFFF] transition-colors cursor-pointer'}),
        }

    def clean_file(self, field_name):
        file = self.cleaned_data.get(field_name)
        if file:
            # Default 10MB limit as requested
            max_size = 10 * 1024 * 1024 
            
            # Try to parse limit from the advisor's instruction in keterangan_file
            if self.instance and hasattr(self.instance, 'keterangan_file') and self.instance.keterangan_file:
                import re
                match = re.search(r'(\d+)\s*(?:mb|megabytes)', self.instance.keterangan_file.lower())
                if match:
                    max_size = int(match.group(1)) * 1024 * 1024
            
            if file.size > max_size:
                limit_mb = max_size // (1024 * 1024)
                raise forms.ValidationError(f"Ukuran berkas melebihi batas maksimal {limit_mb}MB.")
        return file

    def clean_lampiran_gambar(self):
        return self.clean_file('lampiran_gambar')

    def clean_lampiran_dokumen(self):
        return self.clean_file('lampiran_dokumen')
