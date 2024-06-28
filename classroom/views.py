from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.generic import  (View,TemplateView,
                                  ListView,DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from classroom.forms import AssignmentMarkForm,VivaMarkForm,UserForm,TeacherProfileForm,StudentProfileForm,MarksForm,NoticeForm,AssignmentForm,SubmitForm,TeacherProfileUpdateForm,StudentProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from classroom import models
from classroom.models import StudentsInClass,StudentMarks,ClassAssignment,SubmitAssignment,Student,Teacher, ClassNotice
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.utils import timezone


# For Teacher Sign Up
def TeacherSignUp(request):
    user_type = 'teacher'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_profile_form = TeacherProfileForm(data = request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():

            user = user_form.save()
            user.is_teacher = True
            user.save()

            profile = teacher_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = TeacherProfileForm()

    return render(request,'classroom/teacher_signup.html',{'user_form':user_form,'teacher_profile_form':teacher_profile_form,'registered':registered,'user_type':user_type})


###  For Student Sign Up
def StudentSignUp(request):
    user_type = 'student'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_profile_form = StudentProfileForm(data = request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():

            user = user_form.save()
            user.is_student = True
            user.save()

            profile = student_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,student_profile_form.errors)
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()

    return render(request,'classroom/student_signup.html',{'user_form':user_form,'student_profile_form':student_profile_form,'registered':registered,'user_type':user_type})

## Sign Up page which will ask whether you are teacher or student.
def SignUp(request):
    return render(request,'classroom/signup.html',{})

## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('classroom:login')
    else:
        return render(request,'classroom/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

## User Profile of student.
class StudentDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'classroom/student_detail_page.html'

## User Profile for teacher.
class TeacherDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "teacher"
    model = models.Teacher
    template_name = 'classroom/teacher_detail_page.html'

## Profile update for students.
@login_required
def StudentUpdateView(request,pk):
    profile_updated = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST,instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'student_profile_pic' in request.FILES:
                profile.student_profile_pic = request.FILES['student_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None,instance=student)
    return render(request,'classroom/student_update_page.html',{'profile_updated':profile_updated,'form':form})

## Profile update for teachers.
@login_required
def TeacherUpdateView(request,pk):
    profile_updated = False
    teacher = get_object_or_404(models.Teacher,pk=pk)
    if request.method == "POST":
        form = TeacherProfileUpdateForm(request.POST,instance=teacher)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'teacher_profile_pic' in request.FILES:
                profile.teacher_profile_pic = request.FILES['teacher_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = TeacherProfileUpdateForm(request.POST or None,instance=teacher)
    return render(request,'classroom/teacher_update_page.html',{'profile_updated':profile_updated,'form':form})

## List of all students that teacher has added in their class.
def class_students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in students_list:
            qs_one.append(x)
        else:
            pass
    context = {
        "class_students_list": qs_one,
    }
    template = "classroom/class_students_list.html"
    return render(request, template, context)

class ClassStudentsListView(LoginRequiredMixin,DetailView):
    model = models.Teacher
    template_name = "classroom/class_students_list.html"
    context_object_name = "teacher"

## For Marks obtained by the student in all subjects.

from django.db.models import Avg

class StudentAllMarksList(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "classroom/student_allmarks_list.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object

        # Retrieve all marks for the student
        all_marks = student.marks.all()

        # Filter marks based on form input
        semester_filter = self.request.GET.get('semester')
        teacher_filter = self.request.GET.get('teacher')

        if semester_filter:
            all_marks = all_marks.filter(semester=semester_filter)
        
        if teacher_filter:
            all_marks = all_marks.filter(teacher__pk=teacher_filter)

        # Organize marks by semester and by teacher
        semester_marks = {}
        teacher_marks = {}

        for mark in all_marks:
            semester = mark.semester
            teacher = mark.teacher

            # Organize marks by semester
            if semester not in semester_marks:
                semester_marks[semester] = []
            semester_marks[semester].append(mark)

            # Organize marks by teacher
            if teacher not in teacher_marks:
                teacher_marks[teacher] = []
            teacher_marks[teacher].append(mark)

        context['semester_marks'] = semester_marks
        context['teacher_marks'] = teacher_marks
        context['all_marks'] = all_marks  # For displaying all marks if no filter is applied

        # Calculate average marks per semester
        total_marks_per_semester = {}
        count_marks_per_semester = {}

        for mark in all_marks:
            semester = mark.semester
            marks_obtained = mark.marks_obtained

            if semester not in total_marks_per_semester:
                total_marks_per_semester[semester] = []
            
            if marks_obtained is not None:
                total_marks_per_semester[semester].append(marks_obtained)

            count_marks_per_semester[semester] = len(total_marks_per_semester.get(semester, []))

        average_marks_per_semester = {}
        for semester, total_marks in total_marks_per_semester.items():
            if total_marks:
                total_marks.sort(reverse=True)
                top_two_marks = total_marks[:2]
                average_marks = round(sum(top_two_marks) / len(top_two_marks) / mark.maximum_marks * 5)
                average_marks_per_semester[semester] = average_marks
            else:
                average_marks_per_semester[semester] = None

        context['average_marks_per_semester'] = average_marks_per_semester

        return context

    
## To give marks to a student.
from django.core.exceptions import ValidationError

@login_required
def add_marks(request, pk):
    marks_given = False
    student = get_object_or_404(models.Student, pk=pk)
    
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            # Count the number of existing submissions for the semester
            semester = form.cleaned_data['semester']
            teacher = request.user.Teacher
            submissions_count = StudentMarks.objects.filter(student=student, semester=semester, teacher=teacher).count()
            # Check if the semester has reached the maximum number of submissions for this teacher
            if submissions_count < 4:
                marks = form.save(commit=False)
                marks.student = student
                marks.teacher = teacher
                marks.save()
                marks_given = True
                messages.success(request, 'Marks uploaded successfully!')
                return redirect('classroom:student_marks_list', pk=pk)
                
                
            else:
             messages.error(request, 'Maximum number of submissions (4) reached for this semester for this teacher!')
             return redirect('classroom:student_marks_list', pk=pk)   
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    else:
        form = MarksForm()
    
    return render(request, 'classroom/add_marks.html', {'form': form, 'student': student, 'marks_given': marks_given})


@login_required
def add_viva_mark(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    teacher = request.user.Teacher
    if request.method == 'POST':
        form =VivaMarkForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']  
            existing_mark = StudentMarks.objects.filter(student=student, semester=semester, teacher=teacher, assignment_mark_obtained__isnull=False).exists()
            if not existing_mark:    
                viva_marks = form.save(commit=False)
                viva_marks.teacher = teacher
                viva_marks.student = student
                viva_marks.save()
                return redirect('classroom:student_marks_list', pk=student.pk)
            else:
                messages.error(request, 'You have already submitted an assignment mark for this semester.')
    else:
        form = VivaMarkForm()
    return render(request, 'classroom/add_viva_mark.html', {'form': form, 'student': student})

@login_required
def add_assignment_mark(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    teacher = request.user.Teacher
    
    if request.method == 'POST':
        form = AssignmentMarkForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']  
            existing_mark = StudentMarks.objects.filter(student=student, semester=semester, teacher=teacher, assignment_mark_obtained__isnull=False).exists()
            
            if not existing_mark:
                assignment_marks = form.save(commit=False)
                assignment_marks.teacher = teacher
                assignment_marks.student = student
                assignment_marks.save()
                return redirect('classroom:student_marks_list', pk=student.pk)
            else:
                messages.error(request, 'You have already submitted an assignment mark for this semester.')
    else:
        form = AssignmentMarkForm()
    
    return render(request, 'classroom/add_assignment_mark.html', {'form': form, 'student': student})






## For updating marks.
@login_required
def update_marks(request,pk):
    marks_updated = False
    obj = get_object_or_404(StudentMarks,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST,instance=obj)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks_updated = True
            
    else:
        form = MarksForm(request.POST or None,instance=obj)
    return render(request,'classroom/update_marks.html',{'form':form,'marks_updated':marks_updated})


## For writing notice which will be sent to all class students.
@login_required
def add_notice(request):
    notice_sent = False
    teacher = request.user.Teacher
    students = StudentsInClass.objects.filter(teacher=teacher)
    students_list = [x.student for x in students]

    if request.method == "POST":
        notice_form = NoticeForm(request.POST)
        if notice_form.is_valid():
            notice_content = notice_form.cleaned_data['message']
            existing_notice = ClassNotice.objects.filter(teacher=teacher, message=notice_content).exists()
            if existing_notice:
                # Handle the case where the same notice already exists
                return render(request, 'classroom/error.html')
            else:
                notice = notice_form.save(commit=False)
                notice.teacher = teacher
                notice.save()
                notice.students.add(*students_list)
                notice_sent = True
    else:
        notice = NoticeForm()
    return render(request,'classroom/write_notice.html',{'notice':notice,'notice_sent':notice_sent})


## For the list of all the messages teacher have received.
@login_required
def messages_list(request,pk):
    teacher = get_object_or_404(models.Teacher,pk=pk)
    return render(request,'classroom/messages_list.html',{'teacher':teacher})

## Student can see all notice given by their teacher.
@login_required
def class_notice(request,pk):
    student = get_object_or_404(models.Student,pk=pk)
    return render(request,'classroom/class_notice_list.html',{'student':student})

## To see the list of all the marks given by the techer to a specific student.


@login_required
def student_marks_list(request, pk):
    student = get_object_or_404(Student, pk=pk)
    teacher = request.user.Teacher
    given_marks = StudentMarks.objects.filter(student=student, teacher=teacher)

    # Create a dictionary to store the total marks and count for each semester
    total_marks_per_semester = {}
    count_marks_per_semester = {}

 

    # Calculate the total marks and count for each semester
    for mark in given_marks:
        semester = mark.semester
        marks_obtained = mark.marks_obtained

        if semester not in total_marks_per_semester:
            total_marks_per_semester[semester] = [marks_obtained]
        else:
            total_marks_per_semester[semester].append(marks_obtained)
            

        count_marks_per_semester[semester] = len(total_marks_per_semester[semester])

    # Calculate the average marks per semester
    average_marks_per_semester = {}
    for semester, total_marks in total_marks_per_semester.items():
        if total_marks:
            total_marks = [mark for mark in total_marks if mark is not None]
            if total_marks:
                total_marks.sort(reverse=True)
                total_marks = total_marks[:2]
                average_marks  = round(sum(total_marks) / 32 * 5)
            else:
                average_marks = None
        else:
            average_marks = None 
            
        average_marks_per_semester[semester]={
            
            "average_marks":average_marks,
            "viva_mark":0,
            "assignment_mark":0,
            'total_ce_marks':0
            
        } 
        

    assignment_mark = StudentMarks.objects.filter(student=student, teacher=teacher)
    viva_mark = StudentMarks.objects.filter(student=student, teacher=teacher)
    for marks in assignment_mark:
        semester = marks.semester 
        if semester in average_marks_per_semester:
            if marks.assignment_mark_obtained is not None:
                average_marks_per_semester[semester]["assignment_mark"] += marks.assignment_mark_obtained
                
                
    for marks in viva_mark:
        semester = marks.semester
        if semester in average_marks_per_semester:
            if marks.viva_mark_obtained is not None:
                average_marks_per_semester[semester]["viva_mark"] += marks.viva_mark_obtained
                
                
    for semester_data in average_marks_per_semester.values():
        if semester_data['average_marks'] != None:
            semester_data['total_ce_marks'] = (
                semester_data['average_marks'] +
                semester_data['viva_mark'] +
                semester_data['assignment_mark']
            )
        else:
            semester_data['total_ce_marks'] = (
                semester_data['viva_mark'] +
                semester_data['assignment_mark']
            )
        
    print("average marks",average_marks_per_semester)

    context = {
        'student': student,
        'given_marks': given_marks,
        'average_marks_per_semester': average_marks_per_semester,
    }

    return render(request, 'classroom/student_marks_list.html', context)

## To add student in the class.
class add_student(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('classroom:students_list')

    def get(self,request,*args,**kwargs):
        student = get_object_or_404(models.Student,pk=self.kwargs.get('pk'))

        try:
            StudentsInClass.objects.create(teacher=self.request.user.Teacher,student=student)
        except:
            messages.warning(self.request,'warning, Student already in class!')
        else:
            messages.success(self.request,'{} successfully added!'.format(student.name))

        return super().get(request,*args,**kwargs)

@login_required
def student_added(request):
    return render(request,'classroom/student_added.html',{})

## List of students which are not added by teacher in their class.
def students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in students_list:
            pass
        else:
            qs_one.append(x)

    context = {
        "students_list": qs_one,
    }
    template = "classroom/students_list.html"
    return render(request, template, context)

## List of all the teacher present in the portal.
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Teacher.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )

    context = {
        "teachers_list": qs,
    }
    template = "classroom/teachers_list.html"
    return render(request, template, context)


####################################################

## Teacher uploading assignment.
@login_required
def upload_assignment(request):
    assignment_uploaded = False
    teacher = request.user.Teacher
    students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.end_date = form.cleaned_data['end_date']
            students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)
            upload.save()
            upload.student.add(*students)
            assignment_uploaded = True
    else:
        form = AssignmentForm()
    return render(request,'classroom/upload_assignment.html',{'form':form,'assignment_uploaded':assignment_uploaded})

## Students getting the list of all the assignments uploaded by their teacher.
@login_required
def class_assignment(request):
    student = request.user.Student
    current_time = timezone.now()
    assignment = SubmitAssignment.objects.filter(student=student)
    assignment_list = [x.submitted_assignment for x in assignment]
    
    return render(request,'classroom/class_assignment.html',{'student':student,'assignment_list':assignment_list})

## List of all the assignments uploaded by the teacher himself.
@login_required
def assignment_list(request):
    teacher = request.user.Teacher
    return render(request,'classroom/assignment_list.html',{'teacher':teacher})

## For updating the assignments later.
@login_required
def update_assignment(request,id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        obj.save()
        messages.success(request, "Updated Assignment".format(obj.assignment_name))
        return redirect('classroom:assignment_list')
    template = "classroom/update_assignment.html"
    return render(request, template, context)

## For deleting the assignment.
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Assignment Removed")
        return redirect('classroom:assignment_list')
    context = {
        "object": obj,
    }
    template = "classroom/assignment_delete.html"
    return render(request, template, context)

## For students submitting their assignment.
@login_required
def submit_assignment(request, id=None):
    student = request.user.Student
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.teacher
    
    # Check if the assignment deadline has passed
    if timezone.now() > assignment.end_date:
        return render(request,'classroom/assignment_expired.html')
    
    non_submitted_students = Student.objects.filter(~Q(student_submit__submitted_assignment=assignment))
    
    
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            assignment.status = "Submitted"
            assignment.save()
            return redirect('classroom:class_assignment')
    else:
        form = SubmitForm()
        
       
    context = {
        'form': form,
        'non_submitted_students': non_submitted_students,
        }
    return render(request,'classroom/submit_assignment.html',context)
## To see all the submissions done by the students.




@login_required
def submit_list(request):
    teacher = request.user.Teacher

    # Handle semester filtering
    semester_id = request.GET.get('semester_id')
    if semester_id:
        submitted_assignments = SubmitAssignment.objects.filter(
            teacher=teacher,
            submitted_assignment__semester=semester_id
        )
    else:
        submitted_assignments = SubmitAssignment.objects.filter(teacher=teacher)

    submitted_assignment_ids = submitted_assignments.values_list('submitted_assignment_id', flat=True)

    non_submitted_students = Student.objects.filter(
        student_assignment__teacher=teacher
    ).exclude(
        student_assignment__id__in=submitted_assignment_ids
    )

    context = {
        'teacher': teacher,
        'submitted_assignments': submitted_assignments,
        'non_submitted_students': non_submitted_students,
        'semester_id': semester_id,  # Pass semester_id to template for filtering
    }

    return render(request, 'classroom/submit_list.html', context)
##################################################################################################

## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('classroom:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'classroom/change_password.html',args)


# views.py

