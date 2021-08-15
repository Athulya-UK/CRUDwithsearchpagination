from django.contrib import admin
from .models import *
# Register your models here.
class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(Student, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teacher, TeacherExtraAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)
class SubjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject, SubjectAdmin)

