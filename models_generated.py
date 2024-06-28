# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ClassroomClassassignment(models.Model):
    created_at = models.DateTimeField()
    assignment_name = models.CharField(max_length=250)
    assignment = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.ForeignKey('ClassroomTeacher', models.DO_NOTHING)
    semester = models.IntegerField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classroom_classassignment'


class ClassroomClassassignmentStudent(models.Model):
    classassignment = models.ForeignKey(ClassroomClassassignment, models.DO_NOTHING)
    student = models.ForeignKey('ClassroomStudent', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_classassignment_student'
        unique_together = (('classassignment', 'student'),)


class ClassroomClassnotice(models.Model):
    created_at = models.DateTimeField()
    message = models.TextField()
    message_html = models.TextField()
    teacher = models.ForeignKey('ClassroomTeacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_classnotice'
        unique_together = (('teacher', 'message'),)


class ClassroomClassnoticeStudents(models.Model):
    classnotice = models.ForeignKey(ClassroomClassnotice, models.DO_NOTHING)
    student = models.ForeignKey('ClassroomStudent', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_classnotice_students'
        unique_together = (('classnotice', 'student'),)


class ClassroomSemester(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'classroom_semester'


class ClassroomStudent(models.Model):
    user = models.OneToOneField('ClassroomUser', models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    phone = models.IntegerField()
    student_profile_pic = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'classroom_student'


class ClassroomStudentmarks(models.Model):
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField(blank=True, null=True)
    maximum_marks = models.IntegerField()
    student = models.ForeignKey(ClassroomStudent, models.DO_NOTHING)
    teacher = models.ForeignKey('ClassroomTeacher', models.DO_NOTHING)
    semester = models.IntegerField()
    assignment_mark_obtained = models.FloatField(blank=True, null=True)
    viva_mark_obtained = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classroom_studentmarks'


class ClassroomStudentsinclass(models.Model):
    student = models.ForeignKey(ClassroomStudent, models.DO_NOTHING)
    teacher = models.ForeignKey('ClassroomTeacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_studentsinclass'
        unique_together = (('teacher', 'student'),)


class ClassroomSubmitassignment(models.Model):
    created_at = models.DateTimeField()
    submit = models.CharField(max_length=100)
    submitted_assignment = models.ForeignKey(ClassroomClassassignment, models.DO_NOTHING)
    student = models.ForeignKey(ClassroomStudent, models.DO_NOTHING)
    teacher = models.ForeignKey('ClassroomTeacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_submitassignment'


class ClassroomTeacher(models.Model):
    user = models.OneToOneField('ClassroomUser', models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=250)
    subject_name = models.CharField(max_length=250)
    email = models.CharField(max_length=254)
    phone = models.IntegerField()
    teacher_profile_pic = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'classroom_teacher'


class ClassroomUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    is_student = models.BooleanField()
    is_teacher = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'classroom_user'


class ClassroomUserGroups(models.Model):
    user = models.ForeignKey(ClassroomUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_user_groups'
        unique_together = (('user', 'group'),)


class ClassroomUserUserPermissions(models.Model):
    user = models.ForeignKey(ClassroomUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'classroom_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(ClassroomUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
