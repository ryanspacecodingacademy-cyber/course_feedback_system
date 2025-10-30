from django.contrib import admin
from .models import Faculty, Department, Course, Lecturer, Feedback


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('name', 'faculty__name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'code', 'department__name')


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_department', 'course')
    list_filter = ('course__department',)
    search_fields = ('name', 'course__department__name')

    def get_department(self, obj):
        return obj.course.department
    get_department.short_description = 'Department'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('course', 'lecturer', 'rating', 'comment', 'submitted_at')
    list_filter = ('course', 'lecturer', 'rating', 'submitted_at')
    search_fields = ('comment', 'course__name', 'lecturer__name')
