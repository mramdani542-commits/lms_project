from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Avg
# -----------------------------------------------------------------------------
# Model untuk Pengguna dan Peran (Users and Roles)
# -----------------------------------------------------------------------------
def generate_token():
    """Membuat token acak 6 karakter."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(AbstractUser):
    """
    Model pengguna kustom yang menggantikan model User bawaan Django.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        GURU = 'GURU', 'Guru'
        WALIKELAS = 'WALIKELAS', 'Wali Kelas'
        SISWA = 'SISWA', 'Siswa'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.SISWA)
    
    # --- TAMBAHKAN FIELD INI ---
    # Ini adalah hubungan yang hilang antara Siswa dan Kelas.
    # related_name='students' memungkinkan kita memanggil class_instance.students.all()
    class_group = models.ForeignKey(
        'ClassGroup', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students',  # Ini adalah nama yang akan kita gunakan
        verbose_name="Kelas"
    )
    
    # ... (field Anda yang lain seperti nis, nisn, dll. tidak perlu diubah) ...
    join_date = models.DateField(null=True, blank=True, verbose_name="Tanggal Bergabung")
    employee_id = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name="Nomor Induk Pegawai")
    nis = models.CharField(max_length=20, null=True, blank=True, verbose_name="NIS")
    nisn = models.CharField(max_length=20, null=True, blank=True, verbose_name="NISN")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default.png', verbose_name="Foto Profil")
    address = models.TextField(null=True, blank=True, verbose_name="Alamat")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Nomor Telepon")
    
    class Theme(models.TextChoices):
        LIGHT = 'LIGHT', 'Light'
        DARK = 'DARK', 'Dark'
        BLUE = 'BLUE', 'Blue Ocean'
        GREEN = 'GREEN', 'Green Forest'
        PURPLE = 'PURPLE', 'Purple Night'
        NEON = 'NEON', 'Neon Cyber'
        RETRO = 'RETRO', 'Retro Terminal'
        FUTURISTIC = 'FUTURISTIC', 'Futuristic Glass'
        HIGH_CONTRAST = 'HIGH_CONTRAST', 'High Contrast'

    theme = models.CharField(max_length=20, choices=Theme.choices, default=Theme.LIGHT)

# PENTING: Definisikan MataPelajaran SEBELUM model lain yang menggunakannya (seperti Nilai)
class MataPelajaran(models.Model):
    # Field yang sudah ada
    nama = models.CharField(max_length=100, unique=True)
    
    # Field baru yang ditambahkan
    level = models.CharField(max_length=50, blank=True, null=True, verbose_name="Jenjang/Tingkat")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")

    def __str__(self):
        return self.nama
# -----------------------------------------------------------------------------
# Model untuk Entitas Akademik (Classes, MataPelajarans)
# -----------------------------------------------------------------------------

class ClassGroup(models.Model):
    """
    Model untuk merepresentasikan kelas.
    Contoh: 'Kelas 7-A', 'Kelas 10-B'.
    Kita menggunakan nama 'ClassGroup' untuk menghindari konflik dengan keyword 'class' di Python.
    """
    
    # 1. Definisikan pilihan untuk jenjang di sini
    LEVEL_CHOICES = [
        ('SD', 'Sekolah Dasar'),
        ('SMP', 'Sekolah Menengah Pertama'),
        ('SMA', 'Sekolah Menengah Atas'),
        ('SMK', 'Sekolah Menengah Kejuruan'),
        # Tambahkan jenjang lain jika perlu
    ]

    name = models.CharField(max_length=100, help_text="Contoh: 10-A, 12-C")
    
    # 2. Tambahkan 'choices' ke field 'level'
    level = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES,
        verbose_name="Jenjang/Tingkat"
    )
    
    homeroom_teacher = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'WALIKELAS'},
        related_name='homeroom_class_dari',
        verbose_name="Wali Kelas"
    )
    # Relasi Many-to-Many ke MataPelajaran tetap dipertahankan
    mata_pelajaran = models.ManyToManyField("MataPelajaran", blank=True)
    exam_room = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ruang Ujian")
    def __str__(self):
        # Menggunakan get_level_display() untuk menampilkan label yang mudah dibaca
        return f"{self.name} ({self.get_level_display()})"

