from django.contrib import admin
from .models import Question,Option,Answer,Candidate,Submission
from django import forms
# Register your models here.

class OptionInline(admin.StackedInline):
    model = Option
    extra = 4
    max_num = 4


class QuestionAdmin(admin.ModelAdmin):

    inlines = [OptionInline]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = "__all__" # for Django 1.8+

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['correct_choice'].queryset = Option.objects.filter(question=self.instance.question_id)


class AnswerAdmin(admin.ModelAdmin):
    form=AnswerForm
    

admin.site.register(Question,QuestionAdmin)
admin.site.register(Candidate)
admin.site.register(Submission)
admin.site.register(Answer,AnswerAdmin)