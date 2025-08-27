from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import redirect_view 
from .views import (
    redirect_view,
    rapor_print_view,
    lampiran_print_view,
)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as main_views
from . import views as student_views
from . import views as teacher_views
from .views import redirect_view
from .views import theme_settings


urlpatterns = [
    # URL yang sudah ada
    path('users/', views.user_management_view, name='user_management'),
    path('users/<int:pk>/edit/', views.user_update_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
    path('classes/', views.class_management_view, name='class_management'),

    # URL BARU UNTUK EDIT DAN HAPUS KELAS
    path('classes/<int:pk>/edit/', views.class_update_view, name='class_edit'),
    path('classes/<int:pk>/delete/', views.class_delete_view, name='class_delete'),

    # URL BARU UNTUK IMPOR/EKSPOR KELAS
    path('classes/export/', views.class_export_template, name='class_export_template'),
    path('classes/import/', views.class_import_view, name='class_import'),
    
    # URL BARU UNTUK EKSPOR DAN IMPOR PENGGUNA
    path('users/export/', views.export_users_to_excel, name='user_export'),
    path('users/import/', views.import_users_from_excel, name='user_import'),

     # ... (URL untuk users dan classes) ...
    path('MataPelajarans/', views.MataPelajaran_management_view, name='MataPelajaran_management'),
    # Tambahkan baris ini
    path('assignments/export-template/', views.export_assignments_template_view, name='export_assignments_template'),
    # Tambahkan baris ini
    path('assignments/import/', views.import_assignments_view, name='import_assignments'),

    # URL BARU UNTUK EDIT DAN HAPUS MAPEL
    path('MataPelajarans/<int:pk>/edit/', views.MataPelajaran_update_view, name='MataPelajaran_edit'),
    path('MataPelajarans/<int:pk>/delete/', views.MataPelajaran_delete_view, name='MataPelajaran_delete'),

    # == URL UNTUK MANAJEMEN KELAS & SISWA ==

    # Halaman utama manajemen kelas (Anda mungkin sudah punya ini)
    path('classes/', views.class_management_view, name='class_management'),

    # Halaman utama untuk mengelola siswa di dalam kelas spesifik
    # Pastikan 'enroll_students_view' adalah nama fungsi view utama Anda untuk halaman ini
    path('class/<int:pk>/enroll/', views.enroll_students_view, name='enroll_students'),

    # URL untuk mendaftarkan siswa yang sudah ada (dari form manual)
    # Ini bisa ditangani oleh view yang sama dengan di atas (enroll_students_view)
    # karena form-nya ada di halaman yang sama.

    # URL untuk mengeluarkan siswa dari kelas
    path('class/<int:class_pk>/unenroll/<int:student_pk>/', views.unenroll_student_view, name='unenroll_student'),

    # URL untuk mengekspor daftar siswa dari kelas
    path('class/<int:class_pk>/export_students/', views.export_class_students, name='export_class_students'),

    # URL BARU YANG PERLU ANDA TAMBAHKAN UNTUK MEMPERBAIKI ERROR
    path('class/<int:class_pk>/import_new_students/', views.import_new_students_to_class, name='import_new_students_to_class'),
    
    # URL untuk mengunduh template siswa baru (jika Anda membuatnya)
    # Ini mengarah ke view 'user_export' yang mungkin sudah ada di manajemen pengguna
    path('users/export/', views.user_export, name='user_export'),
    
        # URL BARU UNTUK MANAJEMEN SOAL
    path('questions/', views.question_management_view, name='question_management'),
    path('questions/<int:pk>/edit/', views.question_update_view, name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete_view, name='question_delete'),
    # =========================================================
    # URL UNTUK GURU / ADMIN (menggunakan main_views)
    # =========================================================
    path('exams/', main_views.exam_management_view, name='exam_management'),
    path('exam/<int:pk>/detail/', main_views.exam_detail_view, name='exam_detail'),
    path('exams/<int:pk>/preview/', views.exam_preview_view, name='exam_preview'),
    # =========================================================
    # URL UNTUK SISWA (menggunakan student_views)
    # =========================================================
    # PERBAIKAN DI SINI: Arahkan ke student_views
    path('exam/<int:pk>/start/', student_views.exam_start_view, name='exam_start'),
    path('exam/<int:pk>/gate/', student_views.exam_token_gate_view, name='exam_token_gate'),
    path('exam/<int:pk>/take/', student_views.take_exam_view, name='take_exam'),
    path('exam/<int:pk>/submit/', student_views.exam_submit_view, name='exam_submit'),
    path('exam/<int:exam_pk>/resume/', views.resume_exam_with_token, name='resume_exam_with_token'),
    path('exam/attempt/<int:attempt_pk>/save/', student_views.save_exam_progress, name='save_exam_progress'),

     # URL untuk form membuat soal baru UNTUK UJIAN SPESIFIK
    path('exam/<int:exam_pk>/questions/create/', views.question_create_view, name='question_create'),
    path('exam/<int:exam_pk>/questions/import/word/', views.import_questions_from_word, name='question_import_word'),

    # URL BARU UNTUK EKSPOR DAN IMPOR SOAL
    path('questions/export_word/', views.export_questions_word_template, name='question_export_word'),
    path('exam/<int:exam_pk>/questions/import/word/', views.import_questions_from_word, name='question_import_word'),
    path('questions/export/word-template/', views.export_questions_word_template, name='question_export_word_template'),

    # URL BARU UNTUK MANAJEMEN UJIAN
    path('exams/', views.exam_management_view, name='exam_management'),
    path('exams/<int:pk>/', views.exam_detail_view, name='exam_detail'),
    path('exams/<int:pk>/edit/', views.exam_update_view, name='exam_edit'),
    path('exams/<int:pk>/delete/', views.exam_delete_view, name='exam_delete'),

    # URL BARU UNTUK PROFIL GURU
    path('teacher/<int:pk>/profile/', views.teacher_profile_view, name='teacher_profile'),

     # URL BARU UNTUK PENDAFTARAN SISWA
    path('class/<int:pk>/enroll/', views.enroll_students_view, name='class_enroll'),
     # URL BARU UNTUK PROFIL
    path('profile/', views.profile_view, name='profile'),
    # URL BARU UNTUK GURU MELIHAT EVALUASI
    path('evaluations/', views.view_evaluations_view, name='view_evaluations'),
    # URL BARU UNTUK IMPOR SISWA BARU
    path('users/export_new_student_template/', views.export_new_student_template, name='export_new_student_template'),
    path('users/import_new_students/', views.import_new_students_view, name='import_new_students'),
   # URL untuk mengunduh template siswa baru
    path('students/export-template/', views.export_new_student_template, name='export_new_student_template'),

    # URL untuk memproses unggahan file siswa baru ke kelas spesifik
    path('class/<int:class_pk>/import_new_students/', views.import_new_students_to_class, name='import_new_students_to_class'),
    # URL BARU UNTUK DAFTAR KOREKSI
    path('corrections/', views.correction_list_view, name='correction_list'),
    path('exam/<int:exam_pk>/analysis/', views.item_analysis_view, name='item_analysis'),

    # DENGAN YANG BENAR (SESUAIKAN NAMA VIEW UTAMA ANDA):
    path('class/<int:pk>/enroll/', views.enroll_students_view, name='enroll_students'), 
        # ... URL Anda yang lain
    path('classes/<int:pk>/edit/', views.edit_class_view, name='class_edit'),
    # ... URL Anda yang lain

    path('settings/grading/', views.grading_settings_view, name='grading_settings'),
# ... URL Anda yang lain
    path('MataPelajarans/<int:MataPelajaran_pk>/competencies/', views.competency_settings_view, name='competency_settings'),
     # ... URL Anda yang lain
    path('grades/input/class/<int:class_pk>/MataPelajaran/<int:MataPelajaran_pk>/', views.grade_input_view, name='grade_input'),
    # TAMBAHKAN PATH BARU INI UNTUK MEMPERBAIKI ERROR 404
    path('MataPelajarans/<int:MataPelajaran_pk>/competencies/', views.competency_settings_view, name='competency_settings'),

    path('dashboard/admin/', TemplateView.as_view(template_name="dashboard/dashboard_admin.html"), name="dashboard_admin"),
    path('dashboard/guru/', TemplateView.as_view(template_name="dashboard/dashboard_guru.html"), name="dashboard_guru"),
    path('dashboard/siswa/', TemplateView.as_view(template_name="dashboard/dashboard_siswa.html"), name="dashboard_siswa"),
    path('dashboard/manager/', TemplateView.as_view(template_name="dashboard/dashboard_manager.html"), name="dashboard_manager"),
    path('dashboard/redirect/', redirect_view, name="redirect_view"),
    path("redirect/", views.redirect_view, name="role_redirect"),
    path('raport/print/', views.rapor_print_view, name='rapor_print'),
    path('lampiran/print/', views.lampiran_print_view, name='lampiran_print'),
    path('dashboard/rapor/<int:siswa_id>/', views.rapor_print_view, name='rapor_print'),

    
    # URL untuk fitur rapor yang kita buat
    path('dashboard/lampiran/print/', views.lampiran_print_view, name='lampiran_print'), # Jika Anda punya view ini

    # === INI BAGIAN PENTING ===
    # URL untuk API yang akan dipanggil oleh JavaScript
    path('api/dashboard/raport-data/', views.raport_data_api, name='raport_data_api'),
    path('api/dashboard/raport-update/', views.update_rapor_api, name='update_rapor_api'),

    # TAMBAHKAN URL BARU INI UNTUK IMPOR SOAL PER MAPEL
    path('MataPelajaran/<int:MataPelajaran_pk>/questions/import/', views.import_questions_for_MataPelajaran_view, name='question_import_for_MataPelajaran'),
    # TAMBAHKAN URL BARU INI UNTUK HALAMAN ANALISIS
    # =========================================================
    path('exam/<int:exam_pk>/analysis/', teacher_views.item_analysis_view, name='item_analysis'),
    path('exam/<int:exam_pk>/analysis/export/', views.export_item_analysis_excel, name='export_item_analysis'),
    path('correction/<int:attempt_pk>/', views.correction_detail_view, name='correction_detail'),
    path('answer/<int:answer_pk>/ai-suggestion/', views.get_ai_correction_suggestion_view, name='get_ai_suggestion'),

    # Di dalam dashboard/urls.py
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    # --- URL UNTUK HALAMAN GABUNGAN ---
    path('MataPelajarans/', views.MataPelajaran_management_view, name='MataPelajaran_management'),

    # --- URL UNTUK FITUR MATA PELAJARAN ---
    # (Ini yang sudah Anda miliki dan sudah benar)
    path('MataPelajarans/export-template/', views.export_MataPelajarans_template_view, name='export_MataPelajarans_template'),
    path('MataPelajarans/import/', views.import_MataPelajarans_view, name='import_MataPelajarans'),

    # --- URL UNTUK FITUR PENUGASAN GURU ---
    # (Ini yang perlu Anda tambahkan)
    path('assignments/export-template/', views.export_assignments_template_view, name='export_assignments_template'),
    path('assignments/import/', views.import_assignments_view, name='import_assignments'),

    path('theme-settings/', theme_settings, name='theme_settings'),
    path('manajemen-nilai/', views.manajemen_nilai_view, name='manajemen_nilai'),
    # PASTIKAN BARIS-BARIS INI ADA
    path('manajemen-komponen/', views.komponen_nilai_list, name='komponen_nilai_list'),
    path('manajemen-komponen/hapus/<int:pk>/', views.komponen_nilai_delete, name='komponen_nilai_delete'),

    path('api/kelas/<int:kelas_id>/siswa/', views.api_get_siswa, name='api_get_siswa'),
    path('api/rapor/siswa/<int:siswa_id>/mapel/<int:mapel_id>/', views.api_get_rapor_data, name='api_get_rapor_data'),

    # URL API BARU UNTUK MENYIMPAN DATA
    path('api/penilaian/tambah/', views.api_tambah_penilaian, name='api_tambah_penilaian'),
    path('api/rapor/<int:rapor_id>/simpan/', views.api_simpan_semua_perubahan, name='api_simpan_semua_perubahan'),
    # URL BARU UNTUK IMPOR/EKSPOR
    path('export/nilai/kelas/<int:kelas_id>/mapel/<int:mapel_id>/', views.export_nilai_kelas, name='export_nilai_kelas'),
    path('import/nilai/kelas/<int:kelas_id>/mapel/<int:mapel_id>/', views.import_nilai_kelas, name='import_nilai_kelas'),
     # ... URL Anda yang lain
    path('grade-report/', views.grade_report_view, name='grade_report'),
    # URL BARU UNTUK MELIHAT DAFTAR SISWA DI SEBUAH KELAS
    path('class/<int:class_id>/students/', views.class_student_list_view, name='class_student_list'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    