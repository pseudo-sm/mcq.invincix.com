from django.shortcuts import render,redirect
from django.db import connection
from random import choice
from . models import Candidate,Submission,Question,Option
from django.db.utils import IntegrityError
from django.contrib import messages
# Create your views here.

def done(request):
    
    return render(request,"done.html")

def question(request,id):
    question = fetch_next(id)
    if question is None:
        return redirect('done')
    return render(request,"exam.html",{"question":question})


def resume_exam_action(request):
    trial_registration_no = request.POST.get('regno')
    registered_registration_no = request.COOKIES.get("registration_no")
    if trial_registration_no == registered_registration_no:
        candidate = Candidate.objects.get(registration_no=trial_registration_no)
        return redirect('question/{}'.format(candidate.candidate_id))
    else:
        messages.error(request, 'You can resume your exam only in your original exam machine')
        return redirect('resume_exam')

def resume_exam(request):

    return render(request,'resume-exam.html')


def next(request):

    question_id = request.POST.get("question_id")
    choice_id = request.POST.get("choice_id")
    candidate_id = request.session.get("candidate_id")
    print(candidate_id)
    candidate=get_object(candidate_id,'Candidate')
    question=get_object(question_id,'Question')
    choice=get_object(choice_id,'Option')
    new_submission = Submission(candidate_id=candidate,question_id=question,choice_id=choice)
    new_submission.save()
    return redirect('question/{}'.format(candidate_id))

def start(request):

    name = request.POST.get("name")
    registration_no = request.POST.get("regno")
    phone = request.POST.get("mobileno")
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
    response = redirect('question/{}'.format(new_candidate.candidate_id))
    response.set_cookie('registration_no',registration_no,max_age=3600)
    return response

def index(request):

    return render(request,"index.html")

def fetch_next(candidate_id):
    total_questions = len(Question.objects.all())
    with connection.cursor() as cursor:
        cursor.execute("select id,question,image from question q where id not in (select question_id_id from submission s where s.candidate_id_id={})".format(candidate_id))
        row = cursor.fetchall()
        if len(row)==0:
            connection.close()
            return 
        qno = total_questions-len(row)+1
        question_id, question,image = choice(row)
        print(question_id,image)
        cursor.execute("select id,option_value from option where question_id={}".format(question_id))
        options = cursor.fetchall()
    connection.close()
    return {'question_id':question_id,"question":question,"options":options,'qno':qno,'total_questions':total_questions,'image':image}
        
def get_object(pk_id,obj_type):

    if obj_type=='Candidate':
        object = Candidate.objects.get(candidate_id=pk_id) 
    elif obj_type=='Question':
        object = Question.objects.get(id=pk_id)
    elif obj_type=='Option':
        object = Option.objects.get(id=pk_id)
    else:
        return "Invalid Object"
    return object