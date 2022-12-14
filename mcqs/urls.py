"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('question/<slug:qno>',views.get_question,name='get_question'),
    path('start',views.start,name="start"),
    path('next',views.next,name="next"),
    path('done',views.done,name="done"),
    path('resume-exam',views.resume_exam,name="resume_exam"),
    path('results',views.results,name="results"),
    path('resume-exam-action',views.resume_exam_action,name="resume_exam_action"),
    path('',views.index,name="index")
]


from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)