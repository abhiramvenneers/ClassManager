from django import forms
from django.contrib.auth.forms import UserCreationForm
from classroom.models import User,Teacher,Student,StudentMarks,ClassNotice,ClassAssignment,SubmitAssignment
from django.db import transaction

## User Login Form (Applied in both student and teacher login)
class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']
        widgets = {
                'username': forms.TextInput(attrs={'class':'answer'}),
                'password1': forms.PasswordInput(attrs={'class':'answer'}),
                'password2': forms.PasswordInput(attrs={'class':'answer'}),
                }
        
## Teacher Registration Form 
class TeacherProfileForm(forms.ModelForm):
    class Meta():
        model =  Teacher
        fields = ['name','subject_name','phone','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'subject_name': forms.TextInput(attrs={'class':'answer'}),
                'phone': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Teacher Profile Update Form
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name','subject_name','email','phone','teacher_profile_pic']

## Student Registration Form
class StudentProfileForm(forms.ModelForm):
    class Meta():
        model =  Student
        fields = ['name','roll_no','phone','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'roll_no': forms.NumberInput(attrs={'class':'answer'}),
                'phone': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Student profile update form
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name','roll_no','email','phone','student_profile_pic']
        


class MarksForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
        (9, 'Semester 9'),
        (10, 'Semester 10'),
    ]
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='Semester')
    class Meta:
        model = StudentMarks
        fields = ['semester', 'subject_name', 'marks_obtained', 'maximum_marks']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marks_obtained'].label = 'Internal Marks'
        self.fields['maximum_marks'].label = 'Maximum Marks'

class AssignmentMarkForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
        (9, 'Semester 9'),
        (10, 'Semester 10'),
    ]
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='Semester')
    
    class Meta:
        model = StudentMarks
        fields = ['semester', 'subject_name', 'assignment_mark_obtained']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignment_mark_obtained'].label = 'Assignment Marks'
        

class VivaMarkForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
        (9, 'Semester 9'),
        (10, 'Semester 10'),
    ]
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='Semester')
    
    class Meta:
        model = StudentMarks
        fields = ['semester', 'subject_name', 'viva_mark_obtained']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['viva_mark_obtained'].label = 'Viva Marks'
        
        
## Writing notice in the class        
class NoticeForm(forms.ModelForm):
    class Meta():
        model = ClassNotice
        fields = ['message']
        


## Form for uploading or updating assignment (teachers only)       
class AssignmentForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
        (9, 'Semester 9'),
        (10, 'Semester 10'),
    ]
    
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='Semester')
     
    end_date = forms.DateTimeField()
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','semester','assignment','end_date']
        
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].widget.attrs['placeholder'] = 'yy:mm:dd h:m:s'

## Form for submitting assignment (Students only)        
class SubmitForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submit']




