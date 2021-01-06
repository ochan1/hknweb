from django.contrib import admin
from .models import Course, CourseSemester, CourseSemesterExams, Department, Instructor, Semester

admin.site.register(Course)
admin.site.register(CourseSemester)
admin.site.register(CourseSemesterExams)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Semester)
