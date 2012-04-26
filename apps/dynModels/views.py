# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson

from apps.dynModels.utils import DynamicModels

def index(request):
    mod = DynamicModels('models.yaml')
    data = {
        'models_name':mod.getModelsName(),
    }
    return render(request, 'dynModels_index.html', data)

def content(request):
    json = {'error': 1, 'rows': [], 'header': [],}
    if request.is_ajax():
        name = request.GET.get('t', None)
        if name:
            model = DynamicModels().get(name)
            if model:
                not_return = ['id',]
                fields = model._meta.fields
                for f in fields:
                    if f.name not in not_return:
                        json['header'].append(f.verbose_name)
                for m in model.objects.all():
                    row = {}
                    for f in fields:
                        if f.name not in not_return:
                            row[f.name] = getattr(m, f.name)
                    json['rows'].append(row)
                json['error'] = 0
    return HttpResponse(simplejson.dumps(json), mimetype='application/json')
