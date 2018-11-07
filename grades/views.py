from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Student


# Create your views here.
def index(request):
    context = {
        'heading': 'Welcome to A Grade Book',
        'title': 'A Grade Book'
    }
    if not request.user.is_authenticated():
        context['content'] = 'Must <a href="/login/">login</a> to use the application.',
    #return HttpResponse(html)
    return render(request, 'grades/index.html', context)


def about(request):
    #print(request)
    data = {'heading': 'About',
            'content': 'Demo program developed using django framework.',
            'title': 'About A Grade Book App'
            }
    return render(request, 'grades/index.html', data)


def showGrades(request):
    html = """
        <table>
            <tr>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Test 1</th>
                <th>Test 2</th>
                <th>Test 3</th>
                <th>Average </th>
                <th colspan="2">Tools</th>
            </tr>
        """
    for student in Student.objects.all():
        student.findAverage()
        student.save()
        html += """<tr>
                    <td>{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                    <td>{3}</td>
                    <td>{4}</td>
                    <td>{5:.2f}</td>
                    <td><a href="{6}">Edit</a></td>
                    <td><a href="{7}">Delete</a></td>
                    </tr>
                """.format(student.first_name, student.last_name, student.test1,
                           student.test2, student.test3, student.avg,
                           reverse('grade', args=(student.id,)),
                           reverse('delete', args=(student.id,)))

    html += "</table>"
    return HttpResponse(html)


@login_required(login_url='/login/')
def allGrades(request):
    students = Student.objects.order_by("-avg")
    data = ""
    for student in students:
        data += str(student.id) + "  " + student.first_name + "  " + str(student.avg) + "<br>"

    return HttpResponse(data)


def showGradesUsingTemplate(request):
    if not request.user.is_authenticated():
        return render(request, 'grades/login.html')

    students = Student.objects.order_by('-avg')
    for student in students:
        student.findAverage()
        student.save()

    context = {
            'title': 'All Students Grades',
            'heading': "All Students' Grades",
            'students_list': students,
            }
    return render(request, 'grades/grades.html', context)


@login_required()
def saveGrade(request, student_id=None):
    errors = []
    if request.method == 'POST':
        # handle data posted from the from
        if not request.POST.get('first_name', ''):
            errors.append('Enter first name.')
        if not request.POST.get('last_name'):
            errors.append('Enter last name.')
        if not request.POST.get('test1', ''):
            errors.append('Enter Test 1')
        if not request.POST.get('test2', ''):
            errors.append('Enter Test 2')
        if not request.POST.get('test3', ''):
            errors.append('Enter Test 3')

        if student_id:
            student = Student.objects.get(pk=student_id)
        else:
            student = Student()
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.test1 = request.POST.get('test1')
        student.test2 = request.POST.get('test2')
        student.test3 = request.POST.get('test3')
        data = {
            'errors': errors,
            'student': student,
            }
        if errors:
            data['heading'] = 'Add New Student Grade'
            data['content'] = 'Fill in the following information:'
            return render(request, 'grades/edit_grade.html', data)
        else:
            student.test1 = float(student.test1)
            student.test2 = float(student.test2)
            student.test3 = float(student.test3)
            student.findAverage()
            student.save()
            data['heading'] = 'Success'
            data['content'] = 'Student grade updated successfully!'
            data['student'] = student
            return render(request, 'grades/edit_grade.html', data)
    else:
        if not student_id:
            # must be a get method to enter new grade info so render the form for user to enter
            # data
            data = {
                'heading': 'Add New Student Grade',
                'content': 'Fill in the following information',
                'errors': errors,
            }
        else:
            # edit existing student
            #student = Student.objects.get(pk=student_id)
            student = get_object_or_404(Student, pk=student_id)
            data = {
                'heading': 'Edit Student Grade',
                'content': 'Update the following information',
                'errors': errors,
                'student': student,
            }
        return render(request, 'grades/edit_grade.html', data)


@login_required()
def deleteGrade(request, student_id):
    #student = Student.objects.get(pk=student_id)
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return showGrades(request)


def login_view(request):
    context = {
        'title': 'Login',
        'heading': 'Login',
    }
    return render(request, 'grades/login.html', context)


def loginProcess(request):
    errors = []
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not username:
            errors.append('Username is required')
        if not password:
            errors.append('Password is required')

        if not errors:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user) #adds session info for user
                    context = {
                        'heading': 'Welcome to A Grade Book.',
                        'title': 'A Grade Book',
                    }
                    return render(request, 'grades/index.html', context)
                else:
                    errors.append('This account has been disabled.')
            else:
                errors.append('Invalid username or password.')

        context['errors'] = errors
        return render(request, 'grades/login.html', context)
    else:
        login_view(request)


def logout_view(request):
    logout(request)
    context = {
        'heading': 'Successfully logged out.',
        'content': '<a href="/login/">Log back in again.</a>',
        'title': 'Logout Successful'
    }
    return render(request, 'grades/index.html', context)