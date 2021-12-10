from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("papan-laporan", views.papan_laporan, name="papan_laporan"),
  path("laporan/<int:laporan_id>", views.laporan, name="laporan"),
  path("laporan/buat", views.buat_laporan, name="buat_laporan"),
  path("jalan", views.jalan, name="jalan"),
]