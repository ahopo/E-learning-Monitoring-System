from django.db import models
from string import Formatter
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Section(models.Model):    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class Manager(models.Model):
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.given_name + ' ' + self.surname


# Create your models here.
class Employee(models.Model):
    employee_id = models.IntegerField(verbose_name='EMPLOYEE ID')
    surname = models.CharField(max_length=255, verbose_name='SURNAME')
    given_name = models.CharField(max_length=255, verbose_name='GIVEN NAME')
    email_add = models.CharField(max_length=255, verbose_name='EMAIL ADDRESS')
    section_id = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, verbose_name='SECTION')
    manager_id = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, verbose_name='MANAGER')
    status = models.BooleanField(
        default=True, verbose_name='STATUS', blank=True)

    def __str__(self):
        return self.given_name+' '+self.surname + ' . ' + self.manager_id.given_name + ' '+self.manager_id.surname


CouseStatus = (
    ("1", "Active"),
    ("2", "In Progress"),
    ("3", "Done"),
    ("4", "Cancelled"),
)


class Course(models.Model):
    url = models.CharField(max_length=255)
    date_created=models.DateField(auto_now_add=True)
    completion_date = models.DateField()
    title = models.CharField(max_length=255)
    class_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20,
                              choices=CouseStatus,
                              default='2')
    class_description = models.TextField(max_length=2000)

    def __str__(self):
        return self.title


CouseCompiantStatus = (
    ("1", "Compliant"),
    ("2", "Non compliant"),
)


class CompliantCourse(models.Model):

    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, verbose_name='Course')
    employeedb_id=models.IntegerField()
    employee_id = models.CharField(max_length=255)
    employee_name = models.CharField(max_length=255)
    manager=models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, verbose_name='MANAGER')
    status = models.CharField(max_length=20,
                              choices=CouseCompiantStatus,
                              default='2')
    section=models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, verbose_name='SECTION')

    def __str__(self):
        return self.employee_id


@receiver(post_save, sender=Course)
def course_is_created(sender, instance, created, **kwargs):
    if created:
        for emp in Employee.objects.filter(status='1'):
            CompliantCourse.objects.create(employeedb_id=emp.id, course=instance, employee_id=emp.employee_id, employee_name=(
                emp.given_name+'  '+emp.surname+' ('+emp.email_add+')'),section=emp.section_id,manager=emp.manager_id)
