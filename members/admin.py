from django.contrib import admin
from .models import Employee, Manager, Section, Course, CompliantCourse
from django.http import HttpResponse
import csv
import logging
# Register your models here.
logger = logging.getLogger(__name__)

class EmpAdmin(admin.ModelAdmin):
    fields = (
        ('employee_id', 'status'),
        'email_add',
        ('surname', 'given_name'),
        ('manager_id', 'section_id'))
    list_display = ('fullname',
                    'manager_id', 'section_id', 'status', 'employee_id')

    list_filter = ('status', 'section_id', 'manager_id')
    search_fields = ('employee_id', 'surname', 'given_name')
    list_editable = ('status', 'manager_id')

    def fullname(self, obj):
        return ("%s, %s (%s)" % (obj.surname, obj.given_name, obj.email_add))
    fullname.short_description = 'Full name'

    list_per_page = 50


admin.site.register(Employee, EmpAdmin)


@admin.register(Manager)
class MngrAdmiin(admin.ModelAdmin):
    pass


@admin.register(Section)
class SecAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')


def Export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Elearning_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'SURNAME', 'GIVEN NAME',
                     'E-MAIL ADDRESS', 'Section', 'Manager', 'Status'])
    # SURNAME	GIVEN NAME	E-MAIL ADDRESS	Section	Manager

    coursecompliant = queryset.values_list('employeedb_id', 'status')    
    for crscmp in coursecompliant:
        emp_id = crscmp[0]
        
        empdata = Employee.objects.filter(id=emp_id)

        if(crscmp[1] == '1'):
            emp_status = 'Compliant'
        else:
            emp_status = 'Non compliant'
        writer.writerow([
            empdata[0].employee_id, 
            empdata[0].surname,
            empdata[0].given_name, 
            empdata[0].email_add,
            empdata[0].section_id.name, 
            empdata[0].manager_id.given_name+' '+empdata[0].manager_id.surname, 
            emp_status])
        
    return response


Export_to_csv.short_description = 'Export to csv'


@admin.register(CompliantCourse)
class CompliantCourseAdmin(admin.ModelAdmin):
    search_fields = ('employee_id', 'section__name', 'employee_name')
    readonly_fields = ["course", "employee_id", "employee_name"]
    list_display = ('employee_name', 'employee_id', 'course', 'status')
    list_filter = ('course__title', 'section__name')
    list_editable = ('status',)
    list_per_page = 20
    fields = (
        ('status', 'section'),
        'course',
        ('employee_id', 'employee_name'))
    actions = [Export_to_csv, ]
