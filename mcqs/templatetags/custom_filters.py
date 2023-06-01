from django import template
from datetime import timedelta
register = template.Library()

@register.filter
def in_mins(time):
    seconds = (time // 1000000)
    consumed = (40*60) - (seconds)
    minutes = round(consumed // 60,2)
    seconds = consumed % 60
    formatted_duration = "{}m:{}s".format(minutes, seconds)
    return formatted_duration
    
