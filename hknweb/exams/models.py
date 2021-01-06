from django.db import models

class Department(models.Model):
    abbreviated_name = models.CharField(unique=True, max_length=10, null=True) #short form (e.g. 'EE')
    long_name = models.CharField(max_length=255) #long form (e.g. 'Electrical Engineering')

    def __str__(self):
        return "{} ({})".format(self.long_name, self.abbreviated_name)

class Instructor(models.Model):
    first_name       = models.CharField(max_length=255)
    middle_name      = models.CharField(max_length=255, default="")
    last_name        = models.CharField(max_length=255, default="")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    # Instructor may or may not allows exams to be published (Exams are copyrighted)
    exam_permissions = models.BooleanField(default=False)

    # Example: Danny Dan Garcia
    def getFullName(self):
        middleNameSection = ""
        if len(self.middle_name) != 0:
            middleNameSection = " " + self.middle_name
        lastNameSection = ""
        if len(self.last_name) != 0:
            lastNameSection = " " + self.last_name
        return self.first_name + middleNameSection + lastNameSection
    
    # Example: Garcia, Danny
    def getLastNameFirstName(self):
        lastNameSection = self.last_name
        # Include comma if the first name exist (otherwise, don't)
        if len(self.first_name) != 0:
            lastNameSection += ", "
        return lastNameSection + self.first_name

    def __str__(self):
        return "{} (Department: {})".format(self.getFullName(), self.department)

class Course(models.Model):
    name        = models.CharField(max_length=255, null=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number 		= models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department.abbreviated_name, self.number)

class Semester(models.Model):
    semester = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.semester, self.year)

# class CourseSemester(models.Model):
#     course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
#     semester    = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     instructor  = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
#     release     = models.BooleanField()
#     midterm1    = models.FileField(blank=True)
#     midterm1_sol = models.FileField(blank=True)
#     midterm2    = models.FileField(blank=True)
#     midterm2_sol = models.FileField(blank=True)
#     midterm3    = models.FileField(blank=True)
#     midterm3_sol = models.FileField(blank=True)
#     final       = models.FileField(blank=True)
#     final_sol   = models.FileField(blank=True)

#     def __str__(self):
#         return "CourseSemester(course={}, semester={})".format(self.course, self.semester)

class CourseSemester(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester    = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # instructor  = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
    instructors = models.ManyToManyField(Instructor, blank=False)

    def __str__(self):
        return "CourseSemester(course={}, semester={})".format(self.course, self.semester)

# Create your models here.
class CourseSemesterExams(models.Model):
    courseSemester = models.ForeignKey(CourseSemester, on_delete=models.CASCADE, null=True)

    exam_release = models.BooleanField(default=False)

    def __str__(self):
        return "CourseSemesterExams(courseSemester={}, exam_release={})".format(self.courseSemester, self.exam_release)

class ExamTypes(models.Model):
    exam_type = models.CharField(max_length=15)
    max_number_of_exams = models.IntegerField(default=-1)

    def __str__(self):
        return self.exam_type

class Exams(models.Model):
    courseSemester = models.ForeignKey(CourseSemesterExams, on_delete=models.CASCADE, null=False)
    exam_type   = models.ForeignKey(ExamTypes, on_delete=models.CASCADE)
    exam_number = models.IntegerField(default=-1)
    exam        = models.FileField(blank=True)
    exam_sol    = models.FileField(blank=True)

    def __str__(self):
        examNumberSection = ""
        if self.exam_number < 0:
            examNumberSection = " " + self.exam_number
        return "{}{} - {}".format(self.exam_type, examNumberSection, self.exam)

    # Style to AVOID:
    # midterm1    = models.FileField(blank=True)
    # midterm1_sol = models.FileField(blank=True)
    # midterm2    = models.FileField(blank=True)
    # midterm2_sol = models.FileField(blank=True)
    # midterm3    = models.FileField(blank=True)
    # midterm3_sol = models.FileField(blank=True)
    # final       = models.FileField(blank=True)
    # final_sol   = models.FileField(blank=True)


