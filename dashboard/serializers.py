# api/serializers.py

from rest_framework import serializers
from .models import User, ClassGroup, MataPelajaran, Kehadiran, Ekstrakurikuler, Prestasi, CatatanWaliKelas, TanggapanOrangTua, Nilai

# Serializer sederhana untuk menampilkan daftar
class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializer untuk menampilkan nama dan ID siswa."""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

    def to_representation(self, instance):
        # Menggabungkan nama depan dan belakang
        return {
            'id': instance.id,
            'name': instance.get_full_name() or instance.username
        }

class SimpleMataPelajaranSerializer(serializers.ModelSerializer):
    """Serializer untuk menampilkan nama dan ID mapel."""
    class Meta:
        model = MataPelajaran
        fields = ['id', 'nama']
    
    def to_representation(self, instance):
        # Menggunakan field 'nama' dari model
        return {
            'id': instance.id,
            'name': instance.nama
        }

class ClassGroupSerializer(serializers.ModelSerializer):
    """Serializer untuk daftar kelas di dropdown filter."""
    homeroom_teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = ClassGroup
        fields = ['id', 'name', 'level', 'homeroom_teacher_name', 'is_wali_kelas']

    def get_homeroom_teacher_name(self, obj):
        # Mengambil nama lengkap wali kelas
        if obj.homeroom_teacher:
            return obj.homeroom_teacher.get_full_name() or obj.homeroom_teacher.username
        return "Belum Ditentukan"

# Serializers untuk detail data rapor
class KehadiranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kehadiran
        fields = ['sakit', 'izin', 'alpha']

class EkstrakurikulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ekstrakurikuler
        fields = ['id', 'nama_kegiatan', 'predikat', 'keterangan']

class PrestasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestasi
        fields = ['id', 'jenis_kegiatan', 'keterangan']

class CatatanWaliKelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatatanWaliKelas
        fields = ['catatan']

class TanggapanOrangTuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TanggapanOrangTua
        fields = ['id', 'tanggapan', 'tanggal']

class NilaiSerializer(serializers.ModelSerializer):
    mapel_name = serializers.CharField(source='mata_pelajaran.nama', read_only=True)
    
    class Meta:
        model = Nilai
        fields = ['id', 'mapel_name', 'nilai_akhir', 'deskripsi']


# Serializer utama yang menggabungkan semua data rapor
class RaporSiswaSerializer(serializers.ModelSerializer):
    """Serializer utama untuk mengambil dan menyimpan semua data rapor siswa."""
    profil = serializers.SerializerMethodField()
    kehadiran = KehadiranSerializer(source='kehadiran_siswa', required=False)
    ekskul = EkstrakurikulerSerializer(source='ekskul_siswa', many=True, required=False)
    prestasi = PrestasiSerializer(source='prestasi', many=True, required=False)
    catatan = CatatanWaliKelasSerializer(source='catatan_wali_kelas', many=True, required=False)
    ortu = TanggapanOrangTuaSerializer(source='tanggapan_orang_tua', many=True, required=False)
    
    # Untuk tampilan Wali Kelas
    akademik_wali = serializers.SerializerMethodField()
    
    # Untuk tampilan Guru Mapel (akan diisi di view)
    akademik_guru = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['profil', 'akademik_wali', 'akademik_guru', 'kehadiran', 'ekskul', 'prestasi', 'catatan', 'ortu']

    def get_profil(self, obj):
        return {
            'name': obj.get_full_name() or obj.username,
            'nisn': obj.nisn,
            'photo_url': obj.profile_picture.url if obj.profile_picture else None
        }
        
    def get_akademik_wali(self, obj):
        # Mengambil semua nilai akhir siswa untuk semua mapel
        nilai_queryset = Nilai.objects.filter(siswa=obj)
        return NilaiSerializer(nilai_queryset, many=True).data

    def get_akademik_guru(self, obj):
        # Logika ini akan ditangani di view untuk mendapatkan data TP
        # berdasarkan mata pelajaran yang dipilih.
        return self.context.get('akademik_guru_data', [])
