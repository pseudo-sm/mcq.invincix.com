from django.db import models
from datetime import timedelta
# Create your models here.

class Question(models.Model):

    id = models.AutoField(primary_key=True)
    question = models.TextField()
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to="questions/",null=True,blank=True)

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'question'

class Option(models.Model):

    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    option_value = models.CharField(max_length=255)

    def __str__(self):
        return self.option_value

    class Meta:
        db_table = 'option'

class Answer(models.Model):

    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    correct_choice = models.ForeignKey(Option,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'answer'

    def __str__(self):
        return self.question_id.question


class Candidate(models.Model):

    candidate_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False,blank=False)
    registration_no = models.CharField(max_length=255,unique=True,null=False,blank=False)
    phone = models.CharField(max_length=100)
    time = models.DurationField(default=timedelta(minutes=150))

    def __str__(self):
        return self.name + '({})'.format(self.candidate_id)

    class Meta:
        db_table = 'candidate'

class Submission(models.Model):

    candidate_id = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Option,on_delete=models.CASCADE,null=True,blank=True)
    qno = models.IntegerField()
    class Meta:
        db_table = 'submission'

class PassKey(models.Model):

    passcode = models.CharField(max_length=100)
    validity_start = models.DateTimeField()
    validity_end = models.DateTimeField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.passcode
