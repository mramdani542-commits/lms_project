# lms_project/urls.py

from django.contrib import admin
from django.urls import path, include # Pastikan 'include' diimpor
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views

urlpatterns = [
    # Path '' akan menjalankan fungsi 'halaman_utama' dari views
    path('', views.halaman_utama, name='home'), # <--- TAMBAHKAN BARIS INI
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')), # Arahkan URL ke aplikasi dashboard

    # --- TAMBAHKAN URL BARU UNTUK AUTENTIKASI DI SINI ---
    path('accounts/login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URL untuk Halaman Utama
    # Ini akan menjadi halaman default saat membuka http://127.0.0.1:8000/
    path('', dashboard_views.home_view, name='home'),
    path('', include('dashboard.urls')),
]
# --- TAMBAHKAN BLOK KODE INI DI BAGIAN BAWAH ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Baris ini khusus untuk file yang diunggah pengguna (jika ada nanti)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Tambahkan baris ini di bawah blok 'if settings.DEBUG'
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # TAMBAHKAN BARIS INI
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

