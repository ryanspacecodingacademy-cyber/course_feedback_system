from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Faculty, Department, Course, Feedback

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    list_filter = ('faculty',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('course', 'student_name', 'rating', 'submitted_at')
    list_filter = ('course', 'rating', 'submitted_at')
    search_fields = ('student_name', 'comments')
