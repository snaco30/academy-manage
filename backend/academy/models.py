from django.db import models
from django.utils import timezone
import os

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    STATUS_CHOICES = [
        ('active', '재원생'),
        ('on_leave', '휴원'),
        ('suspended', '일시정지'),
        ('withdrawn', '퇴원'),
    ]

    # Personal Info
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="전화번호 뒤 4자리 등")
    phone_number = models.CharField(max_length=20, unique=True)
    password_hash = models.CharField(max_length=128, blank=True, null=True)
    
    gender = models.CharField(max_length=10, choices=[('M', '남성'), ('F', '여성')], default='M')
    school = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)
    
    # Parent Info
    parent_name = models.CharField(max_length=50, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=20)
    
    address = models.CharField(max_length=255, blank=True, null=True)
    detail_address = models.CharField(max_length=255, blank=True, null=True)
    
    birth_date = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(default=timezone.now)
    withdrawal_date = models.DateField(blank=True, null=True)
    
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    tuition_fee = models.IntegerField(default=0)
    memo = models.TextField(blank=True, help_text="관리 고정 메모")
    
    attendance_code = models.CharField(max_length=10, blank=True, null=True)
    manager_name = models.CharField(max_length=50, blank=True, null=True)
    payment_day = models.IntegerField(default=25, help_text="매월 결제일")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.school or '학교미정'})"

class AcademyClass(models.Model):
    name = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, related_name='classes', blank=True)
    schedule = models.CharField(max_length=200, blank=True) # e.g. "Mon,Wed 14:00"

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='present') # present, absent, late, etc.
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

class Memo(models.Model):
    # Global/Dashboard memos (quick memo)
    content = models.TextField()
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

class ConsultationLog(models.Model):
    # Specific to student
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='consultations')
    date = models.DateField(default=timezone.now)
    content = models.TextField()
    author = models.CharField(max_length=50, default='Admin')

class Homework(models.Model):
    academy_class = models.ForeignKey(AcademyClass, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='submitted') # submitted, late, graded

class Schedule(models.Model):
    COLOR_CHOICES = [
        ('indigo', 'Indigo'),
        ('emerald', 'Emerald'),
        ('rose', 'Rose'),
        ('amber', 'Amber'),
        ('blue', 'Blue'),
        ('pink', 'Pink'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='indigo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_date})"
