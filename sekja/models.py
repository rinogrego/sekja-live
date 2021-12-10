from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.forms import ModelForm, widgets


# Source for setting up: https://medium.com/@royprins/django-custom-user-model-email-authentication-d3e89d36210f
# Additional Sources:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html

class UserManager(BaseUserManager):
   use_in_migrations = True

   def _create_user(self, no_KK, password, is_staff, is_superuser, email, **extra_fields):
      #  if not email:
      #      raise ValueError('Users must have an email address')
      now = timezone.now()
      email = self.normalize_email(email)
      no_KK = str(no_KK)
      user = self.model(
         email=email,
         is_staff=is_staff, 
         is_active=True,
         is_superuser=is_superuser, 
         last_login=now,
         date_joined=now, 
         no_KK=no_KK,
         **extra_fields
      )
      user.set_password(password)
      user.save(using=self._db)
      return user

   def create_user(self, no_KK, password, **extra_fields):
      return self._create_user(no_KK, password, False, False, **extra_fields)

   def create_superuser(self, no_KK, password, **extra_fields):
      user=self._create_user(no_KK, password, True, True, **extra_fields)
      return user




class User(AbstractBaseUser, PermissionsMixin):
   no_KK = models.CharField(max_length=16, unique=True)
   email = models.EmailField(max_length=254, unique=True)
   name = models.CharField(max_length=254, null=False, blank=False)
   is_staff = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   is_active = models.BooleanField(default=True)
   last_login = models.DateTimeField(null=True, blank=True)
   date_joined = models.DateTimeField(auto_now_add=True)
   ROLES = (
     # (simpan di database, display)
     (1, 'Admin'),
     (2, 'Pengguna')
    )
   status = models.PositiveSmallIntegerField(blank=False, choices=ROLES, default=2)

   USERNAME_FIELD = 'no_KK' # The name of the field that will serve as unique identifier (which will be the email field for us --> dari source)
   EMAIL_FIELD = 'email' # The name of the field that will be returned when get_email_field_name() is called on a User instance
   # to be displayed at command line for createsuperuser
   REQUIRED_FIELDS = ['email', 'name'] # Required fields besides the password and USERNAME_FIELD when signing up.

   objects = UserManager()

   def get_absolute_url(self):
      return "/users/%i/" % (self.pk)

   def __str__(self):
      return f"{self.name}"


class Jalan(models.Model):
   nama_jalan = models.CharField(max_length=60, null=True)
   LEVEL_TIPE_JALAN = (
      ('V', 'Kelas V'),
      ('IV', 'Kelas IV'),
      ('III', 'Kelas III'),
      ('II', 'Kelas II'),
      ('I', 'Kelas I'),
   )
   tipe_jalan = models.CharField(max_length=10, choices=LEVEL_TIPE_JALAN)
   LEVEL_KONDISI_TROTOAR = (
      ('0', 'Skala 0'),
      ('1', 'Skala 1'),
      ('2', 'Skala 2'),
      ('3', 'Skala 3'),
   )
   kondisi_trotoar = models.CharField(max_length=10, choices=LEVEL_KONDISI_TROTOAR)
   LEVEL_KONDISI_PENERANGAN = (
      ('1', 'Skala 1'),
      ('2', 'Skala 2'),
      ('3', 'Skala 3'),
   )
   kondisi_penerangan = models.CharField(max_length=10, choices=LEVEL_KONDISI_PENERANGAN)
   LEVEL_KONDISI_JALAN = (
      ('1', 'Skala 1'),
      ('2', 'Skala 2'),
      ('3', 'Skala 3'),
      ('4', 'Skala 4'),
      ('5', 'Skala 5'),
   )
   kondisi_jalan = models.CharField(max_length=10, choices=LEVEL_KONDISI_JALAN)
   jalan_sekitar = models.ManyToManyField("self", related_name="berdekatan", symmetrical=True, blank=True)
   
   def __str__(self):
      return f"{self.nama_jalan}"

   def call_jalan_sekitar(self):
      jumlah_tetangga = len(self.jalan_sekitar.all())
      if jumlah_tetangga == 0:
         return "Tidak tersambung dengan jalan lain yang tersimpan dalam basis data"
      string = ""
      for i in range(jumlah_tetangga - 1):
         string += f"{self.jalan_sekitar.all()[i].nama_jalan}, "
      if jumlah_tetangga > 0:
         string += f"{self.jalan_sekitar.all()[jumlah_tetangga - 1]}"
      return string


class Laporan(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="membuat_laporan")
   jalan = models.ForeignKey(Jalan, on_delete=models.CASCADE, related_name="dilaporkan_dalam")
   judul = models.CharField(max_length=32, default="Tanpa Judul", blank=False, null=False)
   tanggal_laporan = models.DateTimeField(auto_now_add=True, null=False)
   LEVEL_STATUS = (
      ('W', 'Waiting List'),
      ('P', 'On Progress'),
      ('S', 'Selesai')
   )
   status = models.CharField(max_length=15, choices=LEVEL_STATUS, default='W', blank=False)
   pesan = models.CharField(max_length=512)
   
   def __str__(self):
      return f"{self.pesan}"


class Komentar(models.Model):
   laporan = models.ForeignKey(Laporan, on_delete=models.CASCADE, related_name="komentar")
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="berkomentar", null=True)
   tanggal = models.DateTimeField(auto_now_add=True, null=False)
   komentar = models.CharField(max_length=512, null=False)
   
   def __str__(self):
      return f"{self.komentar}"

