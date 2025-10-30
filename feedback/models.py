from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['faculty', 'name']

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, unique=True)

    class Meta:
        ordering = ['department', 'name']

    def __str__(self):
        return f"{self.name} - {self.code}" if self.code else self.name


class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lecturers')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.course.name})"

    @property
    def department(self):
        """Return the department of the lecturer via the course."""
        return self.course.department if self.course else None


class Feedback(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        course_name = self.course.name if self.course else "No course"
        return f"Feedback for {course_name} ({self.rating}/5)"
