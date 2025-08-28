from django import forms
from .models import User, ClassGroup  # pastikan ClassGroup sudah diimpor
from django.contrib.auth.forms import UserChangeForm
from .models import MataPelajaran # Tambahkan MataPelajaran ke impor
from .models import Exam, Question, MataPelajaran 
from .models import TeacherEvaluation # Tambahkan TeacherEvaluation ke impor
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import (
    User, ClassGroup, MataPelajaran, Question, Exam, 
    TeacherEvaluation, TeacherAssignment
)
from .models import GradingSettings
from .models import Competency
from .models import MataPelajaran
from .models import KomponenNilai

# ---------------- FORM USER ------------------
class UserCreationForm(forms.ModelForm):
    """
    Formulir untuk membuat pengguna baru.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
        'placeholder': 'Masukkan kata sandi'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'role': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'password': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# ---------------- FORM KELAS ------------------
class ClassGroupForm(forms.ModelForm):
    """
    ModelForm untuk membuat dan mengedit data ClassGroup.
    """
    class Meta:
        model = ClassGroup
        fields = ['name', 'level', 'homeroom_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'level': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'homeroom_teacher': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
        }
        labels = {
            'name': 'Nama Kelas',
            'level': 'Jenjang/Tingkat',
            'homeroom_teacher': 'Wali Kelas',
        }

    def __init__(self, *args, **kwargs):
        """
        Kustomisasi form saat diinisialisasi.
        """
        super(ClassGroupForm, self).__init__(*args, **kwargs)
        
        # Filter dropdown 'homeroom_teacher' agar hanya menampilkan
        # user dengan role 'WALIKELAS' atau 'GURU'.
        self.fields['homeroom_teacher'].queryset = User.objects.filter(
            role__in=[User.Role.WALIKELAS, User.Role.GURU]
        ).order_by('first_name', 'last_name')
        
        # Mengubah cara nama guru ditampilkan di dropdown agar lebih informatif
        self.fields['homeroom_teacher'].label_from_instance = lambda obj: f"{obj.get_full_name() or obj.username} ({obj.username})"
        
        # Menambahkan opsi kosong di awal dropdown wali kelas
        self.fields['homeroom_teacher'].empty_label = "-- Pilih Wali Kelas --"
# ---------------- FORM EDIT PENGGUNA (UPDATE) ------------------class UserUpdateForm(UserChangeForm):
class UserUpdateForm(UserChangeForm):
    """
    Formulir untuk mengedit data pengguna yang sudah ada.
    """
    password = None # Menghapus field password dari form edit

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'password': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
            'role': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm'}),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture']

class QuestionForm(forms.ModelForm):
    """
    Formulir untuk membuat dan mengedit soal.
    Disesuaikan dengan model Question yang sudah diperbaiki.
    """
    class Meta:
        model = Question
        # PERBAIKAN: Menggunakan nama field yang sudah distandarkan
        fields = ['question_text','matapelajaran', 'question_image','question_audio', 'question_type', 'difficulty', 'weight', 'options', 'correct_answer']
        
        widgets = {
            # PERBAIKAN: Menggunakan nama field huruf kecil
            'matapelajaran': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'question_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'id': 'id_question_type'}),
            'difficulty': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'question_text': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 4}),
            'question_image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
            'options': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'rows': 4,
                'placeholder': 'Hanya untuk Pilihan Ganda. Format JSON:\n{"A": "Teks Jawaban A",\n"B": "Teks Jawaban B"}'
            }),
            'correct_answer': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Contoh: A (untuk PG) atau teks jawaban esai'}),
        }
        
        help_texts = {
            'options': 'Masukkan pilihan dalam format JSON. Contoh: {"A": "Opsi A", "B": "Opsi B"}',
            'correct_answer': 'Untuk Pilihan Ganda, isi dengan kuncinya (misal: A). Untuk Esai, isi dengan jawaban referensi.'
        }

class ExamForm(forms.ModelForm):
    """
    Formulir untuk membuat dan mengedit detail dasar ujian.
    """
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Exam
        fields = ['name', 'MataPelajaran', 'class_group', 'start_time', 'end_time', 'duration_minutes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'token': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Kosongkan untuk token otomatis'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        
        # BARIS KUNCI 1: Paksa field 'MataPelajaran' untuk memuat dari model MataPelajaran
        # dan urutkan berdasarkan field 'nama'
        self.fields['MataPelajaran'].queryset = MataPelajaran.objects.all().order_by('nama')
        self.fields['MataPelajaran'].label = "Mata Pelajaran"
        self.fields['MataPelajaran'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})

        # BARIS KUNCI 2: Pastikan class_group juga diurutkan dengan benar
        self.fields['class_group'].queryset = ClassGroup.objects.all().order_by('name')
        self.fields['class_group'].label = "Kelas"
        self.fields['class_group'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})

class AddQuestionsToExamForm(forms.Form):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=""
    )

    def __init__(self, *args, **kwargs):
        MataPelajaran = kwargs.pop('MataPelajaran', None)
        exam = kwargs.pop('exam', None) # <-- Pastikan ada baris ini
        super().__init__(*args, **kwargs)
        
        if MataPelajaran and exam:
            # Filter: Ambil semua soal dari mapel yang sama,
            # KECUALI yang sudah ada di ujian ini.
            self.fields['questions'].queryset = Question.objects.filter(
                MataPelajaran=MataPelajaran
            ).exclude(
                pk__in=exam.questions.all().values_list('pk', flat=True)
            )

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = TeacherEvaluation
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500', 
                'rows': 4,
                'placeholder': 'Tuliskan umpan balik atau evaluasi kinerja di sini...'
            }),
        }
        labels = {
            'content': 'Tulis Evaluasi Baru'
        }
class EvaluationForm(forms.ModelForm):
    class Meta:
        model = TeacherEvaluation
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500', 
                'rows': 4,
                'placeholder': 'Tuliskan umpan balik atau evaluasi kinerja di sini...'
            }),
        }
        labels = {
            'content': 'Tulis Evaluasi Baru'
        }
class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ambil instance pengguna dari form
        user = self.instance
        # Jika peran pengguna BUKAN siswa, hapus field nisn dari form
        if user and user.role != 'SISWA':
            if 'nisn' in self.fields:
                del self.fields['nisn']
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'nisn', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'nisn': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Password saat ini'})
        self.fields['new_password1'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Password baru'})
        self.fields['new_password2'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Konfirmasi password baru'})

class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'employee_id', 'join_date', 'address', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'employee_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'join_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class ClassForm(forms.ModelForm):
    """
    Formulir untuk membuat dan mengedit data Kelas,
    memastikan field 'level' menggunakan pilihan yang benar.
    """
    class Meta:
        model = ClassGroup
        fields = ['name', 'level', 'homeroom_teacher']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Contoh: Kelas 10-A, Kelas 12-C'
            }),
            # Menggunakan Select widget agar pilihan jenjang muncul sebagai dropdown
            'level': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500'
             }),
            'homeroom_teacher': forms.Select(attrs={
                 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500'
            })
        }
        labels = {
            'name': 'Nama Kelas',
            'level': 'Jenjang/Tingkat',
            'homeroom_teacher': 'Wali Kelas',
        }

class GradingSettingsForm(forms.ModelForm):
    """
    Formulir untuk mengedit bobot nilai sumatif dan formatif.
    """
    class Meta:
        model = GradingSettings
        fields = ['summative_weight', 'formative_weight']
        widgets = {
            'summative_weight': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500',
                'min': '0',
                'max': '100',
            }),
            'formative_weight': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500',
                'min': '0',
                'max': '100',
            }),
        }
        labels = {
            'summative_weight': 'Bobot Nilai Sumatif (%)',
            'formative_weight': 'Bobot Nilai Formatif (%)',
        }

    def clean(self):
        """
        Validasi kustom untuk memastikan total bobot adalah 100%.
        """
        cleaned_data = super().clean()
        summative = cleaned_data.get("summative_weight")
        formative = cleaned_data.get("formative_weight")

        if summative is not None and formative is not None:
            if summative + formative != 100:
                raise forms.ValidationError("Total bobot nilai Sumatif dan Formatif harus 100%.")
        
        return cleaned_data
    
class CompetencyForm(forms.ModelForm):
    """
    Formulir untuk membuat dan mengedit Capaian Kompetensi.
    """
    class Meta:
        model = Competency
        fields = ['code', 'description']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Contoh: TP 1.1 atau BAB 1'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'rows': 3,
                'placeholder': 'Contoh: Memahami konsep dasar aljabar'
            }),
        }
        labels = {
            'code': 'Kode Capaian Kompetensi',
            'description': 'Deskripsi Capaian Kompetensi',
        }
class UserEditForm(forms.ModelForm):
    """
    Form untuk mengedit data pengguna (termasuk siswa).
    """
    class Meta:
        model = User
        # Tentukan field apa saja yang ingin ditampilkan di form edit
        fields = [
            'username', 'first_name', 'last_name', 'email', 'role', 
            'class_group', # <-- INI FIELD PENTING YANG KITA TAMBAHKAN
            'nis', 'nisn', 'address', 'phone_number'
        ]
        widgets = {
            # Tambahkan styling agar konsisten dengan form Anda yang lain
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'role': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'class_group': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'nis': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'nisn': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        }
        labels = {
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'class_group': 'Kelas',
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # Membuat field 'class_group' tidak wajib diisi.
        # Berguna jika user yang diedit bukan siswa (misalnya guru).
        self.fields['class_group'].required = False

class MataPelajaranForm(forms.ModelForm):
    """
    Form untuk menambah dan mengedit mata pelajaran.
    """
    class Meta:
        model = MataPelajaran
        # --- PERBAIKAN DI SINI ---
        # Tambahkan 'level' dan 'description' agar muncul di form
        fields = ['nama', 'level', 'description']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Contoh: Matematika'}),
            'level': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Contoh: SMA, SMP, SD'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 3, 'placeholder': 'Deskripsi singkat (opsional)'}),
        }
        labels = {
            'nama': 'Nama Mata Pelajaran',
            'level': 'Jenjang/Tingkat',
            'description': 'Deskripsi',
        }

    def clean_level(self):
        # Fungsi untuk memastikan input Jenjang selalu huruf besar (opsional tapi bagus)
        level = self.cleaned_data.get('level')
        if level:
            return level.upper()
        return level
    
class ThemeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['theme']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }

class KomponenNilaiForm(forms.ModelForm):
    class Meta:
        model = KomponenNilai
        fields = ['nama_komponen']
        widgets = {
            'nama_komponen': forms.TextInput(attrs={'class': 'p-2 border rounded-md w-full', 'placeholder': 'Contoh: Tugas Harian'})
        }
        labels = {
            'nama_komponen': 'Nama Komponen Baru'
        }