class Rapor(models.Model):
    siswa = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='rapor_siswa'
    )
    mata_pelajaran = models.ForeignKey("MataPelajaran", on_delete=models.CASCADE)
    nilai_uts = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Nilai Ujian Tengah Semester")
    nilai_uas = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Nilai Ujian Akhir Semester")
    catatan_guru = models.TextField(blank=True, null=True)

    @property
    def nilai_akhir_rata_rata(self):
        # Menghitung rata-rata dari semua 'Penilaian' yang terkait dengan rapor ini.
        # Ini akan menjadi nilai akhir di rapor.
        # Mengembalikan 0 jika belum ada penilaian.
        return self.penilaian_set.aggregate(rata_rata=Avg('nilai'))['rata_rata'] or 0.0

    class Meta:
        unique_together = ('siswa', 'mata_pelajaran')

    def __str__(self):
        return f"Rapor {self.siswa.username} - {self.mata_pelajaran.nama}"

# Model 2: KomponenNilai
# Untuk mendefinisikan jenis-jenis penilaian yang bisa dibuat oleh guru.
class KomponenNilai(models.Model):
    nama_komponen = models.CharField(max_length=100, unique=True, help_text="Contoh: Tugas Harian, Ulangan Harian, Proyek")
    # Anda bisa menambahkan bobot di sini jika diperlukan, misal: bobot = models.FloatField(default=1.0)

    def __str__(self):
        return self.nama_komponen

# Model 3: Penilaian
# Menyimpan setiap entri nilai individual (misal: Tugas 1, Ulangan 2, dll.)
class Penilaian(models.Model):
    rapor = models.ForeignKey(Rapor, on_delete=models.CASCADE)
    komponen = models.ForeignKey(KomponenNilai, on_delete=models.PROTECT, help_text="Jenis penilaian (Tugas, Ulangan, dll.)")
    nama_penilaian = models.CharField(max_length=150, help_text="Contoh: Tugas 1 - Mengerjakan LKS Hal 10")
    nilai = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_penilaian} - {self.rapor.siswa.username}"

# Model untuk Ekstrakurikuler
class Ekstrakurikuler(models.Model):
    """
    Menyimpan data ekstrakurikuler yang diikuti oleh siswa.
    """
    siswa = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        # UBAH INI: dari 'ekstrakurikuler' menjadi 'ekskul_siswa'
        related_name='ekskul_siswa', 
        limit_choices_to={'role': 'SISWA'}
    )
    nama_kegiatan = models.CharField(max_length=255)
    predikat = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Ekskul {self.siswa.username} - {self.nama_kegiatan}"

# Model untuk Kehadiran
class Kehadiran(models.Model):
    """
    Menyimpan rekap data ketidakhadiran siswa per semester.
    """
    siswa = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        # PASTIKAN BAGIAN INI ADA DAN TIDAK SALAH KETIK
        related_name='kehadiran_siswa' 
    )
    sakit = models.PositiveIntegerField(default=0)
    izin = models.PositiveIntegerField(default=0)
    alpha = models.PositiveIntegerField(default=0, verbose_name="Tanpa Keterangan")

    def __str__(self):
        return f"Kehadiran {self.siswa.username}"

class Prestasi(models.Model):
    siswa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestasi', limit_choices_to={'role': 'SISWA'})
    jenis_kegiatan = models.CharField(max_length=255, verbose_name="Jenis Prestasi/Kegiatan")
    keterangan = models.TextField(verbose_name="Keterangan (Contoh: Juara 1 Tingkat Nasional)")
    def __str__(self):
        return f"Prestasi {self.siswa.username} - {self.jenis_kegiatan}"

class CatatanWaliKelas(models.Model):
    siswa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catatan_wali_kelas', limit_choices_to={'role': 'SISWA'})
    # Tambahkan semester/tahun ajaran jika ingin menyimpan riwayat catatan
    catatan = models.TextField()
    def __str__(self):
        return f"Catatan untuk {self.siswa.username}"

