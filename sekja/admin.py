from django.contrib import admin
from .models import User, Laporan, Komentar, Jalan
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# class UserAdmin(BaseUserAdmin):
#    fieldsets = (
#       (None, {'fields': ('no_KK', 'email', 'password', 'name', 'last_login')}),
#       ('Permissions', {'fields': (
#             'is_active', 
#             'is_staff', 
#             'is_superuser',
#             'groups', 
#             'user_permissions',
#       )}),
#    )
#    add_fieldsets = (
#       (
#             None,
#             {
#                'classes': ('wide',),
#                'fields': ('no_KK', 'email', 'password1', 'password2')
#             }
#       ),
#    )

#    list_display = ('no_KK', 'email', 'name', 'is_staff', 'last_login')
#    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#    search_fields = ('no_KK', 'email',)
#    ordering = ('no_KK', 'email',)
#    filter_horizontal = ('groups', 'user_permissions',)



class UserAdmin(admin.ModelAdmin):
   list_display = ("id", "name", "status", "email", "no_KK")

class JalanAdmin(admin.ModelAdmin):
   filter_horizontal = ("jalan_sekitar", )
   list_display = ("id", "nama_jalan", "tipe_jalan", "kondisi_jalan", "kondisi_trotoar", "kondisi_penerangan")

class LaporanAdmin(admin.ModelAdmin):
   list_display = ("id", "user", "jalan", "tanggal_laporan", "status", "pesan")

class KomentarAdmin(admin.ModelAdmin):
   list_display = ("id", "laporan", "author", "tanggal", "komentar")

admin.site.register(User, UserAdmin)
admin.site.register(Laporan, LaporanAdmin)
admin.site.register(Komentar, KomentarAdmin)
admin.site.register(Jalan, JalanAdmin)