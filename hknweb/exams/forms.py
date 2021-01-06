from django import forms

from hknweb.exams.models import Course, Semester, ExamTypes

EXAM_OR_SOLUTION = [('exam', 'Exam'), ('sol', 'Solution')]

class ExamUploadForm(forms.Form):

    course = forms.ModelChoiceField(queryset=Course.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    
    Exam_Type_Choices = []
    for examType in ExamTypes:
        examTypeName = examType.exam_type
        if examType.max_number_of_exams < 0:
            examTypeNameValue = examTypeName
            Exam_Type_Choices.append((examTypeNameValue, examTypeNameValue))
        else:
            for i in range(examType.max_number_of_exams):
                examTypeNameValue = examTypeName + " " + i
                examTypeNameKey = examTypeName + "--" + i
                Exam_Type_Choices.append((examTypeNameKey, examTypeNameValue))

    exam = forms.CharField(label='Exam', widget=forms.Select(choices=Exam_Type_Choices))
    type = forms.CharField(label='Type', widget=forms.Select(choices=EXAM_OR_SOLUTION))

    file = forms.FileField(label="Exam")
