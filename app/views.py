﻿"""
Definition of views.
"""
import os
import subprocess
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import FeatureForm
from .models import Feature, Scenario
from .tasks import gen_feature_file, make_test_funcs

from behave.configuration import Configuration
from behave.runner import Runner

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
            conf = Configuration('media/features/{}.feature'.format(feature.id))
            conf.format = [ conf.default_format ]
            runner = Runner(conf)
            runner.run()
            make_test_funcs(runner.undefined_steps, feature.id)
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