class TanggapanOrangTua(models.Model):
    siswa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tanggapan_orang_tua', limit_choices_to={'role': 'SISWA'})
    tanggapan = models.TextField()
    tanggal = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Tanggapan untuk {self.siswa.username}"

class KenaikanKelas(models.Model):
    STATUS_CHOICES = [
        ('NAIK', 'Naik Kelas'),
        ('TINGGAL', 'Tinggal di Kelas'),
        ('LULUS', 'Lulus'),
    ]
    siswa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kenaikan_kelas', limit_choices_to={'role': 'SISWA'})
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    keterangan = models.CharField(max_length=255, verbose_name="Naik ke/Tinggal di Kelas") # Contoh: "Naik ke Kelas XI", "Tinggal di Kelas X"
    def __str__(self):
        return f"Status Kenaikan {self.siswa.username}: {self.get_status_display()}"

# Model untuk Info Sekolah
class InfoSekolah(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.TextField()
    kepala_sekolah = models.CharField(max_length=255)
    nip_kepsek = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nama

# -----------------------------------------------------------------------------
# Model untuk Relasi (Enrollments, Assignments)
# -----------------------------------------------------------------------------

class Enrollment(models.Model):
    """
    Model penghubung (pivot) untuk mendaftarkan siswa ke dalam sebuah kelas.
    Relasi Many-to-Many antara User (Siswa) dan ClassGroup.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'SISWA'}, related_name='enrollment') # Tambahkan related_name
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        # Memastikan seorang siswa tidak bisa mendaftar di kelas yang sama lebih dari sekali.
        unique_together = ('student', 'class_group')

    def __str__(self):
        return f"{self.student.username} terdaftar di {self.class_group.name}"

class TeacherAssignment(models.Model):
    """
    Model untuk menugaskan seorang guru untuk mengajar mata pelajaran tertentu di kelas tertentu.
    """
    # Diperbaiki: Memungkinkan peran GURU dan WALIKELAS untuk ditugaskan.
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='GURU') | Q(role='WALIKELAS')
    )
    MataPelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'MataPelajaran', 'class_group')

    def __str__(self):
        return f"{self.teacher.username} mengajar {self.MataPelajaran.nama} di {self.class_group.name}"

class TeacherEvaluation(models.Model):
    # Manajer yang memberikan evaluasi
    evaluator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='given_evaluations', 
        limit_choices_to={'role': 'MANAGER'}
    )
    # Guru yang menerima evaluasi
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_evaluations', 
        limit_choices_to=Q(role='GURU') | Q(role='WALIKELAS')
    )
    content = models.TextField(verbose_name="Isi Evaluasi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Menampilkan evaluasi terbaru di paling atas

    def __str__(self):
        evaluator_name = self.evaluator.username if self.evaluator else "[deleted]"
        return f"Evaluasi untuk {self.teacher.username} oleh {evaluator_name}"

class GradingSettings(models.Model):
    summative_weight = models.PositiveIntegerField(default=60, verbose_name="Bobot Nilai Sumatif (%)")
    formative_weight = models.PositiveIntegerField(default=40, verbose_name="Bobot Nilai Formatif (%)")
# -----------------------------------------------------------------------------
# Model untuk Ujian dan Penilaian (Exams, Questions, Answers)
# -----------------------------------------------------------------------------

class Question(models.Model):
    """
    Model untuk menyimpan satu soal.
    Versi ini sudah dibersihkan dari duplikasi field.
    """
    class QuestionType(models.TextChoices):
        PILIHAN_GANDA = 'PILIHAN_GANDA', 'Pilihan Ganda'
        ISIAN_SINGKAT = 'ISIAN_SINGKAT', 'Isian Singkat'
        MENJODOHKAN = 'MENJODOHKAN', 'Menjodohkan'
        BENAR_SALAH = 'BENAR_SALAH', 'Benar/Salah'
        ESAI = 'ESAI', 'Esai'

    class DifficultyLevel(models.TextChoices):
        PRA_STRUKTURAL = 'PRA-STRUKTURAL', 'PRA-STRUKTURAL'
        UNISTRUKTURAL = 'UNISTRUKTURAL', 'UNISTRUKTURAL'
        MULTISTRUKTURAL = 'MULTISTRUKTURAL', 'MULTISTRUKTURAL'
        RELASI = 'RELASI', 'RELASI'
        ABSTRAK = 'ABSTRAK', 'ABSTRAK'

    # Relasi
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    # PERBAIKAN: Nama field menggunakan huruf kecil (snake_case)
    matapelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='questions')

    # Konten Soal
    question_text = models.TextField(verbose_name="Teks Pertanyaan")
    # PERBAIKAN: Menggunakan satu nama field yang konsisten: 'question_image'
    question_image = models.ImageField(upload_to='question_images/', blank=True, null=True, verbose_name="Gambar Soal")
    question_audio = models.FileField(upload_to='question_audio/', blank=True, null=True)
    # Properti Soal
    question_type = models.CharField(max_length=50, choices=QuestionType.choices, verbose_name="Tipe Soal")
    difficulty = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.ABSTRAK,
        verbose_name="Tingkat Kesulitan"
    )
    weight = models.PositiveIntegerField(default=10, verbose_name="Bobot Soal")
    
    # Jawaban
    options = models.JSONField(blank=True, null=True, default=dict, help_text="Hanya untuk soal pilihan ganda atau menjodohkan")
    correct_answer = models.TextField(help_text="Kunci jawaban untuk PG atau jawaban referensi untuk esai")

    def __str__(self):
        # Menggunakan versi __str__ yang bersih
        return f"Soal: {self.question_text[:50]}..."

class Exam(models.Model):
    """
    Model untuk mendefinisikan sebuah ujian.
    """
    name = models.CharField(max_length=255, verbose_name="Nama Ujian")
    MataPelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, verbose_name="Mata Pelajaran")
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, verbose_name="Kelas")
    start_time = models.DateTimeField(verbose_name="Waktu Mulai")
    end_time = models.DateTimeField(verbose_name="Waktu Selesai")
    duration_minutes = models.PositiveIntegerField(help_text="Durasi ujian dalam menit")
    tokens = models.JSONField(default=list)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_exams',
        verbose_name="Dibuat oleh"
    )
    
    
    # Relasi Many-to-Many untuk memilih soal mana saja yang ada di ujian ini.
    def save(self, *args, **kwargs):
        if not self.tokens:
            # Buat token acak jika belum ada
            self.tokens = [
                ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            for _ in range(5)
            ]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.MataPelajaran.nama} ({self.class_group.name})"
    
class Token(models.Model):
    """
    Model untuk menyimpan token unik untuk setiap ujian.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='token_set')
    token = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token} for {self.exam.name}"

    class Meta:
        # Menambahkan constraint agar kombinasi exam dan token selalu unik
        unique_together = ('exam', 'token')
        ordering = ['-created_at']


