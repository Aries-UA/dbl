# -*- coding: utf-8 -*-
import datetime
from django.template import RequestContext
from django import template

register = template.Library()

def header():
    return {}

def footer():
    return {}
    
def menu():
    return {}

register.inclusion_tag('templatetags/header.html')(header)
register.inclusion_tag('templatetags/footer.html')(footer)
register.inclusion_tag('templatetags/menu.html')(menu)
