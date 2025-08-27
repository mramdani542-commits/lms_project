from django.contrib import admin
from .models import (
    User, ClassGroup, MataPelajaran, Enrollment, TeacherAssignment,
    Question, Exam, ExamAttempt, Answer
)
from .models import TujuanPembelajaran, PenilaianTP
from .models import User, InfoSekolah, Ekstrakurikuler, Kehadiran, Rapor, KomponenNilai, Penilaian

# Mendaftarkan setiap model agar bisa dikelola melalui admin panel
admin.site.register(User)
admin.site.register(ClassGroup)
admin.site.register(MataPelajaran)
admin.site.register(Enrollment)
admin.site.register(TeacherAssignment)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(ExamAttempt)
admin.site.register(Answer)
admin.site.register(InfoSekolah)
admin.site.register(Ekstrakurikuler)
admin.site.register(Kehadiran)
admin.site.register(TujuanPembelajaran)
admin.site.register(PenilaianTP)
admin.site.register(Rapor)
admin.site.register(KomponenNilai)
admin.site.register(Penilaian)