class ExamAttempt(models.Model):
    """
    Mencatat setiap percobaan pengerjaan ujian oleh seorang siswa.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'SISWA'})
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    token_used = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True, blank=True, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    current_answers = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.student.username}'s attempt on {self.exam.name}"

class Answer(models.Model):
    """
    Menyimpan jawaban yang diberikan oleh siswa untuk satu soal pada suatu percobaan ujian.
    Versi ini sudah disempurnakan.
    """
    # PERBAIKAN 1: Hanya ada SATU hubungan ke ExamAttempt
    attempt = models.ForeignKey(
        ExamAttempt, 
        on_delete=models.CASCADE, 
        related_name='answers' # 'answers' adalah nama yang umum dan mudah diingat
    )
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # PERBAIKAN 2: Memisahkan penyimpanan jawaban PG dan Essay
    # Untuk Pilihan Ganda (misal: 'A', 'B')
    selected_option = models.CharField(max_length=10, null=True, blank=True, verbose_name="Opsi Dipilih")
    # Untuk jawaban Essay atau Isian
    answer_text = models.TextField(null=True, blank=True, verbose_name="Jawaban Teks")
    
    # Untuk menyimpan hasil koreksi (otomatis atau manual)
    is_correct = models.BooleanField(null=True, blank=True)

    class Meta:
        # unique_together sudah benar, memastikan satu jawaban per soal per percobaan
        unique_together = ('attempt', 'question')

    def __str__(self):
        # Menggunakan 'attempt' karena kita sudah mengganti nama field-nya
        return f"Jawaban untuk soal {self.question.id} di percobaan {self.attempt.id}"
    
class Competency(models.Model):
    """
    Model untuk menyimpan Capaian Kompetensi atau Tujuan Pembelajaran (TP).
    """
    class CalculationMethod(models.TextChoices):
        WEIGHTED_AVERAGE = 'BOBOT', 'Bobot'
        AVERAGE = 'RATA_RATA', 'Rata-Rata'
        MODE = 'MODUS', 'Modus'
        HIGHEST = 'NILAI_TERTINGGI', 'Nilai Tertinggi'

    matapelajaran = models.ForeignKey('MataPelajaran', on_delete=models.CASCADE, related_name='competencies')
    code = models.CharField(max_length=20, verbose_name="Kode Capaian Kompetensi")
    description = models.TextField(verbose_name="Deskripsi Capaian Kompetensi")
    calculation_method = models.CharField(
        max_length=20, 
        choices=CalculationMethod.choices, 
        default=CalculationMethod.WEIGHTED_AVERAGE,
        verbose_name="Tipe Penilaian"
    )
    
    class Meta:
        verbose_name_plural = "Daftar Capaian Kompetensi"
        unique_together = ('matapelajaran', 'code')

    def __str__(self):
        return f"{self.matapelajaran.nama} - {self.code}"

class AssessmentComponent(models.Model):
    """
    Model untuk komponen penilaian di dalam sebuah kompetensi (misal: Formatif, Sumatif).
    """
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=100, verbose_name="Nama Komponen (cth: Formatif, Sumatif)")
    description = models.TextField(verbose_name="Deskripsi Komponen", blank=True)
    weight = models.PositiveIntegerField(
        default=100, 
        verbose_name="Bobot (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.competency.code} - {self.name} ({self.weight}%)"

class Score(models.Model):
    """
    Model untuk menyimpan nilai setiap siswa untuk setiap KOMPONEN PENILAIAN.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')
    # PERUBAHAN PENTING: Nilai sekarang terikat ke AssessmentComponent
    assessment_component = models.ForeignKey(AssessmentComponent, on_delete=models.CASCADE, related_name='scores')
    value = models.PositiveIntegerField(default=0, verbose_name="Nilai")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Daftar Nilai Siswa"
        unique_together = ('student', 'assessment_component')

    def __str__(self):
        return f"Nilai {self.student.username} - {self.assessment_component.name}: {self.value}"

