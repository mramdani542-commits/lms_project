from django import template
from django.utils import timezone
from dashboard.models import ExamAttempt # Ganti dengan path model Anda

register = template.Library()

@register.simple_tag(takes_context=True)
def get_exam_status(context, exam):
    request = context['request']
    now = timezone.now()
    
    # 1. Cek apakah siswa sudah menyelesaikan ujian ini
    already_completed = ExamAttempt.objects.filter(student=request.user, exam=exam, is_completed=True).exists()
    if already_completed:
        return "SELESAI"
        
    # 2. Cek waktu ujian
    if now < exam.start_time:
        return "BELUM_MULAI"
    elif now > exam.end_time:
        return "BERAKHIR"
    else:
        return "BERLANGSUNG"