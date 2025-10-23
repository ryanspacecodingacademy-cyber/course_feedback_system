
from django.shortcuts import render, redirect
from .models import Faculty, Department, Course, Feedback

def home(request):
    faculties = Faculty.objects.all()
    return render(request, 'feedback/home.html', {'faculties': faculties})

def feedback_form(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Feedback.objects.create(course_id=course_id, rating=rating, comments=comment)
        return redirect('thank_you')

    faculty_id = request.GET.get('faculty')
    department_id = request.GET.get('department')

    faculties = Faculty.objects.all()
    departments = Department.objects.filter(faculty_id=faculty_id) if faculty_id else None
    courses = Course.objects.filter(department_id=department_id) if department_id else None

    context = {
        'faculties': faculties,
        'departments': departments,
        'courses': courses,
    }
    return render(request, 'feedback/feedback_form.html', context)

def thank_you(request):
    return render(request, 'feedback/thank_you.html')
