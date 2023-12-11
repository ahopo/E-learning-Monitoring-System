from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from members.models import Employee, Course, CompliantCourse, Section
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.db.models import Q
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import textract
import datetime
from django.http import request
logger = logging.getLogger(__name__)
now = datetime.datetime.now()


def index(request):
    searchval = request.GET.get('eid')
    courses = Course.objects.all().order_by('status')

    if searchval != None:
        courses = Course.objects.filter(title__contains=searchval)
    context = {
        'courses': courses,
        'index': True
    }
    return render(request, 'index.html', context)


def complaintsview(request):
    try:
        section_id = 0
        compliant = 0
        total = 0
        compliant_per = 'No data found'
        non_compliant_per = 'No data found'
        non_compliant = 0
        query = request.GET.get('q')    
        querysec = request.GET.get('s')
        queryempid = request.GET.get('eid')
        POST = False
        try:
            if(querysec == None):
                querysec=request.session['sec']
                INSECTION=True
        except:
            INSECTION=False
        sections = Section.objects.all()
        if(querysec == None and not INSECTION):
            querysec=1
        else:            
            INSECTION=True
            request.session['sec'] = querysec
        if request.method == 'POST':
            POST = True
            modalmethod(request)
        if queryempid != None and queryempid != '':
            if query == None:
                query = request.session['course_id']
            compliantcourses = CompliantCourse.objects.filter(
                course=query, employee_id=queryempid)
            logger.error(compliantcourses)
        elif querysec != None and queryempid == None or queryempid=='':
            if query == None or query == '' and INSECTION:
                query = request.session['course_id']
                querysec= request.session['sec']        
            compliantcourses = CompliantCourse.objects.filter(
                course=query, section=querysec).order_by('-status')
            compliant = CompliantCourse.objects.filter(
                course=query, section=querysec, status=1).count()
            non_compliant = CompliantCourse.objects.filter(
                course=query, section=querysec, status=2).count()
        else:
            if query == None or query == '':
                query = request.session['course_id']

            compliantcourses = CompliantCourse.objects.filter(
                Q(course=query)).order_by('-status')
            compliant = CompliantCourse.objects.filter(
                course=query, status=1).count()
            non_compliant = CompliantCourse.objects.filter(
                course=query, status=2).count()
        if POST and queryempid != None and queryempid != '':
            query = request.session['course_id']
            compliantcourses = CompliantCourse.objects.filter(
                course=query, employee_id=queryempid)
            compliant = CompliantCourse.objects.filter(
                course=query, status=1).count()
            non_compliant = CompliantCourse.objects.filter(
                course=query, status=2).count()
        if not POST and compliantcourses.exists() and queryempid == None or queryempid == '':
            total = compliant+non_compliant
            section_id = compliantcourses[0].section.id
            logger.error(total)
            compliant_per = "{}%".format(round(compliant/total*100, 2))
            non_compliant_per = "{}%".format(round(non_compliant/total*100, 2))

            if querysec == None and query!='' or query!=None:
                request.session['course_id'] = query
                request.session['course_title'] = compliantcourses[0].course.title

        
        page = request.GET.get('page', 1)

        paginator = Paginator(compliantcourses, 20)
        try:
            compliantcourses = paginator.page(page)
        except PageNotAnInteger:
            compliantcourses = paginator.page(1)
        except EmptyPage:
            compliantcourses = paginator.page(paginator.num_pages)
        logger.error(compliantcourses)
        context = {
            'compliantcourses': compliantcourses,
            'sections': sections,
            'section_id': section_id,
            'compliant': compliant,
            'non_compliant': non_compliant,
            'compliant_per': compliant_per,
            'non_compliant_per': non_compliant_per,
            'total': total,
            'title': "• {}".format(request.session['course_title']),
            'incompliant': True

        }

        return render(request, 'compliants.html', context)
    except (ValueError, IndexError):
        return redirect('../')


def modalmethod(request):
    query = request.POST.get('val')
    upload_file = request.FILES['document']
    if upload_file.name.endswith('.pdf'):
        fs = FileSystemStorage()
        if not fs.exists(upload_file.name):
            fs.save(upload_file.name, upload_file)

        EXTRACTED_TEXT = textract.process(
            "media/{}".format(upload_file.name), encoding='utf-8', extension='pdf')

        textstr = str(EXTRACTED_TEXT)
        lines = textstr.count('\\r\\n')
        employee_name = "notvalid"
        course_name = "notvalid"

        date_completed = "notvalid"
        empdata = CompliantCourse.objects.filter(id=query)
        empcrstitle = empdata[0].course.title
        empname = empdata[0].employee_name.split('(')[0]
        empname = ' '.join(empname.split())
        crs_created = empdata[0].course.date_created.year
        logger.error("EMPLOYEE NAME:"+empname)
        for x in range(lines):
            linevalue = textstr.replace('\\r\\n', '\n').splitlines()[x]
            if x == 0:
                continue
            if(empcrstitle == linevalue):
                course_name = linevalue
                logger.error('Title passed')
            if(empname in linevalue):
                employee_name = linevalue
                logger.error('Employee name passed')
            if(str(crs_created) in linevalue):
                date_completed = linevalue
                logger.error('date name passed')
            if(str(crs_created+1) in linevalue):
                date_completed = linevalue

            elif x == lines-1:
                msgs = []
                if(course_name == 'notvalid'):
                    msgs.append('Course Title')
                if(employee_name == 'notvalid'):
                    msgs.append('Employee name')
                if(date_completed == 'notvalid'):
                    msgs.append('Date')
                logger.error(date_completed == 'notvalid')
                logger.error(date_completed)

                if(msgs == []):
                    CompliantCourse.objects.filter(id=query).update(status='1')
                    crs = CompliantCourse.objects.filter(id=query)
                    messages.success(request, "Thank you for completing {} on {}".format(
                        course_name, date_completed))
                    return redirect('../complaintsview/?eid={}'.format(crs[0].employee_id))

                else:
                    messages.warning(
                        request, "invalid ({})".format(', '.join(msgs)))

    else:
        messages.error(
            request, '{} is not a pdf file'.format(upload_file.name))
    storage = messages.get_messages(request)
    storage.used = True
