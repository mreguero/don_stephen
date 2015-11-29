import os
from django.template import loader
from django.core.files.base import ContentFile
from .models import Feature
from behave.runner_util import make_undefined_step_snippet

def gen_feature_file(feature_id):

    feature = Feature.objects.get(id=feature_id)
    template = loader.get_template('app/Feature/Base.feature')
    data_dict = {
        'description': feature.description,
        'finality': feature.finality,
        'who': feature.who,
        'purpose': feature.purpose, 
        'title': feature.scenario.all()[0].title,
        'given': feature.scenario.all()[0].given,
        'when': feature.scenario.all()[0].when,
        'then': feature.scenario.all()[0].then}

    
    c = ContentFile(content=template.render(data_dict))
    feature.ffile.save('{}.feature'.format(feature.id), c)


def make_test_funcs(steps, feature_id):

    with open('stephen_demo_repo\\test_{}.py'.format(feature_id), 'w') as f:
        for step in steps:
            test_fun = make_undefined_step_snippet(step)
            f.write(test_fun)
    return "test_{}.py".format(feature_id)

def add_to_repo(filename, feature):
    os.chdir(r'C:\Users\miguel\Documents\GitHub\don_stephen\stephen_demo_repo')
    os.system('git add {}'.format(filename))
    os.system('git commit -m "Added tests for feature {}'.format(feature))
    os.system('git push origin master')
    os.chdir(r"C:\Users\miguel\Documents\GitHub\don_stephen")
