from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Student, Schedule, Attendance
from django.contrib import messages
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@ensure_csrf_cookie
def home(request):
    return render(request, 'academy/home.html')

def api_schedule_list(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    schedules = Schedule.objects.all()
    if start_date:
        schedules = schedules.filter(start_date__gte=start_date)
    if end_date:
        schedules = schedules.filter(start_date__lte=end_date)
    
    data = []
    for s in schedules:
        data.append({
            'id': s.id,
            'title': s.title,
            'description': s.description,
            'start_date': s.start_date.isoformat(),
            'start_time': s.start_time.isoformat() if s.start_time else None,
            'color': s.color,
            'created_at': s.created_at.isoformat(),
            'updated_at': s.updated_at.isoformat(),
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def api_schedule_save(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_id = data.get('id')
            if schedule_id:
                schedule = get_object_or_404(Schedule, id=schedule_id)
            else:
                schedule = Schedule()
            
            schedule.title = data.get('title')
            schedule.description = data.get('description', '')
            schedule.start_date = data.get('start_date')
            schedule.color = data.get('color', 'indigo')
            schedule.save()
            return JsonResponse({'status': 'success', 'id': schedule.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def api_schedule_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_id = data.get('id')
            if not schedule_id:
                return JsonResponse({'status': 'error', 'message': 'ID is required'}, status=400)
            schedule = get_object_or_404(Schedule, id=schedule_id)
            schedule.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def attendance_management(request):
    date_str = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    students = Student.objects.all().order_by('name')
    attendances = Attendance.objects.filter(date=selected_date)
    attendance_dict = {a.student_id: a for a in attendances}
    
    student_data = []
    for s in students:
        attendance = attendance_dict.get(s.id)
        student_data.append({
            'id': s.id,
            'name': s.name,
            'school': s.school,
            'status': attendance.status if attendance else 'absent',
            'check_in': attendance.check_in_time if attendance else None,
            'check_out': attendance.check_out_time if attendance else None,
        })
        
    return render(request, 'academy/attendance_management.html', {
        'student_data': student_data,
        'selected_date': date_str,
    })

@csrf_exempt
def api_attendance_update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            date_str = data.get('date')
            status = data.get('status')
            
            student = get_object_or_404(Student, id=student_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            attendance, created = Attendance.objects.get_or_create(
                student=student, 
                date=date,
                defaults={'status': status}
            )
            if not created:
                attendance.status = status
                if status == 'present' and not attendance.check_in_time:
                    attendance.check_in_time = datetime.now().time()
            
            attendance.is_present = (status == 'present')
            attendance.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def student_management(request):
    query = request.GET.get('q', '')
    students = Student.objects.all().order_by('-created_at')
    
    if query:
        students = students.filter(name__icontains=query)

    selected_student_id = request.GET.get('id')
    selected_student = None
    if selected_student_id:
        selected_student = get_object_or_404(Student, id=selected_student_id)

    if request.method == 'POST':
        # Determine if creating or updating
        student_id = request.POST.get('id')
        if student_id:
            student = get_object_or_404(Student, id=student_id)
            messages.success(request, '학생 정보가 수정되었습니다.')
        else:
            student = Student()
            messages.success(request, '신규 학생이 등록되었습니다.')
        
        # Update fields
        student.name = request.POST.get('name')
        student.phone_number = request.POST.get('phone_number')
        student.parent_name = request.POST.get('parent_name')
        student.parent_phone_number = request.POST.get('parent_phone_number')
        student.school = request.POST.get('school')
        student.gender = request.POST.get('gender', 'M')
        student.status = request.POST.get('status', 'active')
        student.address = request.POST.get('address')
        student.detail_address = request.POST.get('detail_address')
        student.attendance_code = request.POST.get('attendance_code')
        student.payment_day = request.POST.get('payment_day') or 25
        student.manager_name = request.POST.get('manager_name')
        
        # Date fields
        enrollment_date = request.POST.get('enrollment_date')
        if enrollment_date:
            student.enrollment_date = enrollment_date
            
        if request.FILES.get('photo'):
            student.photo = request.FILES.get('photo')
            
        student.save()
        
        return redirect(f'/management/?id={student.id}')

    return render(request, 'academy/student_management_v2.html', {
        'students': students,
        'selected_student': selected_student,
        'query': query,
    })
