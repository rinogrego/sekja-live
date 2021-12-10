from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User, Jalan, Laporan, Komentar
from .forms import LaporanForm, KomentarForm

# Create your views here.


def login_view(request):
  if request.method == "POST":

      # Attempt to sign user in
      no_KK = request.POST["no_KK"]
      status = request.POST["status"]
      status = int(status)
      password = request.POST["password"]
      user = authenticate(request, no_KK=no_KK, password=password)

      # Check if authentication successful
      if user is not None:
         # Check login status
         if status != user.status:
            return render(request, "sekja/login.html", {
               "message": f"Maaf, login sesuai dengan status anda! (Admin/Pengguna)"
            })
         login(request, user)
         return HttpResponseRedirect(reverse("index"))
      else:
         return render(request, "sekja/login.html", {
              "message": "Nomor KK atau Password Salah."
         })
  else:
      return render(request, "sekja/login.html")


def logout_view(request):
   logout(request)
   return HttpResponseRedirect(reverse("index"))


def register(request):
   if request.method == "POST":
      no_KK = request.POST["no_KK"]
      name = request.POST["name"]
      email = request.POST["email"]

      # Ensure password matches confirmation
      password = request.POST["password"]
      confirmation = request.POST["confirmation"]
      if password != confirmation:
            return render(request, "sekja/register.html", {
               "message": "Passwords must match."
            })

      # Attempt to create new user
      try:
         user = User.objects.create_user(no_KK=no_KK, name=name, email=email, password=password, status=2)
         user.save()
      except IntegrityError:
         return render(request, "sekja/register.html", {
            "message": "Nomor KK or email already taken."
         })
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
   else:
      if request.user.is_authenticated:
         logout(request)
      return render(request, "sekja/register.html")


def index(request):
   try:
      return render(request, "sekja/index.html", {
         "user_status": "Admin" if request.user.status == 1 else "Pengguna"
      })
   except:
      return render(request, "sekja/index.html")


def papan_laporan(request):
   if request.method == "POST":
      form = LaporanForm(request.POST)
      if form.is_valid():
         user = request.user
         jalan = form.cleaned_data["jalan"]
         judul = form.cleaned_data["judul"]
         pesan = form.cleaned_data["pesan"]
         a = Laporan(user=user, jalan=jalan, judul=judul, pesan=pesan)
         a.save()
   try:
      Reports = Laporan.objects.order_by('-tanggal_laporan').all()
      return render(request, "sekja/laporan_papan.html", {
         "user_status": "Admin" if request.user.status == 1 else "Pengguna",
         "Laporan": Reports,
      })
   except:
      return render(request, "sekja/laporan_papan.html", {
         "Laporan": Reports,
      })


@login_required(login_url='login')
def laporan(request, laporan_id):
   if request.method == "POST":
      form = KomentarForm(request.POST)
      if form.is_valid():
         laporan = Laporan.objects.get(id=laporan_id)
         author = request.user
         komentar = form.cleaned_data["komentar"]
         a = Komentar(laporan=laporan, author=author, komentar=komentar)
         a.save()
   laporan = Laporan.objects.get(id=laporan_id)
   komentar = laporan.komentar.all()
   form = KomentarForm()
   return render(request, "sekja/laporan.html", {
      "laporan": laporan,
      "Komentar": komentar,
      "form": form,
      "user_status": "Admin" if request.user.status == 1 else "Pengguna",
   })


@login_required(login_url='login')
def buat_laporan(request):
   if request.user.status == 1:
      return HttpResponse("Maaf, Admin tidak diperbolehkan membuat laporan secara langsung.")
   if not request.user.is_authenticated:
      return render(request, "sekja/login.html", {
         "message": "Maaf, sebelum membuat laporan, mohon Login terlebih dahulu sebagai Pengguna."
      })
   form = LaporanForm()
   return render(request, "sekja/laporan_buat.html", {
      "form": form
   })


@login_required(login_url='login')
def jalan(request):
   jalan = Jalan.objects.all()
   try:
      return render(request, "sekja/jalan.html", {
         "user_status": "Admin" if request.user.status == 1 else "Pengguna",
         "Jalan": jalan
      })
   except:
      return render(request, "sekja/jalan.html", {
         "Jalan": jalan,
      })
