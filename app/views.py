"""
Definition of views.
"""
import os
import json
import subprocess
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.conf import settings
from datetime import datetime
from .forms import FeatureForm
from .models import Feature, Scenario, Project
from .tasks import gen_feature_file, make_test_funcs

from behave.configuration import Configuration
from behave.runner import Runner
from app.tasks import add_to_repo

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if request.method != 'POST':
        form = FeatureForm()
        return render(
            request,
            'app/index.html',
            context_instance = RequestContext(request,
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'form': form,
            })
        )
    else:
        form = FeatureForm(request.POST)
        if form.is_valid():
            feature = Feature(description=form.cleaned_data['description'], finality=form.cleaned_data['finality'], who=form.cleaned_data['who'], purpose=form.cleaned_data['purpose'])
            feature.save()

            scenario = Scenario(given=form.cleaned_data['given'], when=form.cleaned_data['when'], then=form.cleaned_data['then'], title=form.cleaned_data['title'], feature=feature)
            scenario.save()
            gen_feature_file(feature.id)
            conf = Configuration(os.path.join(settings.PROJECT_ROOT, 'media', 'features', '{}.feature'.format(feature.id)))
            conf.format = [ conf.default_format ]
            runner = Runner(conf)
            runner.run()
            filename = make_test_funcs(runner.undefined_steps, feature.id)
            add_to_repo(filename, feature.description)
        return render(         request,
            'app/index.html',
            context_instance = RequestContext(request,
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'form': form,
            })
        )
            


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def project_list(request):
    assert isinstance(request, HttpRequest)
    projs = Project.objects.all()
    data = []
    for project in projs:
        proj = {'id': project.id,
                'name': project.name}
        data.append(proj)
    return HttpResponse(json.dumps(data))

def feature_new(request):
    print(request.POST)
    form = json.loads(request.body.decode('utf-8'))
    feature = Feature(description=form['description'], finality=form['finality'], who=form['who'], purpose=form['purpose'], project_id=form['project'])
    feature.save()

    scenario = Scenario(given=form['given'], when=form['when'], then=form['then'], title=form['title'], feature=feature)
    scenario.save()
    gen_feature_file(feature.id)
    conf = Configuration('media/features/{}.feature'.format(feature.id))
    conf.format = [ conf.default_format ]
    runner = Runner(conf)
    runner.run()
    filename = make_test_funcs(runner.undefined_steps, feature.id)
    add_to_repo(filename, feature.description)
    return HttpResponse()
