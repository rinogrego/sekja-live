from django import forms
from django.db.models import query
from .models import User, Jalan, Laporan, Komentar



class LaporanForm(forms.Form):
   jalan = forms.ModelChoiceField(queryset=Jalan.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Jalan'}))
   judul = forms.CharField(max_length=32, label="Judul", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul'}))
   # LEVEL_STATUS = (
   #    ('W', 'Waiting List'),
   #    ('P', 'On Progress'),
   #    ('S', 'Selesai')
   # )
   # status = forms.CharField(max_length=15, widget=forms.Select(choices=LEVEL_STATUS))
   pesan = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pesan'}))


class KomentarForm(forms.Form): 
   # author = forms.ModelChoiceField(queryset=User.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Author'}))
   komentar = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'class': 'form-control mt-2', 'style': 'height: 8rem;', 'placeholder': 'Komentar'}), label='')


class EditJalan(forms.Form): pass