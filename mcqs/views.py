from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from django.db import connection
from random import choice
from . models import Candidate,Submission,Question,Option,Answer,PassKey
from django.db.utils import IntegrityError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta,datetime
from django.db import connection
# Create your views here.

def done(request):
    response = render(request,"done.html")
    response.set_cookie('registration_no',None,max_age=7200)
    return response

def resume_exam(request):

    return render(request,"resume-exam.html")


def resume_exam_action(request):
    trial_registration_no = request.POST.get('regno')
    registered_registration_no = request.COOKIES.get("registration_no")
    if trial_registration_no == registered_registration_no:
        candidate = Candidate.objects.get(registration_no=trial_registration_no)
        return redirect('question/1'.format(candidate.candidate_id))
    else:
        messages.error(request, 'You can resume your exam only in your original exam machine')
        return redirect('resume_exam')

def next(request):
    question_id = request.POST.get("question_id")
    choice_id = request.POST.get("choice_id")
    registration_no = request.COOKIES.get("registration_no")
    if registration_no is None:
        messages.error(request, 'Something went wrong.')
        return redirect('index')
    candidate = Candidate.objects.get(registration_no=registration_no)
    question=get_object(question_id,'Question')
    choice=get_object(choice_id,'Option')
    submission = Submission.objects.get(question_id=question,candidate_id=candidate)
    if choice is not None:
        submission.choice_id = choice
        submission.save()
    max_qno = Submission.objects.filter(candidate_id=candidate.candidate_id).order_by("-qno")[0].qno
    if int(submission.qno)==int(max_qno):
        return redirect('question/1')
    return redirect('question/{}'.format(submission.qno+1))

def start(request):

    name = request.POST.get("name")
    registration_no = request.POST.get("regno")
    phone = request.POST.get("mobileno")
    passkey = request.POST.get("passkey")
    valid_passkeys = list(PassKey.objects.filter(validity_start__lte=datetime.now()).filter(validity_end__gte=datetime.now()).values_list("passcode",flat=True))
    print(valid_passkeys)
    if passkey not in valid_passkeys:
        messages.error(request,'Invalid passkey')
        return redirect('index')
    if "" in [name,registration_no,phone]:
        messages.error(request, 'All fields are mandatory.')
        return redirect('index')
    try:
        new_candidate = Candidate(name=name,registration_no=registration_no,phone=phone)
        new_candidate.save()
        request.session["candidate_id"] = new_candidate.candidate_id
    except IntegrityError:
        messages.error(request, 'Candidate already registered')
        return redirect('index')
    qno = 1
    for question in Question.objects.order_by('?'):
        default_submission = Submission(candidate_id=new_candidate,question_id=question,qno=qno)
        default_submission.save()
        qno+=1
    response = redirect('question/1')
    response.set_cookie('registration_no',registration_no,max_age=7200)
    return response

def index(request):

    return render(request,"index.html")

def fetch_next(candidate_id):
    
    return {'question_id':question_id,"question":question,"options":options,'qno':qno,'total_questions':total_questions,'image':image}

def get_object(pk_id,obj_type):
    try:
        if obj_type=='Candidate':
            object = Candidate.objects.get(candidate_id=pk_id)
        elif obj_type=='Question':
            object = Question.objects.get(id=pk_id)
        elif obj_type=='Option':
            object = Option.objects.get(id=pk_id)
        else:
            return "Invalid Object"
        return object
    except ObjectDoesNotExist:
        None

def results(request):
    with connection.cursor() as cursor:
        cursor.execute('''            
            select cand.name candidate_name,cand.phone,cand.registration_no,cand.time, count(1) correct from submission sub
            join
            candidate cand on (sub.candidate_id_id = cand.candidate_id)
            join answer a on(a.question_id_id = sub.question_id_id and a.correct_choice_id = sub.choice_id_id)
            group by cand.name
            order by count(1) desc;
        ''')
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in results
        ]
        max_qno = Question.objects.count()
    return render(request,"results.html",{'results':results,'max_qno':max_qno})

def results1(request):
    candidates = Candidate.objects.all()
    questions = Question.objects.all()
    submissions = Submission.objects.all()
    answers = Answer.objects.all()
    results = []
    correct_aptitude = 0
    correct_program = 0
    for candidate in candidates:
        for question in questions:
            try:
                unit_submission = submissions.get(question_id=question,candidate_id=candidate)
                correct_choice = answers.get(question_id=unit_submission.question_id).correct_choice
                if unit_submission.choice_id == correct_choice:
                    if question.category=='Program':
                        correct_program+=1
                    else:
                        correct_aptitude+=1
            except ObjectDoesNotExist:
                pass
        apti_total = questions.filter(category='Aptitude').count()
        program_total = questions.filter(category='Program').count()
        correct_program = round(correct_program*100/program_total,2)
        correct_aptitude = round(correct_aptitude*100/apti_total,2)
        results.append({"registration_no":candidate.registration_no,"name":candidate.name,"phone":candidate.phone,"program":correct_program,"aptitude":correct_aptitude})

    return render(request,"results.html",{"results":results})


def get_question(request,qno):
    registration_no = request.COOKIES.get("registration_no")
    if registration_no is None:
        messages.error(request, 'Something went wrong.')
        return redirect('index')
    candidate = Candidate.objects.get(registration_no=registration_no)
    result_question = {}
    with connection.cursor() as cursor:
        cursor.execute("select q.id,question,image from question q join submission s on (s.question_id_id = q.id and s.qno={} and s.candidate_id_id={})".format(qno,candidate.candidate_id))
        result_question["question_id"],result_question["question"],result_question["image"] = cursor.fetchall()[0]
        cursor.execute("select id,option_value from option where question_id={}".format(result_question["question_id"]))
        result_question["options"] = cursor.fetchall()
    connection.close()
    submissions = list(Submission.objects.filter(candidate_id=candidate.candidate_id).values("question_id","choice_id","qno"))
    finish = False
    max_qno = Submission.objects.filter(candidate_id=candidate.candidate_id).order_by("-qno")[0].qno
    if int(qno)==int(max_qno):
        finish = True
    if(candidate.time<timedelta(minutes=150)):
        started = 1
    else:
        started = 0
    return render(request,"exam.html",{"question":result_question,"submissions":submissions,"finish":finish,"registration_no":registration_no,"started":started,"qno":qno,"max_qno":max_qno})