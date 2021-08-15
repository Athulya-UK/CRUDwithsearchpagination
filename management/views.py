from django.core import paginator
from django.http.response import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404, render,redirect
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.urls import reverse

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    if 's' in request.GET:
        s=request.GET['s']
        data=models.Subject.objects.filter(subject_name__icontains=s)
    else:
        data=models.Subject.objects.all()
    paginator=Paginator(data,3)
    page=request.GET.get('page')
    try:
        data=paginator.page(page)
    except PageNotAnInteger:
        data=paginator.page(1)
    except EmptyPage:
        data=paginator.page(paginator.num_pages)
    return render(request,'management/index.html',{'data':data,'page':page})
# def home_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     data=models.Subject.objects.all()
#     paginator=Paginator(data,3)
#     page=request.GET.get('page')
#     try:
#         data=paginator.page(page)
#     except PageNotAnInteger:
#         data=paginator.page(1)
#     except EmptyPage:
#         data=paginator.page(paginator.num_pages)

#     return render(request,'management/index.html',{'data':data,'page':page})

def detail_page(request,subect_id):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    obj=get_object_or_404(models.Subject,pk=subect_id)
    return render(request,'management/detail.html',{'obj':obj})

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'management/adminclick.html')

def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'management/teacherclick.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'management/studentclick.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'management/adminsignup.html',{'form':form})

def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'management/studentsignup.html',context=mydict)

def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'management/teachersignup.html',context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        
        return HttpResponseRedirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            
            return HttpResponseRedirect('teacher-dashboard')
        else:
            return render(request,'management/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return HttpResponseRedirect('student-dashboard')
        else:
            return render(request,'management/student_wait_for_approval.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.Teacher.objects.all().filter(status=True).count()
    pendingteachercount=models.Teacher.objects.all().filter(status=False).count()

    studentcount=models.Student.objects.all().filter(status=True).count()
    pendingstudentcount=models.Student.objects.all().filter(status=False).count()

    notice=models.Notice.objects.all()

    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'notice':notice,
    }
    return render(request,'management/admin_dashboard.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'management/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'management/admin_add_teacher.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.Teacher.objects.all().filter(status=True)
    return render(request,'management/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=models.Teacher.objects.all().filter(status=False)
    return render(request,'management/admin_approve_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    # return redirect(reverse('admin-approve-teacher'))
    # return HttpResponseRedirect(reverse('admin-approve-teacher'))
    return render(request,'management/updatemessage.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    # return redirect('admin-approve-teacher')
    return render(request,'management/admin_approve_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    # return redirect('admin-view-teacher')
    return render(request,'management/admin_view_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            # return HttpResponseRedirect('admin-view-teacher')
        return render(request,'management/updatemessage.html')
    return render(request,'management/admin_update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'management/admin_student.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'management/admin_add_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.Student.objects.all().filter(status=True)
    return render(request,'management/admin_view_student.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    # return HttpResponseRedirect('admin-view-student')
    return render(request,'management/admin_view_student.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    # return HttpResponseRedirect('admin-approve-student')
    return render(request,'management/admin_approve_student.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            # return HttpResponseRedirect('admin-view-student')
        return render(request,'management/updatemessage.html')
    return render(request,'management/admin_update_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.Student.objects.all().filter(status=False)
    return render(request,'management/admin_approve_student.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.Student.objects.get(id=pk)
    students.status=True
    students.save()
    return render(request,'management/updatemessage.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return HttpResponseRedirect('admin-dashboard')
    return render(request,'management/admin_notice.html',{'form':form})

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_notice_delete(request,id):
#     models.Notice.objects.filter(id=id).delete()
#     return redirect("/")

# #for TEACHER  LOGIN    SECTION
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.Teacher.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'management/teacher_dashboard.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return HttpResponseRedirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'management/teacher_notice.html',{'form':form})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.Student.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'mobile':studentdata[0].mobile,
        'date':studentdata[0].joindate,
        'notice':notice
    }
    return render(request,'management/student_dashboard.html',context=mydict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_joinmeeting(request):
    return render(request,'management/student_joinmeeting.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_joinmeeting(request):
    return render(request,'management/teacher_joinmeeting.html')







