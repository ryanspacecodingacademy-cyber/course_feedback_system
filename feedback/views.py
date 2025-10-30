from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from .models import Faculty, Department, Course, Lecturer, Feedback

# Home page
def home(request):
    faculties = Faculty.objects.all()
    return render(request, 'feedback/home.html', {'faculties': faculties})

# Feedback form (anonymous submission)
def feedback_form(request):
    if request.method == 'POST':
        # Get IDs from POST
        faculty_id = request.POST.get('faculty')
        department_id = request.POST.get('department')
        course_id = request.POST.get('course')
        lecturer_id = request.POST.get('lecturer')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Save feedback anonymously
        Feedback.objects.create(
            faculty_id=faculty_id,
            department_id=department_id,
            course_id=course_id,
            lecturer_id=lecturer_id,
            rating=rating,
            comment=comment
        )
        return redirect('thank_you')

    # Handle GET filtering for dynamic dropdowns
    faculty_id = request.GET.get('faculty')
    department_id = request.GET.get('department')

    faculties = Faculty.objects.all()
    departments = Department.objects.filter(faculty_id=faculty_id) if faculty_id else Department.objects.none()
    courses = Course.objects.filter(department_id=department_id) if department_id else Course.objects.none()
    lecturers = Lecturer.objects.filter(course__in=courses) if courses.exists() else Lecturer.objects.none()

    context = {
        'faculties': faculties,
        'departments': departments,
        'courses': courses,
        'lecturers': lecturers
    }
    return render(request, 'feedback/feedback_form.html', context)

# Thank you page
def thank_you(request):
    return render(request, 'feedback/thank_you.html')

# Admin-only dashboard to view all feedback
@staff_member_required
def admin_dashboard(request):
    feedbacks = Feedback.objects.all().select_related('faculty', 'department', 'course', 'lecturer')

    # Optional filtering
    faculty_id = request.GET.get('faculty')
    department_id = request.GET.get('department')
    course_id = request.GET.get('course')
    lecturer_id = request.GET.get('lecturer')

    if faculty_id:
        feedbacks = feedbacks.filter(faculty_id=faculty_id)
    if department_id:
        feedbacks = feedbacks.filter(department_id=department_id)
    if course_id:
        feedbacks = feedbacks.filter(course_id=course_id)
    if lecturer_id:
        feedbacks = feedbacks.filter(lecturer_id=lecturer_id)

    # Calculate average rating
    average_rating = feedbacks.aggregate(avg=Avg('rating'))['avg']

    # Get most recent feedback for summary card
    recent_feedback = feedbacks.order_by('-submitted_at').first()

    context = {
        'feedbacks': feedbacks,
        'faculties': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'courses': Course.objects.all(),
        'lecturers': Lecturer.objects.all(),
        'average_rating': average_rating,
        'recent_feedback': recent_feedback,
    }
    return render(request, 'feedback/admin_dashboard.html', context)
