from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question,Answer

@receiver(post_save,sender=Question)
def notify_answer(sender,instance,created,**kwargs):
    if created:
        default_answer = Answer(question_id=instance)
        default_answer.save()