class TujuanPembelajaran(models.Model):
    # ... field mata_pelajaran tidak berubah ...
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='tujuan_pembelajaran')

    # === TAMBAHKAN FIELD INI ===
    level = models.CharField(
        max_length=50,
        choices=ClassGroup.LEVEL_CHOICES, # Mengambil pilihan dari model ClassGroup
        verbose_name="Jenjang/Tingkat",
        default="SMA"
    )
    kelas = models.CharField(
        max_length=20,
        verbose_name="Tingkat Kelas",
        help_text="Contoh: 10 A, 11 IPA, 12 IPS"
    )
    deskripsi = models.TextField(verbose_name="Deskripsi Tujuan Pembelajaran")
    semester = models.IntegerField()

    def __str__(self):
        # Tampilkan jenjang agar lebih jelas di admin
        return f"{self.get_level_display()} - ({self.kelas}) - {self.mata_pelajaran.nama} - {self.deskripsi[:30]}..."

class PenilaianTP(models.Model):
    """
    Menyimpan nilai setiap siswa untuk setiap TP.
    Ini adalah sumber data utama untuk rapor.
    """
    siswa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='penilaian_tp')
    tp = models.ForeignKey(TujuanPembelajaran, on_delete=models.CASCADE, related_name='penilaian')
    nilai = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('siswa', 'tp') # Siswa hanya punya satu nilai per TP

    def __str__(self):
        return f"Nilai {self.siswa.username} - TP: {self.tp.id}"